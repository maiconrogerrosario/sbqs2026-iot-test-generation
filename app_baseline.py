import json
import sys

from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import glob
import yaml
import os
import logging

load_dotenv()

app = Flask(__name__)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # FORÇA SAÍDA NO TERMINAL
    ]
)


logger = logging.getLogger("app_ontologia")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def load_ontologies(path="./ontologias/"):
    ontologias = {}
    arquivos = glob.glob(os.path.join(path, "*.yaml")) + glob.glob(os.path.join(path, "*.yml"))

    logger.info("Buscando arquivos de ontologia na pasta: %s", path)
    logger.info("Arquivos encontrados: %s", arquivos)

    for arquivo in arquivos:
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if isinstance(data, dict):
                for k, v in data.items():
                    ontologias[k] = v
                    logger.info("Ontologia '%s' carregada com sucesso do arquivo: %s", k, os.path.basename(arquivo))
            else:
                logger.warning("O arquivo '%s' não possui um objeto válido na raiz.", arquivo)
        except Exception as e:
            logger.error("Erro ao ler o arquivo '%s': %s", arquivo, e, exc_info=True)

    logger.info("Total de ontologias em memória: %s", list(ontologias.keys()))
    return ontologias


ontologias = load_ontologies()


def build_form_fields(ontologia):
    campos = []
    valores_default = {}

    properties = ontologia.get("properties", {})
    logger.debug("Construindo campos do formulário a partir de 'properties'.")

    for campo, info in properties.items():
        if not isinstance(info, dict):
            logger.debug("Propriedade '%s' ignorada: conteúdo não é um dicionário.", campo)
            continue

        if info.get("editable") is False:
            logger.debug("Propriedade '%s' ignorada: editable=False.", campo)
            continue

        if info.get("type") == "object":
            logger.debug("Propriedade '%s' ignorada: tipo é 'object'.", campo)
            continue

        opcoes = ",".join(map(str, info.get("allowedValues", info.get("items", []))))
        campos.append({
            "Campo": campo,
            "Tipo": info.get("type", "string"),
            "Descrição": info.get("description", ""),
            "Opções": opcoes
        })

        valores_default[campo] = info.get("value", "")
        logger.debug("Campo mapeado para o formulário: %s (Default: %s, Opções: [%s])", campo, valores_default[campo],
                     opcoes)

    campos.append({
        "Campo": "hasTestMode",
        "Tipo": "string",
        "Descrição": "Modo de teste",
        "Opções": "Sensor Físico,Mock,Ambos"
    })
    valores_default["hasTestMode"] = "Mock"

    return campos, valores_default


def collect_form_answers(campos, request_form):
    respostas = {}
    logger.info("Coletando respostas enviadas pelo formulário HTTP POST.")

    for c in campos:
        nome_campo = c["Campo"]
        valor_bruto = request_form.get(nome_campo)
        respostas[nome_campo] = valor_bruto
        logger.debug("Resposta capturada -> %s: %s", nome_campo, valor_bruto)

    return respostas


def build_prompt(sensor, ontologia, campos, respostas):
    logger.info("================ CONSTRUINDO PROMPT ================")
    logger.info("Sensor: %s", sensor)

    modo_teste = respostas.get("hasTestMode", "Ambos")
    logger.info("Modo de teste: %s", modo_teste)

    # Converte ontologia para JSON
    ontologia_json = json.dumps(ontologia, indent=2, ensure_ascii=False)

    # Parâmetros do usuário
    parametros = "\n".join([f"- {c['Campo']}: {respostas.get(c['Campo'])}" for c in campos])

    prompt = f"""Contexto:
Gerar casos de teste para validar o comportamento do componente físico do sensor {sensor}
integrado à plataforma alvo.



Modo de execução: {modo_teste}

"""

    logger.info(f"📏 Tamanho do prompt: {len(prompt)} caracteres")
    logger.info("\n" + "=" * 80)
    logger.info("📝 PROMPT ENVIADO:")
    logger.info("=" * 80)
    logger.info("\n" + prompt[:2000] + "..." if len(prompt) > 2000 else prompt)  # Mostra início
    logger.info("\n" + "=" * 80)

    return prompt


def generate_code(prompt):
    logger.info("🚀 Chamando a API da OpenAI com o modelo 'gpt-4o-mini'...")

    # Log do tamanho do prompt para debug
    logger.info(f"📏 Tamanho do prompt: {len(prompt)} caracteres")

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um especialista em C++ e Arduino para IoT. "
                        "Siga ESTRITAMENTE as instruções do usuário. "
                        "Gere APENAS o código solicitado, sem explicações."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,  # Consistente
            max_tokens=3500,  # Suficiente para qualquer sensor
            top_p=0.95,
            frequency_penalty=0.1,
            presence_penalty=0.1,
            timeout=90
        )

        codigo_gerado = resposta.choices[0].message.content.strip()

        # LOG COM INFO (para você ver)
        logger.info("✅ Resposta recebida com sucesso da OpenAI.")
        logger.info(f"📊 Tokens usados: {resposta.usage.total_tokens if hasattr(resposta, 'usage') else 'N/A'}")
        logger.info(f"📏 Tamanho do código: {len(codigo_gerado)} caracteres")

        # Mostra o código no log (INFO em vez de DEBUG)
        logger.info(
            "\n" + "=" * 80 + "\n" +
            "📝 CÓDIGO GERADO PELA OPENAI:\n" +
            "=" * 80 + "\n" +
            codigo_gerado + "\n" +
            "=" * 80 + "\n" +
            "✅ FIM DO CÓDIGO\n"
        )

        # Validação básica do código
        if not codigo_gerado or len(codigo_gerado) < 50:
            logger.warning("⚠️ Código gerado muito curto ou vazio!")

        # Verifica se tem includes básicos de Arduino
        if "include" not in codigo_gerado.lower():
            logger.warning("⚠️ Código pode estar faltando includes!")

        return codigo_gerado

    except Exception as e:
        logger.error("❌ Falha na comunicação ou processamento da OpenAI API: %s", e, exc_info=True)

        # Retorna um erro amigável em vez de só levantar exceção
        return f"""
// ❌ ERRO AO GERAR CÓDIGO
// Detalhes: {str(e)}
// 
// Por favor, tente novamente ou verifique:
// 1. Sua chave API da OpenAI
// 2. Conexão com a internet
// 3. Se o prompt não está muito longo
"""





@app.route("/")
def home():
    logger.info("Acessando a rota Home (/).")

    plataformas = {
        "Arduino": ["DS18B20", "HCSR04"],
    }


    return render_template("home.html", plataformas=plataformas)


@app.route("/sensor/<sensor>", methods=["GET", "POST"])
def formulario(sensor):
    logger.info("Rota /sensor/%s chamada com método: %s", sensor, request.method)
    ontologia = ontologias.get(sensor)

    if not ontologia:
        logger.error("Ontologia solicitada não encontrada na memória: %s", sensor)
        return f"Ontologia para {sensor} não encontrada.", 404

    campos, valores_default = build_form_fields(ontologia)

    if request.method == "POST":
        try:
            respostas = collect_form_answers(campos, request.form)
            prompt = build_prompt(sensor, ontologia, campos, respostas)
            codigo = generate_code(prompt)
            return render_template(
                "resultado.html",
                codigo=codigo,
                ontologia=sensor
            )
        except Exception as err:
            logger.exception("Erro crítico no fluxo POST do sensor '%s': %s", sensor, err)
            return f"Ocorreu um erro interno ao processar a geração. Detalhes salvos nos logs de execução.", 500

    return render_template(
        "formulario.html",
        ontologia=sensor,
        campos=campos,
        valores_default=valores_default
    )


@app.route("/plataforma/<nome>")
def ver_plataforma(nome):
    logger.info("Rota de visualização por plataforma acionada: %s", nome)
    sensores = []

    for sensor_name, sensor_info in ontologias.items():
        plataforma = sensor_info.get("properties", {}) \
            .get("hasPlatform", {}) \
            .get("value")

        if plataforma == nome:
            sensores.append(sensor_name)

    logger.debug("Sensores encontrados para a plataforma '%s': %s", nome, sensores)
    return render_template(
        "plataforma.html",
        nome=nome,
        sensores=sensores
    )


if __name__ == "__main__":
    logger.info("Iniciando o servidor Flask de Ontologia IoT...")
    app.run(debug=True)