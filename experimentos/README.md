# Artefatos Experimentais — SBQS 2026

## 1. Visão Geral

Este diretório contém os artefatos experimentais associados ao trabalho **“An Ontology- and LLM-Based Approach for Automatic Test Case Generation in IoT Devices”**, aceito no Simpósio Brasileiro de Qualidade de Software (SBQS 2026).

Os experimentos investigam a utilização de conhecimento estruturado, derivado de ontologias leves, para orientar modelos de linguagem de grande porte (LLMs) na geração automática de casos de teste funcionais para a camada de dispositivos IoT.

Os experimentos disponibilizados neste diretório foram realizados em **14 de outubro de 2026**, como execuções adicionais da abordagem proposta. Eles não representam necessariamente as mesmas saídas utilizadas na avaliação original apresentada no artigo.

## 2. Configuração Experimental

Os experimentos foram realizados considerando a seguinte configuração:

| Parâmetro | Configuração |
|---|---|
| Modelo de linguagem | GPT-4o mini |
| Linguagem de programação | C++ / Arduino |
| Plataforma alvo | Arduino Uno |
| Sensores | DS18B20 e HC-SR04 |
| Temperatura do modelo | 0,1 |
| Limite máximo de saída | 3.500 tokens |
| Framework de testes | AUnit (condição com ontologia) |
| Modo de execução selecionado | Sensor Físico |
| Tipo de avaliação | Qualitativa e exploratória |

Foram consideradas duas condições experimentais.

### 2.1. Geração sem Contexto Ontológico (Baseline)

Nesta condição, o LLM recebe uma instrução genérica solicitando a geração de casos de teste para determinado sensor IoT.

O prompt não contém as propriedades técnicas estruturadas do sensor, suas restrições operacionais, interfaces funcionais ou configurações específicas de teste.

A aplicação utiliza os arquivos YAML para disponibilizar os sensores na interface, mas não incorpora esse conhecimento estruturado ao prompt enviado ao modelo.

**Aplicação:** `app_baseline.py`

### 2.2. Geração Orientada por Ontologia

Nesta condição, o LLM recebe um prompt estruturado contendo conhecimento derivado da ontologia leve, organizado operacionalmente em arquivos YAML.

As informações fornecidas incluem:

- Hierarquia de classes e relações semânticas;
- Propriedades de objeto e de dados;
- Limites operacionais, resolução e valores de erro;
- Configurações de hardware e interfaces de comunicação;
- Dependências de software e bibliotecas de teste;
- Restrições para geração de código e modo de execução.

A camada de orquestração combina essas informações com os parâmetros selecionados pelo usuário e com instruções específicas para orientar a geração dos testes.

**Aplicação:** `app_ontology_guided.py`

## 3. Resultados Experimentais

### 3.1. Sensor de Temperatura DS18B20

**Sem ontologia:** O modelo gerou código Arduino destinado à leitura de temperatura, utilizando as bibliotecas OneWire e DallasTemperature, sem produzir testes automatizados com o framework AUnit.

**Com ontologia:** O modelo produziu cinco blocos de teste utilizando AUnit, relacionados aos seguintes aspectos:

1. Inicialização do sensor;
2. Validação da faixa de temperatura;
3. Verificação do valor de erro;
4. Estabilidade das leituras;
5. Resolução da medição.

Foram identificadas inconsistências em algumas verificações, especialmente na simulação de desconexão do sensor e na implementação do teste de estabilidade.

### 3.2. Sensor Ultrassônico HC-SR04

**Sem ontologia:** O modelo gerou um programa para leitura e classificação de distâncias utilizando a biblioteca NewPing, sem asserções automatizadas com AUnit.

**Com ontologia:** O modelo produziu quatro blocos de teste utilizando AUnit, relacionados aos seguintes aspectos:

1. Validação da faixa de distância;
2. Ausência de eco;
3. Timeout da leitura;
4. Resolução da medição.

O código gerado incorporou parâmetros técnicos do sensor, como os pinos Trigger e Echo, a duração do pulso, o tempo máximo de espera e a velocidade do som.

Entretanto, foram identificadas inconsistências na sintaxe dos testes e na simulação de determinadas condições físicas.

## 4. Organização dos Arquivos

```text
experiments/
├── README.md
├── baseline/
│   ├── prompts/
│   │   ├── DS18B20.txt
│   │   └── HCSR04.txt
│   ├── generated/
│   │   ├── DS18B20.cpp
│   │   └── HCSR04.cpp
│   └── logs/
│       └── execution.log
│
└── ontology_guided/
    ├── prompts/
    │   ├── DS18B20.txt
    │   └── HCSR04.txt
    ├── generated/
    │   ├── DS18B20.cpp
    │   └── HCSR04.cpp
    └── logs/
        └── execution.log
```

Os arquivos estão organizados da seguinte maneira:

- **`prompts/`:** instruções utilizadas para orientar a geração dos casos de teste.
- **`generated/`:** códigos C++ produzidos pelo modelo de linguagem.
- **`logs/`:** registros das execuções experimentais e das respostas recebidas da API.

Para apoiar a reprodutibilidade, recomenda-se disponibilizar os prompts integrais e preservar os códigos exatamente como foram retornados pelo modelo, incluindo eventuais inconsistências.

Os logs públicos devem ser sanitizados para remover informações sensíveis, identificadores de sessão, cookies e dados de depuração desnecessários.

## 5. Avaliação e Limitações

A avaliação possui caráter qualitativo e exploratório, concentrando-se na correspondência entre o conhecimento técnico fornecido ao modelo e os elementos incorporados aos códigos gerados.

Os resultados das execuções adicionais indicam que o fornecimento de contexto estruturado, acompanhado de instruções específicas, pode orientar o LLM na produção de códigos de teste contendo asserções, parâmetros operacionais e configurações relacionadas aos dispositivos IoT.

Entretanto, a comparação não permite isolar exclusivamente a contribuição da ontologia, pois as condições experimentais também diferem quanto à quantidade de contexto e às instruções utilizadas nos prompts.

Além disso, foram observadas limitações importantes:

- A avaliação contemplou apenas dois sensores da plataforma Arduino;
- Os códigos gerados apresentaram inconsistências técnicas e funcionais;
- Não foi realizada compilação ou execução sistemática dos artefatos nestas execuções;
- Não foram avaliadas quantitativamente a cobertura dos testes nem sua capacidade de detectar defeitos;
- O conhecimento utilizado pela implementação foi organizado em arquivos YAML, sem recuperação semântica direta da ontologia OWL por consultas SPARQL.

Dessa forma, os artefatos devem ser considerados estruturas iniciais de teste que necessitam de revisão e validação técnica antes de sua utilização em dispositivos físicos.

## 6. Relação com o Artigo SBQS 2026

Os experimentos apresentados neste diretório constituem **execuções adicionais da abordagem descrita no artigo**, realizadas em 14 de outubro de 2026.

A avaliação original apresentada no artigo possui caráter qualitativo e exploratório, fundamentada na análise da correspondência entre propriedades dos componentes e elementos do código gerado.

As saídas completas de algumas execuções anteriores, utilizadas na elaboração do artigo, não estão mais disponíveis. Portanto, os artefatos aqui publicados não devem ser interpretados como reproduções exatas dessas saídas nem como comprovação direta de todas as contagens e observações relatadas na publicação.

As aplicações, representações YAML, prompts e códigos gerados permitem examinar o funcionamento do protótipo e realizar novas gerações, considerando que modelos de linguagem podem apresentar variações entre execuções.

## 7. Considerações Finais

Os experimentos adicionais evidenciam o potencial da utilização de conhecimento estruturado para apoiar a geração automática de casos de teste funcionais em dispositivos IoT.

A abordagem com contexto ontológico produziu estruturas de teste mais alinhadas às propriedades técnicas dos sensores em comparação com a geração baseada apenas em instruções genéricas.

Entretanto, a presença de propriedades e asserções nos códigos não garante sua correção funcional, sendo necessária a realização de etapas posteriores de compilação, execução e validação.

Os artefatos disponibilizados contribuem para a documentação e a transparência da avaliação exploratória da abordagem, além de fornecerem uma base para futuras investigações sobre geração automatizada de testes utilizando ontologias leves e LLMs.