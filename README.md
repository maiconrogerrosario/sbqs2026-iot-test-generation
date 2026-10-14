# SBQS 2026 — Geração Automática de Casos de Teste para Dispositivos IoT com Ontologias e LLMs

Este repositório contém a implementação do protótipo e os artefatos experimentais associados ao artigo:

**An Ontology- and LLM-Based Approach for Automatic Test Case Generation in IoT Devices**

Aceito no **XXV Simpósio Brasileiro de Qualidade de Software (SBQS 2026)**, realizado em Maringá, Paraná, Brasil.

## 1. Visão Geral

Este trabalho apresenta uma abordagem para apoiar a geração automática de casos de teste funcionais para a camada de dispositivos da Internet das Coisas (IoT), combinando:

- Ontologias leves para representação de conhecimento;
- Modelos de linguagem de grande porte (LLMs);
- Orquestração de prompts utilizando Python e Flask;
- Geração de código de teste em C++ para a plataforma Arduino;
- Utilização do framework AUnit para testes automatizados.

A proposta concentra-se na validação da integração e compatibilidade entre o firmware executado em microcontroladores e os componentes físicos conectados, como sensores e atuadores.

O conhecimento técnico dos componentes inclui propriedades operacionais, protocolos de comunicação, bibliotecas de software, interfaces funcionais, configurações de hardware e restrições utilizadas na geração de testes.

A ontologia foi inicialmente modelada em OWL utilizando o Protégé. Na implementação experimental apresentada neste repositório, o conhecimento foi organizado em arquivos YAML, utilizados como representação operacional pela aplicação.

Nesta versão, não são realizadas consultas SPARQL diretamente à ontologia OWL.

## 2. Arquitetura da Abordagem

A solução é organizada em quatro camadas principais:

**Camada de apresentação:** Interface web responsável pela seleção da plataforma, escolha do sensor, configuração dos parâmetros e visualização do código gerado.

**Camada de representação do conhecimento:** Armazena as descrições estruturadas dos dispositivos IoT, incluindo propriedades, relacionamentos, dependências e restrições.

**Camada de orquestração:** Recupera as informações do componente selecionado, combina os parâmetros informados pelo usuário e constrói o prompt enviado ao LLM.

**Camada de inteligência artificial:** Utiliza o modelo de linguagem para produzir código de teste em C++ destinado à plataforma Arduino.

O fluxo da aplicação é representado por:

```text
Interface Web (Flask)
        |
        v
Seleção do Sensor e Parâmetros
        |
        v
Representação de Conhecimento (YAML)
        |
        v
Construção do Prompt
        |
        v
Modelo de Linguagem (LLM)
        |
        v
Geração de Código C++ / AUnit
        |
        v
Visualização do Código Gerado
```

A aplicação realiza a geração dos artefatos, mas não executa automaticamente os testes nos dispositivos físicos.

## 3. Organização do Repositório

```text
sbqs2026-iot-test-generation/
|
|-- README.md
|-- requirements.txt
|-- .env.example
|-- .gitignore
|
|-- app_baseline.py
|-- app_ontology_guided.py
|
|-- ontologias/
|   |-- DS18B20.yml
|   |-- HCSR04.yml
|
|-- templates/
|   |-- base.html
|   |-- home.html
|   |-- plataforma.html
|   |-- formulario.html
|   |-- resultado.html
|   |-- index.html
|
|-- experiments/
    |-- README.md
    |
    |-- baseline/
    |   |-- prompts/
    |   |-- generated/
    |   |-- logs/
    |
    |-- ontology_guided/
        |-- prompts/
        |-- generated/
        |-- logs/
```

Os arquivos `requirements.txt`, `.gitignore` e `experiments/README.md` devem ser adicionados caso ainda não estejam presentes no repositório.

## 4. Versões Experimentais

O repositório disponibiliza duas configurações para investigar a influência do conhecimento estruturado na geração de casos de teste.

### 4.1. Versão sem Contexto Ontológico — Baseline

**Arquivo:** `app_baseline.py`

Nesta condição, o modelo de linguagem recebe uma instrução genérica solicitando a geração de casos de teste para determinado sensor IoT.

Embora a aplicação utilize os arquivos YAML para apresentar os componentes e construir os formulários, as propriedades técnicas estruturadas não são incorporadas ao prompt.

Essa condição é utilizada como referência exploratória para analisar a geração sem contextualização ontológica explícita.

### 4.2. Versão Orientada por Ontologia

**Arquivo:** `app_ontology_guided.py`

Nesta condição, o modelo recebe um prompt estruturado contendo informações derivadas da representação ontológica.

O contexto fornecido inclui:

- Hierarquia de classes;
- Propriedades de objeto e de dados;
- Limites operacionais e valores de erro;
- Protocolos de comunicação;
- Bibliotecas de software e testes;
- Configurações de hardware;
- Interfaces funcionais;
- Parâmetros selecionados pelo usuário;
- Restrições e instruções para geração do código.

O objetivo é orientar a produção de casos de teste mais relacionados às características técnicas dos componentes físicos.

As duas configurações diferem tanto na quantidade de contexto fornecido quanto nas instruções de geração. Portanto, a comparação não permite atribuir exclusivamente à ontologia todas as diferenças observadas nos resultados.

## 5. Construção dos Prompts

A construção dos prompts é realizada pela função `build_prompt()`, presente nas aplicações Flask.

Na versão orientada por ontologia, o prompt é formado pela combinação de:

```text
Contexto da Tarefa
        |
        v
Parâmetros Selecionados pelo Usuário
        |
        v
Modo de Execução
        |
        v
Instruções Obrigatórias
        |
        v
Conhecimento Estruturado (JSON)
        |
        v
Envio ao Modelo de Linguagem
```

A representação YAML do componente é convertida para JSON e incorporada ao prompt.

A aplicação também envia uma instrução de sistema que orienta o modelo a atuar como especialista em C++ e Arduino e retornar apenas o código solicitado.

As instruções de geração incluem restrições relacionadas ao framework de testes, interfaces permitidas, configurações de hardware e padrões de código proibidos.

## 6. Configuração do Modelo de Linguagem

Os experimentos utilizaram a API da OpenAI com os seguintes parâmetros:

| Parâmetro | Configuração |
|---|---|
| Modelo | GPT-4o mini |
| Temperatura | 0,1 |
| Máximo de tokens de saída | 3.500 |
| Top-p | 0,95 |
| Frequency penalty | 0,1 |
| Presence penalty | 0,1 |
| Timeout | 90 segundos |

A aplicação utiliza a função `generate_code()` para enviar o prompt e recuperar o código produzido pelo modelo.

As respostas geradas são apresentadas na interface web e registradas nos logs para apoiar a análise experimental.

A geração pode apresentar variações entre execuções, mesmo quando são utilizados parâmetros de configuração semelhantes.

## 7. Representação do Conhecimento

Os arquivos YAML estão localizados no diretório `ontologias/`.

Cada arquivo representa informações técnicas de um componente IoT.

### 7.1. Sensor DS18B20

Sensor digital utilizado para medição de temperatura.

Entre as propriedades representadas estão:

| Propriedade | Valor |
|---|---|
| Temperatura mínima | -55 °C |
| Temperatura máxima | 125 °C |
| Resolução | 0,0625 °C |
| Valor de erro | -127 °C |
| Protocolo | 1-Wire |
| Bibliotecas | OneWire e DallasTemperature |
| Framework de testes | AUnit |

### 7.2. Sensor HC-SR04

Sensor ultrassônico utilizado para medição de distância.

Entre as propriedades representadas estão:

| Propriedade | Valor |
|---|---|
| Distância mínima | 2 cm |
| Distância máxima | 400 cm |
| Resolução aproximada | 0,3 cm |
| Timeout | 30.000 µs |
| Pulso Trigger | 10 µs |
| Velocidade do som | 0,0343 cm/µs |
| Framework de testes | AUnit |

As representações também incluem informações sobre pinos de comunicação, interfaces funcionais, inicialização de hardware e restrições de geração.

## 8. Instalação e Execução

### 8.1. Pré-requisitos

- Python 3.11 ou superior;
- Flask;
- PyYAML;
- Biblioteca OpenAI para Python;
- python-dotenv;
- Chave de API da OpenAI.

### 8.2. Clonar o Repositório

```bash
git clone https://github.com/maiconrogerrosario/sbqs2026-iot-test-generation.git

cd sbqs2026-iot-test-generation
```

### 8.3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 8.4. Configurar a API

Crie um arquivo `.env` na raiz do projeto e informe sua chave de API:

```text
OPENAI_API_KEY=sua_chave_api
```

Não publique o arquivo `.env` nem suas credenciais no repositório.

### 8.5. Executar a Versão Baseline

```bash
python app_baseline.py
```

### 8.6. Executar a Versão Orientada por Ontologia

```bash
python app_ontology_guided.py
```

Execute apenas uma versão por vez, pois ambas utilizam a mesma porta local.

Após iniciar a aplicação, acesse:

```text
http://127.0.0.1:5000
```

## 9. Artefatos Experimentais

Os artefatos dos experimentos estão disponíveis no diretório:

`experiments/`

A organização separa os resultados das duas condições experimentais:

**`baseline/`**

Contém prompts genéricos, códigos gerados e logs da condição sem contexto ontológico.

**`ontology_guided/`**

Contém prompts estruturados, códigos gerados e logs da condição orientada por ontologia.

Cada diretório possui subpastas destinadas aos prompts, aos códigos C++ e aos registros das execuções.

### 9.1. Experimentos Adicionais — 14/10/2026

Foram realizadas novas execuções com os sensores DS18B20 e HC-SR04 em ambas as condições experimentais.

Na condição baseline, o modelo produziu programas destinados à leitura e ao monitoramento dos sensores, sem gerar testes automatizados utilizando AUnit.

Na condição orientada por ontologia, as respostas incluíram estruturas de teste com asserções e parâmetros relacionados às características técnicas dos componentes.

As execuções adicionais produziram cinco blocos de teste para o DS18B20 e quatro para o HC-SR04, embora tenham sido identificadas inconsistências técnicas e funcionais.

Esses experimentos não correspondem necessariamente às mesmas gerações utilizadas na avaliação original apresentada no artigo.

A documentação detalhada está disponível em `experiments/README.md`.

## 10. Reprodutibilidade

Para realizar novas execuções da abordagem:

1. Clone o repositório.
2. Instale as dependências.
3. Configure a chave de API da OpenAI.
4. Execute a versão experimental desejada.
5. Selecione a plataforma Arduino e um dos sensores disponíveis.
6. Configure os parâmetros do componente.
7. Escolha o modo de teste.
8. Solicite a geração do código.
9. Analise o resultado apresentado pela aplicação.

Os arquivos de experimentos permitem examinar as instruções e os códigos produzidos nas execuções documentadas, desde que sejam disponibilizadas as versões integrais dos prompts e as saídas originais do modelo.

A reprodução do procedimento não garante respostas idênticas, considerando a variabilidade dos modelos de linguagem.

## 11. Avaliação e Limitações

A avaliação apresentada no artigo possui caráter qualitativo e exploratório.

A análise concentra-se na correspondência entre o conhecimento técnico dos sensores e os elementos incorporados aos códigos gerados, como constantes, configurações, chamadas de funções e asserções.

Os resultados indicam a viabilidade inicial da utilização de conhecimento estruturado para orientar a geração de artefatos de teste.

Entretanto, foram identificadas limitações:

- Avaliação restrita aos sensores DS18B20 e HC-SR04;
- Geração de código com inconsistências técnicas e funcionais;
- Ausência de compilação e execução sistemática dos testes;
- Ausência de avaliação quantitativa de cobertura e detecção de defeitos;
- Utilização de YAML como representação operacional, sem consultas SPARQL diretas;
- Diferenças entre os prompts das condições experimentais, dificultando isolar exclusivamente o efeito da ontologia.

Consequentemente, os códigos gerados devem ser considerados artefatos preliminares que necessitam de revisão técnica antes de sua utilização em hardware real.

## 12. Tecnologias Utilizadas

- Python;
- Flask;
- PyYAML;
- OpenAI API;
- GPT-4o mini;
- OWL e Protégé (modelagem do conhecimento);
- YAML e JSON (representação operacional);
- Arduino;
- C++;
- AUnit.

## 13. Artigo Científico

**Título:** An Ontology- and LLM-Based Approach for Automatic Test Case Generation in IoT Devices

**Autores:** Maicon Roger do Rosario e André Luís Andrade Menolli.

**Evento:** XXV Simpósio Brasileiro de Qualidade de Software — SBQS 2026.

**Local:** Maringá, Paraná, Brasil.

**Período:** 10 a 13 de novembro de 2026.

O artigo apresenta a arquitetura proposta, a representação do conhecimento, a implementação inicial do protótipo e a avaliação exploratória com sensores IoT.

## 14. Licença e Utilização

Este repositório é disponibilizado para fins acadêmicos, científicos e de pesquisa.

As condições formais de reutilização, modificação e redistribuição deverão observar o arquivo de licença do projeto, caso disponibilizado.

## 15. Considerações Finais

Este repositório disponibiliza uma implementação inicial de uma abordagem que combina conhecimento estruturado derivado de ontologias leves e modelos de linguagem para apoiar a geração automática de casos de teste funcionais na camada de dispositivos IoT.

Os artefatos experimentais permitem examinar o processo de construção dos prompts e os códigos produzidos pelo modelo.

A abordagem demonstra potencial para apoiar desenvolvedores na elaboração inicial de testes destinados à validação da integração entre firmware e componentes físicos, permanecendo necessárias etapas posteriores de verificação, compilação, execução e avaliação sistemática.