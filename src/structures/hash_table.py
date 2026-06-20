class No:
    """Nó da lista encadeada usada para tratar colisões na HashTable."""
    def __init__(self, chave, contagem=1):
        self.chave = chave        # a palavra armazenada no nó
        self.contagem = contagem  # quantas vezes a palavra apareceu
        self.proximo = None       # aponta para o próximo nó da cadeia


# --------------------------------------------------------------------------

class HashTable:
    """Tabela hash com encadeamento para contar ocorrências de palavras."""
    def __init__(self, tamanho=101):
        self.tamanho = tamanho
        self.tabela = [None] * tamanho  # lista de cadeias (linked lists)

    def _hash(self, chave):
        """Função de dispersão: converte a chave em um índice da tabela."""
        h = 0
        for c in chave:
            h = (h * 31 + ord(c)) % self.tamanho
        return h

    def inserir(self, chave):
        """Insere uma palavra ou incrementa sua contagem se já existir."""
        idx = self._hash(chave)
        no_atual = self.tabela[idx]

        # percorre a cadeia procurando a mesma chave
        while no_atual is not None:
            if no_atual.chave == chave:
                no_atual.contagem += 1
                return
            no_atual = no_atual.proximo

        # se não encontrou, insere no início da cadeia
        novo = No(chave)
        novo.proximo = self.tabela[idx]
        self.tabela[idx] = novo

    def buscar(self, chave):
        """Retorna a contagem de uma palavra, ou 0 se não existir."""
        idx = self._hash(chave)
        no_atual = self.tabela[idx]

        while no_atual is not None:
            if no_atual.chave == chave:
                return no_atual.contagem
            no_atual = no_atual.proximo

        return 0

    def items(self):
        """Gera pares (palavra, contagem) de todos os itens da tabela."""
        for pos in self.tabela:
            no_atual = pos
            while no_atual is not None:
                yield no_atual.chave, no_atual.contagem
                no_atual = no_atual.proximo

    def total_chaves(self):
        """Retorna a quantidade total de palavras distintas na tabela."""
        total = 0
        for pos in self.tabela:
            no_atual = pos
            while no_atual is not None:
                total += 1
                no_atual = no_atual.proximo
        return total


def contar_palavras(sentenca_spacy):
    """Cria uma HashTable com a contagem de palavras relevantes de uma sentença."""
    tabela = HashTable()

    for token in sentenca_spacy:
        if token.is_stop or token.is_punct or token.is_space:
            continue

        palavra = token.lemma_.lower()
        tabela.inserir(palavra)

    return tabela
