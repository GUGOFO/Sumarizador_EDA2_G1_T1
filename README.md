# Sumarizador_EDA2_G1_T1

## Visão Geral do Projeto
Este projeto foi desenvolvido como trabalho final para a disciplina de **Estruturas de Dados 2 (EDA 2)** da Universidade de Brasília (UnB), campus Gama (FCTE). 

O sistema aborda um problema real na área de **Defesa do Consumidor**: a dificuldade de ler e extrair cláusulas críticas em Termos de Serviço, Políticas de Privacidade e contratos de adesão longos, cansativos e repletos de "juridiquês". Utilizando técnicas de **Processamento de Linguagem Natural (PLN)** e **Algoritmos em Grafos**, a aplicação transforma o texto em uma rede interconectada de conceitos e aplica o algoritmo **PageRank** para classificar e retornar as frases estatisticamente mais relevantes (cláusulas críticas) diretamente no terminal.

---

## Requisitos e Escopo Técnico

Para cumprir rigorosamente as diretrizes e penalidades do edital da disciplina, o projeto foi arquitetado sob as seguintes regras:
* **Linguagem Principal:** Python 3.
* **Dependência Externa Permitida:** Apenas a biblioteca `spaCy` para quebra de sentenças, remoção de *stop words* e lematização.
* **Estruturas de Dados Próprias (100% implementadas à mão):** Proibido o uso de estruturas prontas do Python para a lógica principal do grafo e ordenação.
* **Interface:** Execução puramente via terminal (CLI) aceitando argumentos dinâmicos.
* **Prazo Final de Entrega:** Repositório atualizado até **22/06/2026**.

---

## Modelagem e Solução

### 1. Processamento de Texto (PLN)
O texto bruto de entrada (`.txt`) passa pelo motor do `spaCy` (`pt_core_news_sm`), onde:
* O texto é segmentado em frases reais.
* Aplica-se `.lower()` em todos os caracteres.
* Filtram-se pontuações, números isolados e *stop words* (artigos, preposições, etc.).
* É feita a **lematização** (redução das palavras à sua forma canônica, ex: "obrigações" vira "obrigação"), garantindo precisão milimétrica na contagem de termos equivalentes.

### 2. Modelagem do Grafo
O problema é mapeado como um **Grafo Valorado Não-Direcionado**:
* **Vértices (Nós):** Cada frase limpa extraída do texto representa um vértice único.
* **Arestas (Conexões):** Uma aresta liga duas frases se elas compartilham pelo menos uma palavra em comum (após o filtro de PLN).
* **Peso:** O peso da aresta corresponde à quantidade exata de palavras idênticas compartilhadas pelas duas frases (similaridade textual).

### 3. Validação de Conectividade
Antes de calcular a relevância, uma **Fila (Queue)** e uma **Pilha (Stack)** implementadas manualmente realizam uma busca em largura (BFS) para analisar a densidade e garantir que o algoritmo trafegue corretamente por componentes conexos do grafo.

### 4. Algoritmo PageRank e Desempate por Árvore
O algoritmo calcula de forma iterativa a centralidade e importância de cada frase com base nos pesos das suas conexões. Em cenários de convergência com scores idênticos (empates no ranking das frases), o sistema faz o desempate inserindo os nós em uma **Árvore Rubro-Negra Esquerdista (Left-Leaning Red-Black Tree)** desenvolvida do zero, ordenando os critérios por ID e garantindo a estabilidade do ranking.

---

## Arquitetura do Repositório

O projeto segue uma estrutura estritamente modularizada para separar a lógica de negócio das estruturas de dados brutas:

```text
├── inputs/                           # Arquivos de texto (.txt) para testes do professor
│   └── youtube.txt                   # Exemplo de Termo de Serviço do YouTube
│
├── src/
│   ├── __init__.py
│   │
│   ├── structures/                   # Estruturas de dados feitas estritamente na mão
│   │   ├── __init__.py
│   │   ├── linear.py                 # Implementação de Pilha e Fila manuais
│   │   ├── hash_table.py             # Tabela Hash com tratamento de colisão por encadeamento
│   │   ├── graph.py                  # Grafo Não-Direcionado com Lista de Adjacência própria
│   │   └── rne.py                    # Árvore Rubro-Negra Esquerdista (LLRB Tree)
│   │
│   ├── nlp/                          # Filtros e tratamento de texto
│   │   ├── __init__.py
│   │   └── processor.py              # Integração controlada com spaCy
│   │
│   ├── algorithms/                   # Lógica matemática e centralidade
│   │   ├── __init__.py
│   │   ├── textrank.py               # Lógica de ponderação de arestas
│   │   └── pagerank.py               # Algoritmo de ranqueamento textual iterativo
│   │
│   └── main.py                       # Ponto de entrada da aplicação (CLI Argparse)
│
├── requirements.txt                  # Dependências de pacotes (Apenas spaCy)
├── setup.sh                          # Script de automação e ambiente virtual (Linux/macOS)
├── setup.bat                         # Script de automação e ambiente virtual (Windows)
└── README.md                         # Documentação oficial do projeto
```

## Como Executar o Projeto

Para garantir que o ambiente rode perfeitamente sem quebrar caminhos e pacotes, utilize os scripts automatizados fornecidos.

### 1. Configuração Automática do Ambiente

Abra o terminal na raiz do projeto e execute o script correspondente ao seu sistema operacional para criar o Ambiente Virtual (venv), instalar as dependências e baixar o modelo de linguagem:

* **No Windows:**

```text
    setup.bat
```

* **No Linux / macOS:**

```text
    chmod +x setup.sh
    ./setup.sh
```

### 2. Rodando a Aplicação via CLI

Com o ambiente ativado, execute o arquivo main.py passando o nome do arquivo de texto alvo. O arquivo deve estar localizado obrigatoriamente dentro da pasta inputs/.


```text
    # Executar a análise com o corte padrão de 20% do texto
    python src/main.py --arquivo youtube.txt

    # Executar extraindo apenas os 10% mais importantes do contrato
    python src/main.py --arquivo youtube.txt --porcentagem 10

    # Executar extraindo um resumo mais robusto de 35% do documento
    python src/main.py --arquivo youtube.txt --porcentagem 35
```

## Uso de LLM no Desenvolvimento

Conforme o Critério 6 do edital, declara-se que modelos de linguagem de grande escala (LLMs) foram utilizados de forma assistiva durante o desenvolvimento deste trabalho para as seguintes atividades:

* Estruturação de tipagem estática informativa em trechos críticos das estruturas de dados para acelerar o processo de depuração de ponteiros em Python.

* Formatação do plano arquitetural e documentação técnica descrita neste arquivo.