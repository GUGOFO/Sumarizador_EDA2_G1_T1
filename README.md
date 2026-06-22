# Sumarizador_EDA2_G1_T1

Trabalho Final apresentado à disciplina de **Estruturas de Dados 2 (EDA 2)** **Universidade de Brasília (UnB) – Campus Gama (FCTE)** **Grupo 1** | Turma: T01 

##  Integrantes do Grupo

| Nome | Matrícula |
| :--- | :---: |
| Gustavo Gomes Fornaciari | 241032519 |
| Ana Beatriz Souza Araujo | 241025891 |
| Gabriel Mota Oliveira | 241011081 |
| Matheus Pinheiro | 241025336 |
| Gabriel Alves de Araujo | 241025523 |

---

## 1. Descrição do Problema

Este projeto resolve um problema muito comum e real no nosso dia a dia, unindo **Processamento de Linguagem Natural (PLN)** e a **Defesa do Consumidor**: a dificuldade prática de ler e entender Termos de Serviço e Políticas de Privacidade digitais. Por serem textos longos, cansativos e repletos de "juridiquês", a grande maioria das pessoas aceita esses contratos sem ter a menor ideia das obrigações ou das armadilhas que estão escondidas ali.

A proposta do nosso sistema é automatizar esse processo por meio de **sumarização extrativa**. O programa analisa o texto do contrato, calcula a relevância estatística de cada frase e extrai as cláusulas realmente críticas, gerando um relatório limpo e direto no terminal para o usuário.

---

## 2. Qualidade e Coerência dos Dados

Para validar a nossa solução, usamos contratos reais e extensos que exigem bastante do algoritmo. Os arquivos de teste ficam na pasta `inputs/` e incluem:
* **`youtube.txt`**: Os Termos de Serviço completos do YouTube.
* **`instagram.txt`**: Os Termos de Uso atualizados do Instagram.
* **`twitter.txt`**: As condições gerais e termos da plataforma Twitter (agora X).

Essas bases de dados possuem centenas de sentenças complexas, trechos inteiros em caixa alta (como as isenções de responsabilidade jurídica) e repetições de conceitos importantes em diferentes seções. Isso serviu perfeitamente para testar o desempenho e o estresse das nossas estruturas de dados.

---

## 3. Engenharia de Estruturas de Dados Próprias 

Seguindo a regra do trabalho de não usar bibliotecas prontas (como *NetworkX, Pandas ou coleções prontas do Python*), **todas as estruturas fundamentais do projeto foram implementadas do zero pela nossa equipe**:

* **O Grafo de Sentenças (`graph.py`):** Representado por uma **Matriz de Adjacência dinâmica**. Cada frase vira um nó (com ID e score PageRank), conectado a outro (aresta) se compartilharem **pelo menos 2 palavras relevantes em comum**.
* **A HashTable com Encadeamento (`hash_table.py`):** Armazena e conta a frequência de palavras por frase. O tratamento de colisões usa **Lista Ligada Simples**, inserindo novos nós de maneira eficiente no início da cadeia daquela posição.
* **A Árvore Rubro-Negra Esquerdista (`rne.py`):** Organiza o ranking final das frases por meio de um balanceamento perfeito (com rotações e inversão de cores). Se houver empate nos scores de PageRank, usa de forma estável o ID numérico dos vértices como critério de desempate.

---

## 4. Algoritmos de Processamento e Grafos

O pipeline do nosso sistema funciona em três etapas bem definidas:

```text
 [Texto Bruto] ➔ [spaCy (PLN/Lemas)] ➔ [HashTable por Frase]
                                                │
                                                ▼
 [Árvore RNE Ordenada] ◀ [PageRank Ponderado] ◀ [Matriz TextRank]
           │
           ▼
 [Painel de Resumo CLI]
```

## 1. Extração e Filtro de PLN (`processor.py`)
O texto bruto passa pelo motor do `spaCy` (`pt_core_news_sm`) para ser segmentado em frases reais. O filtro limpa pontuações, espaços e *stop words* (como artigos e preposições), e aplica a **lematização** (reduzindo palavras como "reivindicaram" e "reivindicações" para a raiz "reivindicação") com normalização em caixa baixa (`.lower()`).

### 2. Ponderação TextRank (`textrank.py`)
Para cada par de frases $(i, j)$, cruzamos os dados de uma HashTable com a busca da outra. Se houver interseção ($\ge 2$ palavras em comum), calculamos o peso da aresta aplicando uma **penalidade de tamanho** (`length_penalty`). Isso impede que frases gigantescas dominem o grafo injustamente apenas por terem mais palavras:
$$\text{weight} = \frac{\text{comuns}}{\text{total}_a + \text{total}_b - \text{comuns}} \times \frac{\min(\text{total}_a, \text{total}_b)}{\max(\text{total}_a, \text{total}_b)}$$

### 3. PageRank Ponderado (`pagerank.py`)
O algoritmo calcula a importância de cada frase de forma iterativa. Ele trata de forma rigorosa as frases sem saída (**dangling mass**), distribuindo essa perda de massa de maneira síncrona e equilibrada entre todos os nós a cada iteração. O cálculo para de rodar assim que a variação máxima entre as rodadas fica abaixo da nossa meta de convergência (`tolerancia=1e-6`).

---

## 5. Análise e Interpretação dos Resultados

Nosso software oferece **dois métodos estatísticos** para o usuário escolher como deseja filtrar o resumo final:

1. **Seleção por Corte Percentual Dinâmico (`--porcentagem`):** Filtra os top $X\%$ nós de maior autoridade no grafo, separando e destacando visualmente a **Cláusula Soberana (1º Lugar)** em uma moldura especial no terminal.
2. **Seleção por Critério Estatístico (`--k`):** Exibe apenas as sentenças que estão na curva mais alta de relevância da distribuição do contrato. O corte é feito de forma puramente matemática onde:
$$\text{Score PR} > \text{Média} + (k \times \text{Desvio Padrão})$$

No fim de cada execução, o painel exibe a **Taxa de Compressão de Leitura**, mostrando em porcentagem o quanto de texto redundante foi poupado para o usuário.

---

## 6. Arquitetura do Repositório

```text
├── inputs/                           # Contratos reais para testes do professor
│   ├── instagram.txt                 # Termos do Instagram
│   ├── twitter.txt                   # Termos do Twitter / X
│   └── youtube.txt                   # Termos do YouTube
│
├── src/
│   ├── __init__.py
│   │
│   ├── structures/                   # Nossas estruturas de dados (Feitas à mão)
│   │   ├── __init__.py
│   │   ├── hash_table.py             # HashTable manual com lista encadeada
│   │   ├── graph.py                  # Grafo baseado em Matriz de Adjacência
│   │   └── rne.py                    # Árvore Rubro-Negra de ordenação
│   │
│   ├── nlp/                          # Módulos de PLN
│   │   ├── __init__.py
│   │   └── processor.py              # Processamento e lematização com spaCy
│   │
│   ├── algorithms/                   # Motores e lógica matemática
│   │   ├── __init__.py
│   │   ├── textrank.py               # Lógica de pesos e similaridade
│   │   └── pagerank.py               # PageRank iterativo com tratamento de dangling
│   │
│   └── main.py                       # Ponto de entrada (CLI, argumentos e painel)
│
├── requirements.txt                  # Dependências ( spaCy e rich de interface )
├── setup.sh                          # Setup automatizado para Linux/macOS
├── setup.bat                         # Setup automatizado para Windows
└── README.md                         # Documentação do projeto
```

## 7. Como Configurar e Executar o Projeto

Para garantir que o ambiente rode perfeitamente sem quebrar caminhos e pacotes, utilize os scripts automatizados fornecidos.

### 1. Configuração Inicial

Execute o script correspondente ao seu sistema operacional para criar o ambiente virtual, atualizar os gerenciadores e baixar o modelo de português do spaCy automaticamente:

* **No Windows:**

```text
    setup.bat
```

* **No Linux / macOS:**

```text
    chmod +x setup.sh
    ./setup.sh
```

### 2. Ativação Obrigatória do Ambiente Virtual

* **No Windows:**

```text
    venv\Scripts\activate
```

* **No Linux / macOS:**

```text
    source venv/bin/activate
```

O terminal vai mostrar um prefixo (venv) no começo da linha, indicando que deu certo


### 3. Executando via CLI

Com a venv ativa, execute o main.py passando os argumentos que desejar para os testes

* Execução básica (Usa o corte padrão de 20% do texto)
```text
python src/main.py --arquivo youtube.txt
```

* Mudando a Porcentagem Dinâmica (Extrai os 10% mais importantes do texto)
```text
python src/main.py --arquivo instagram.txt --porcentagem 10
```

* Filtrando por Critério Estatístico (Score > Média + 1.5 * Desvio Padrão)
```text
python src/main.py --arquivo twitter.txt --k 1.5
```

## 8. Uso de LLM no Desenvolvimento

Conforme o Critério 6 do trabalho, declara-se que modelos de linguagem de grande escala (LLMs) foram utilizados de forma assistiva durante o desenvolvimento deste trabalho para as seguintes atividades:

* Estruturação de tipagem estática informativa em trechos críticos das estruturas de dados para acelerar o processo de depuração de ponteiros em Python.

* Formatação do plano arquitetural e documentação técnica descrita neste arquivo.