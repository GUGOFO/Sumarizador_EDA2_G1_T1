#__________________________________________________________________________
#               EXEMPLO PARA TESTE
#__________________________________________________________________________

import spacy

nlp = spacy.load("pt_core_news_sm")

# Texto exemplo
doc = nlp("1. A Ana extrai as frases e limpa as palavras com spaCy. 2. O gΔbriel A. compara as palavras das frases e define o peso de cada ligação (aresta). 3. O Matheus fornece a HashTable e o Grafo para salvar essas frases e essas ligações na memória. 4. O Gabriel Moto Moto roda a fórmula do PageRank nesse grafo e descobre a pontuação (peso) de cada frase. 5. Você pega essas pontuações, joga dentro da sua Árvore Rubro-Negra Esquerdista para ordenar e resolver qualquer empate perfeitamente. 6. A Ana puxa os nós ordenados da sua árvore e exibe o resumo bonitinho na tela do professor.")

# palavras que descartei vao estar vermelhas e escolhidas para contagem(vao pra hash) em verde
VERMELHO = "\033[31m"
VERDE = "\033[32m"
RESET = "\033[0m"

# print de teste do parse do spacy
for sentenca in doc.sents:          # cada sentença
    for token in sentenca:          # cada palavra
        texto = f"palavra = {token.text} | Lema = {token.lemma_} | Stopword = {token.is_stop} | Pontuação = {token.is_punct}"
        if token.is_stop or token.is_punct:
            print(f"{VERMELHO}{texto}{RESET}")
        else:
            print(f"{VERDE}{texto}{RESET}")

#__________________________________________________________________________
#                  Hash Table (Contagem de palavras)
#__________________________________________________________________________


# Nó da lista encadeada usado para tratar colisões na tabela hash
class No:
    def __init__(self, chave, contagem=1):
        self.chave = chave        # a palavra armazenada no nó
        self.contagem = contagem  # quantas vezes a palavra apareceu
        self.proximo = None       # "aponta" para o proximo da linked list, preciso trocar pra RNE ainda

#--------------------------------------------------------------------------

class TabelaHash:
    def __init__(self, tamanho=101):   # não sei se precisa ser muito maior, é so para palavras e não frases e se for maior a RNE vai perder o sentido
        self.tamanho = tamanho
        self.tabela = [None] * tamanho  # lista de linkedlists na hash tabble inicializada com None

    def _hash(self, chave): # Função de dispersão
        h = 0
        for c in chave:
            h = (h * 31 + ord(c)) % self.tamanho
        return h

    def inserir(self, chave):   # adiciona palavra na hash ou aumenta contagem
        idx = self._hash(chave)        # calcula índice da linkedlists na hash tabble
        no_atual = self.tabela[idx]    # obtém o cabeçalho da cadeia

        # Percorre a cadeia procurando um nó com a mesma chave
        while no_atual is not None:
            if no_atual.chave == chave:
                no_atual.contagem += 1  # se existir, incrementa a contagem
                return
            no_atual = no_atual.proximo # percorre a linked list

        # (se a palavra ainda nao existir na hashtabble) resolve colisão por linkedlist, falta juntar com a RNE
        novo = No(chave)
        novo.proximo = self.tabela[idx] 
        self.tabela[idx] = novo

    def buscar(self, chave):    # retorna quantas vezes a palavra aparece na hash
        idx = self._hash(chave)        # calcula índice da linkedlists na hash tabble
        no_atual = self.tabela[idx]

        # Percorre a linked list ate achar a chave
        while no_atual is not None:
            if no_atual.chave == chave:
                return no_atual.contagem  # retorna a contagem encontrada
            no_atual = no_atual.proximo

        return 0  # retorna 0 se nao achar

    def itens(self):    # retorna todos os itens da hash (palavra e contagem)
        for pos in self.tabela:
            no_atual = pos
            while no_atual is not None:
                yield no_atual.chave, no_atual.contagem
                no_atual = no_atual.proximo

    def total_chaves(self): # quantas palavras diferentes estao na hash
        total = 0
        for pos in self.tabela:
            no_atual = pos
            while no_atual is not None:
                total += 1
                no_atual = no_atual.proximo
        return total

#--------------------------------------------------------------------------

def contar_palavras(sentenca_spacy): # vai ser chamada pra cada sentenca pra criar a hash dela
    tabela = TabelaHash()  # cria uma tabela hash para contar palavras

    for token in sentenca_spacy:
        if token.is_stop or token.is_punct or token.is_space:  # remove stopwords, pontuação e espaços
            continue

        palavra = token.lemma_.lower()  # normaliza usando lema em minúsculas
        tabela.inserir(palavra)         # insere ou incrementa a contagem da palavra

    return tabela
#__________________________________________________________________________
#                  Print de teste
#__________________________________________________________________________



# Uso de exemplo: mostra palavra e contagem das palavras não descartadas
for sentenca in doc.sents:
    print(f"Sentença: {sentenca.text}")
    freq = contar_palavras(sentenca)
    for palavra, contagem in freq.itens():
        print(f"{palavra}: {contagem}")

