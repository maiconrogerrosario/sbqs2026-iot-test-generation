````markdown
# SBQS 2026 – Ontology and LLM-based Automatic Test Generation for IoT Devices

This repository contains the implementation and experimental artifacts associated with the paper:

> **Uma Abordagem Baseada em Ontologias e LLMs para Geração Automática de Casos de Teste em Dispositivos IoT**

submitted to the **XXV Simpósio Brasileiro de Qualidade de Software (SBQS 2026)**.

---

# Overview

The objective of this work is to support the automatic generation of functional test cases for IoT device firmware by combining:

- Lightweight Ontologies (YAML)
- Large Language Models (LLMs)
- Flask-based orchestration
- Arduino/C++ test generation

The ontology provides structured knowledge about IoT devices, including hardware characteristics, software libraries, communication protocols, measurement constraints and testing rules. This information is incorporated into a structured prompt that guides the language model during code generation.

---

# Repository Structure

```
.
├── app.py                 # Main Flask application
├── ontologias/            # Lightweight ontologies (YAML)
├── templates/             # HTML pages
├── requirements.txt
├── .env.example
└── README.md
```

---

# Main Workflow

The execution pipeline is composed of the following steps:

1. User selects an IoT sensor.
2. The corresponding ontology is loaded.
3. The application dynamically builds the web form.
4. User fills the test configuration.
5. The application constructs the prompt.
6. The prompt is sent to the OpenAI model.
7. The generated Arduino/C++ test code is returned to the user.

---

# Prompt Construction

One of the main contributions of this work is the prompt orchestration strategy.

The prompt is dynamically generated inside the function:

```
app.py
└── build_prompt()
```

This function combines four information sources:

- Context of the requested task;
- User-defined parameters;
- Test execution mode;
- Complete ontology serialized as JSON.

The generated prompt follows the structure:

```
Context
↓

User Parameters
↓

Execution Mode
↓

Mandatory Instructions
↓

Ontology (JSON)
```

The ontology is considered the **single source of knowledge** used by the language model.

---

# Prompt Logging

For reproducibility purposes, every generated prompt is automatically recorded before the API request.

The application prints the prompt in the terminal using the logger:

```
================================================================================
📝 PROMPT ENVIADO:
================================================================================
```

Therefore, reviewers can inspect the exact prompt used during each experiment.

---

# OpenAI API Call

The generated prompt is submitted to the OpenAI API by the function:

```
generate_code()
```

located in

```
app.py
```

The current implementation uses:

- GPT-4o Mini
- Temperature = 0.1
- max_tokens = 3500

The generated source code is also logged before being returned to the web interface.

---

# Ontologies

All ontologies are located inside

```
ontologias/
```

Each ontology describes a specific IoT device.

Example:

```
ontologias/
├── DS18B20.yaml
├── HCSR04.yaml
```

Each ontology contains information such as:

- class hierarchy
- object properties
- data properties
- functional interface
- hardware initialization
- software libraries
- testing framework
- validation constraints

---

# Supported Sensors

Current implementation includes:

- DS18B20
- HC-SR04

New sensors can be added by simply creating new ontology files.

---

# Running the Project

## Requirements

- Python 3.11+
- Flask
- PyYAML
- OpenAI SDK
- python-dotenv

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key
```

---

# Execute

Run:

```bash
python app.py
```

Open:

```
http://localhost:5000
```

---

# Main Source Code

| Component | File |
|------------|------|
| Flask application | app.py |
| Ontology loader | load_ontologies() |
| Dynamic form generation | build_form_fields() |
| Prompt construction | build_prompt() |
| OpenAI communication | generate_code() |
| HTML pages | templates/ |
| Ontologies | ontologias/ |

---

# Reproducibility

To reproduce the experiments:

1. Clone this repository.
2. Install the required packages.
3. Configure the OpenAI API key.
4. Execute the Flask application.
5. Select one of the available sensors.
6. Generate the prompt.
7. Inspect the generated prompt in the terminal logs.
8. Inspect the generated Arduino/C++ test code.

---

# Technologies

- Python
- Flask
- OpenAI API
- YAML
- Arduino
- C++
- Lightweight Ontologies

---

# Citation

If you use this repository in your research, please cite the corresponding SBQS 2026 paper.

---

# License

This repository is provided for academic and research purposes.
````

