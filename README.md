# SBQS 2026 — Geração Automática de Casos de Teste para Dispositivos IoT com Ontologias e LLMs

Este repositório reúne o protótipo e os artefatos experimentais associados ao artigo científico:

**An Ontology- and LLM-Based Approach for Automatic Test Case Generation in IoT Devices**

Artigo aceito no **XXV Simpósio Brasileiro de Qualidade de Software (SBQS 2026)**, realizado em Maringá, Paraná, Brasil, de 10 a 13 de novembro de 2026.

**Autores:** Maicon Roger do Rosario e André Luís Andrade Menolli.

## 1. Visão geral

A pesquisa apresenta uma abordagem para apoiar a geração automática de casos de teste funcionais para a camada de dispositivos da Internet das Coisas (IoT). A proposta combina:

- Ontologias leves para representação do conhecimento;
- Modelos de linguagem de grande porte (LLMs);
- Aplicações Python e Flask para orquestração de prompts;
- Geração de código C++ destinado à plataforma Arduino;
- Framework AUnit como referência para testes automatizados.

O foco é a validação funcional da integração e compatibilidade entre o firmware executado em microcontroladores e componentes físicos, como sensores.

O conhecimento técnico considerado abrange propriedades operacionais, protocolos de comunicação, bibliotecas de software, interfaces funcionais, configurações de hardware e restrições de geração de testes.

## 2. Organização do repositório

A estrutura proposta para esta versão é:

```text
sbqs2026-iot-test-generation/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── app_baseline.py
├── app_ontology_guided.py
├── modelagem/
│   └── iot-device-onto.owl
├── ontologias/
│   ├── DS18B20.yml
│   └── HCSR04.yml
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── plataforma.html
│   ├── formulario.html
│   ├── resultado.html
│   └── index.html
└── experimentos/
    ├── README.md
    ├── sem_ontologia/
    │   ├── prompts/
    │   ├── codigos_gerados/
    │   └── logs/
    └── com_ontologia/
        ├── prompts/
        ├── codigos_gerados/
        └── logs/
```

**Observação:** esta árvore representa a organização pretendida. Antes de publicar esta versão do README, confira se todos os caminhos e arquivos indicados existem de fato no repositório. Diretórios ainda não criados não devem ser apresentados como materiais disponíveis.

## 3. Representação do conhecimento

### 3.1. Modelagem conceitual em OWL

A pasta `modelagem/` contém o arquivo `iot-device-onto.owl`, desenvolvido no Protégé.

A ontologia representa conceitos e relações relevantes para a camada de dispositivos IoT, incluindo:

- Dispositivos, sensores e atuadores;
- Microcontroladores e pinos;
- Grandezas e unidades de medida;
- Protocolos de comunicação;
- Bibliotecas de software e de testes;
- Características operacionais;
- Condições de erro.

A versão incluída neste repositório descreve, entre outros elementos, os sensores DS18B20 e HC-SR04 e instâncias com parâmetros técnicos associados.

### 3.2. Representação operacional em YAML

A pasta `ontologias/` contém os arquivos `DS18B20.yml` e `HCSR04.yml`.

Esses arquivos organizam o conhecimento técnico usado durante a execução das aplicações Flask. Além de conceitos derivados da modelagem ontológica, incluem elementos específicos de implementação e geração de testes, como bibliotecas, métodos, constantes, pinos e restrições de código.

**Distinção importante:** o protótipo experimental não consulta diretamente a ontologia OWL e não executa consultas SPARQL. Os arquivos YAML constituem a fonte operacional de conhecimento incorporada aos prompts. Não há sincronização automática entre os arquivos OWL e YAML.

A ontologia OWL é disponibilizada para documentar a modelagem conceitual da pesquisa. Caso o arquivo seja uma revisão posterior à realização dos experimentos originais, essa diferença deve ser registrada no histórico do repositório.

## 4. Arquitetura da abordagem

A implementação compreende quatro partes:

**Apresentação:** interface web para escolha do sensor, definição de parâmetros e visualização do código gerado.

**Representação do conhecimento:** arquivos YAML com as informações técnicas e operacionais dos componentes IoT.

**Orquestração:** construção das instruções encaminhadas ao modelo de linguagem a partir da tarefa solicitada, dos parâmetros do usuário e do conhecimento estruturado.

**Geração por IA:** chamada à API do modelo de linguagem para produzir código destinado ao Arduino.

O fluxo principal pode ser representado por:

```text
Interface Web (Flask)
        |
        v
Seleção do Sensor e dos Parâmetros
        |
        v
Carregamento do YAML
        |
        v
Construção do Prompt
        |
        v
Modelo de Linguagem
        |
        v
Código C++ Gerado
        |
        v
Apresentação do Resultado
```

O protótipo **gera código**, mas não realiza automaticamente sua compilação nem a execução dos testes em hardware físico.

## 5. Condições experimentais

Foram utilizadas duas configurações para uma comparação qualitativa e exploratória.

### 5.1. Condição sem contexto ontológico

**Aplicação:** `app_baseline.py`  
**Diretório:** `experimentos/sem_ontologia/`

Nessa condição, o modelo recebe uma solicitação genérica de geração de testes ou código para um componente IoT, sem incorporar ao prompt o conjunto de propriedades técnicas estruturadas da ontologia.

A aplicação pode utilizar os YAML para a interface e os formulários, mas esse conhecimento não é utilizado como contexto ontológico explícito na solicitação encaminhada ao modelo.

Essa condição funciona como referência exploratória para observar as saídas obtidas sem o enriquecimento estrutural do prompt.

### 5.2. Condição orientada por conhecimento ontológico

**Aplicação:** `app_ontology_guided.py`  
**Diretório:** `experimentos/com_ontologia/`

Nessa condição, o prompt incorpora informações estruturadas dos YAML, como:

- Hierarquias de classes e mapeamentos ontológicos;
- Propriedades de objeto e propriedades de dados;
- Limites de medição, resolução e valores de erro;
- Protocolos de comunicação;
- Bibliotecas de software e testes;
- Configurações de hardware e pinos;
- Interfaces funcionais;
- Restrições para geração de código.

**Limitação da comparação:** as condições diferem no volume de contexto e em suas instruções. Assim, os resultados não permitem atribuir exclusivamente à presença da ontologia todas as diferenças observadas.

## 6. Construção dos prompts

A construção das instruções é realizada pela função `build_prompt()` nas aplicações experimentais.

Na condição orientada por ontologia, o prompt reúne o contexto da tarefa, os parâmetros selecionados, o modo de execução, as instruções de geração e o conhecimento estruturado extraído do YAML.

A representação operacional é incorporada ao prompt em formato estruturado, incluindo JSON.

```text
Contexto da Tarefa
        |
        v
Parâmetros do Usuário
        |
        v
Modo de Execução
        |
        v
Instruções de Geração
        |
        v
Conhecimento Estruturado
        |
        v
Modelo de Linguagem
```

O modelo recebe instruções para produzir código direcionado à plataforma Arduino. A qualidade e a validade técnica das saídas dependem de revisão posterior.

## 7. Modelo de linguagem

A implementação experimental utiliza a API da OpenAI com o modelo **GPT-4o mini**.

As configurações documentadas no projeto incluem:

| Parâmetro | Configuração |
|---|---|
| Modelo | GPT-4o mini |
| Temperatura | 0,1 |
| Máximo de tokens de saída | 3.500 |
| Top-p | 0,95 |
| Frequency penalty | 0,1 |
| Presence penalty | 0,1 |
| Timeout | 90 segundos |

Esses valores devem ser conferidos nas chamadas atuais ao SDK antes da publicação de uma versão definitiva do repositório.

A utilização da API requer credenciais próprias e pode gerar custos. Execuções posteriores não necessariamente retornam as mesmas saídas, mesmo quando os parâmetros são mantidos.

## 8. Componentes IoT estudados

### 8.1. Sensor DS18B20

Sensor digital de temperatura com comunicação 1-Wire.

| Propriedade | Valor |
|---|---|
| Temperatura mínima | −55 °C |
| Temperatura máxima | 125 °C |
| Resolução | 0,0625 °C |
| Valor de erro | −127 °C |
| Protocolo | 1-Wire |
| Bibliotecas de produção | OneWire e DallasTemperature |
| Biblioteca de testes | AUnit |

O arquivo YAML também contém definições sobre pinos, inicialização, interfaces funcionais e regras de geração.

### 8.2. Sensor HC-SR04

Sensor ultrassônico destinado à medição de distância.

| Propriedade | Valor |
|---|---|
| Distância mínima | 2 cm |
| Distância máxima | 400 cm |
| Resolução aproximada | 0,3 cm |
| Timeout | 30.000 µs |
| Pulso Trigger | 10 µs |
| Velocidade do som | 0,0343 cm/µs |
| Biblioteca de testes | AUnit |

O YAML documenta ainda os pinos Trigger e Echo, os métodos empregados nas medições e as restrições para geração do código.

## 9. Instalação e execução

### 9.1. Pré-requisitos

- Python 3.11 ou superior;
- Dependências listadas em `requirements.txt`;
- Chave de API válida da OpenAI;
- Acesso à internet para as chamadas ao modelo.

O arquivo `requirements.txt` precisa estar disponível no repositório para que o procedimento abaixo seja utilizado.

### 9.2. Clonar o repositório

```bash
git clone https://github.com/maiconrogerrosario/sbqs2026-iot-test-generation.git
cd sbqs2026-iot-test-generation
```

### 9.3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 9.4. Configurar as credenciais

Crie um arquivo `.env` na raiz do projeto, tomando como referência `.env.example`:

```dotenv
OPENAI_API_KEY=sua_chave_api
```

Não compartilhe a chave real, nem publique o arquivo `.env`.

### 9.5. Executar a condição sem contexto ontológico

```bash
python app_baseline.py
```

### 9.6. Executar a condição orientada por ontologia

```bash
python app_ontology_guided.py
```

Execute uma aplicação por vez caso ambas utilizem a mesma porta local.

Acesse no navegador:

```text
http://127.0.0.1:5000
```

### 9.7. Procedimento básico de uso

1. Inicie a aplicação desejada.
2. Selecione a plataforma e um dos sensores disponíveis.
3. Informe ou revise os parâmetros apresentados no formulário.
4. Escolha o modo de teste, quando disponível.
5. Solicite a geração do código.
6. Examine a saída retornada na interface.

A geração de código não comprova, isoladamente, sua compilação, execução ou correção funcional.

## 10. Materiais experimentais

A pasta `experimentos/` organiza os materiais associados às duas condições da investigação.

A estrutura prevista separa:

- `prompts/`: instruções submetidas ao modelo;
- `codigos_gerados/`: códigos retornados pelo modelo;
- `logs/`: registros associados às execuções.

Os resultados devem ser identificados por sensor, condição experimental e data de execução, quando essas informações estiverem disponíveis.

### 10.1. Execuções adicionais de 14/10/2026

Foram realizadas novas execuções com os sensores DS18B20 e HC-SR04 nas duas condições experimentais.

Na condição sem contexto ontológico, as saídas incluíram programas de leitura e monitoramento dos sensores, sem estrutura de testes automatizados utilizando AUnit.

Na condição orientada por ontologia, foram produzidos códigos com estruturas de teste, asserções e parâmetros relacionados às características dos componentes. Foram observados cinco blocos de teste para o DS18B20 e quatro para o HC-SR04, além de inconsistências técnicas e funcionais.

**Essas execuções adicionais não reproduzem necessariamente as saídas originais analisadas no artigo.** Os materiais posteriores devem permanecer identificados separadamente e não podem ser apresentados como reprodução exata dos resultados históricos.

Para detalhes de cada execução, consulte `experimentos/README.md`, caso esse arquivo tenha sido disponibilizado.

## 11. Reprodutibilidade e limitações

A pesquisa apresenta uma avaliação qualitativa e exploratória, centrada na correspondência entre conhecimento técnico dos componentes e elementos incorporados ao código gerado.

Entre as limitações identificadas estão:

- Escopo experimental restrito aos sensores DS18B20 e HC-SR04;
- Possibilidade de inconsistências técnicas e funcionais no código gerado;
- Ausência de compilação e execução sistemática dos testes;
- Ausência de avaliação quantitativa de cobertura de código e detecção de defeitos;
- Utilização de YAML na aplicação, sem consulta direta a OWL/SPARQL;
- Diferenças entre as instruções das condições comparadas;
- Variabilidade das respostas produzidas pelo modelo de linguagem;
- Indisponibilidade de parte das saídas históricas originais, quando aplicável.

A reprodução do procedimento de geração **não garante a reprodução literal dos códigos ou resultados qualitativos apresentados no artigo**.

Os programas produzidos pelo modelo devem ser revisados antes de serem compilados ou executados em hardware real.

## 12. Tecnologias utilizadas

- Python e Flask;
- PyYAML;
- OpenAI API e GPT-4o mini;
- OWL e Protégé;
- YAML e JSON;
- Arduino e C++;
- AUnit.

## 13. Artigo científico

**Título:** An Ontology- and LLM-Based Approach for Automatic Test Case Generation in IoT Devices  
**Autores:** Maicon Roger do Rosario e André Luís Andrade Menolli  
**Evento:** XXV Simpósio Brasileiro de Qualidade de Software (SBQS 2026)  
**Local:** Maringá, Paraná, Brasil  
**Período:** 10 a 13 de novembro de 2026

O artigo apresenta a arquitetura da abordagem, a modelagem do conhecimento, a implementação inicial do protótipo e a avaliação exploratória.

## 14. Disponibilidade do código e dos experimentos

O código-fonte, a modelagem ontológica, as representações operacionais e os materiais experimentais disponibilizados neste projeto podem ser consultados no repositório:

**https://github.com/maiconrogerrosario/sbqs2026-iot-test-generation**

O repositório destina-se à documentação, inspeção e continuidade da pesquisa. O material disponível poderá ser atualizado ao longo do desenvolvimento, com registro das alterações pelo histórico do Git.

Este repositório não afirma reproduzir integralmente as saídas históricas originais do artigo.

## 15. Licença e direitos autorais

Copyright (C) 2026 The Authors.

A disponibilização pública dos arquivos não concede automaticamente autorização irrestrita para sua modificação, redistribuição ou exploração comercial.

As permissões de reutilização deverão seguir a licença efetivamente adotada pelos titulares dos direitos autorais. Na ausência de licença explícita, não se deve presumir uma autorização geral de reutilização.

## 16. Considerações finais

Este repositório documenta uma implementação experimental que utiliza conhecimento estruturado, derivado de uma ontologia leve, para orientar modelos de linguagem na geração de casos de teste funcionais para dispositivos IoT.

A abordagem oferece uma base inicial para estudar o apoio de LLMs à atividade de testes de firmware. Permanecem necessárias avaliações posteriores envolvendo compilação, execução, detecção de defeitos e integração automatizada com ambientes de teste.
