# ─────────────────────────────────────────────────────────────────────────────
# ABB RNE auxiliar (colisão)
# ─────────────────────────────────────────────────────────────────────────────

# region RNE auxiliar

RED = True
BLACK = False

# NÓ DA ÁRVORE RNE USADA COMO BUCKET

class NoArvore:
    """Nó da Árvore Rubro-Negra Esquerdista usada dentro de cada posição da Hash"""
    def __init__(self, chave, contagem=1):
        self.chave = chave          # palavra 
        self.contagem = contagem    # quantas vezes a palavra apareceu
        self.color = RED            # novos nós sempre começam vermelhos
        self.left = None
        self.right = None

# ABB RNE

class HashRNE:
    """
        arvore Rubro Negra Esquerdista usada na HashTable.
        Compara as chaves por ordem alfabética
        se ja existir aumenta a contagem
        busca em O(log n)

    """

    def __init__(self):
        self.root = None

    def _is_red(self, node) -> bool:
        if node is None:
            return BLACK
        return node.color == RED
    
    # Correções 
    def _rotate_left(self, h: NoArvore) -> NoArvore:
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        return x

    def _rotate_right(self, h: NoArvore) -> NoArvore:
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RED
        return x

    def _color_flip(self, h: NoArvore):
        h.color = not h.color
        if h.left:
            h.left.color = not h.left.color
        if h.right:
            h.right.color = not h.right.color

    def inserir(self, chave: str):
        """Insere a chave na árvore ou incrementa sua contagem se já existir."""
        self.root = self._inserir(self.root, chave)
        self.root.color = BLACK     # raiz é sempre preta

    def _inserir(self, h: NoArvore, chave: str) -> NoArvore:
        if h is None:
            return NoArvore(chave)

        # Navegação por ordem alfabética (diferente do rne.py que usa pagerank)
        if chave < h.chave:
            h.left = self._inserir(h.left, chave)
        elif chave > h.chave:
            h.right = self._inserir(h.right, chave)
        else:
            # Chave já existe: só incrementa a contagem, sem novo nó
            h.contagem += 1
            return h               # árvore não mudou o formato

        # Rebalanceamento 
        if self._is_red(h.right) and not self._is_red(h.left):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._color_flip(h)

        return h

    def buscar(self, chave: str) -> int:
        """Busca binária pela chave; retorna a contagem"""
        node = self.root
        while node is not None:
            if chave < node.chave:
                node = node.left
            elif chave > node.chave:
                node = node.right
            else:
                return node.contagem
        return 0

    def items(self):
        """Percorre em inorder (ordem alfabética) e gera pares (chave, contagem)."""
        yield from self._inorder(self.root)

    def _inorder(self, node: NoArvore):
        if node is not None:
            yield from self._inorder(node.left)
            yield node.chave, node.contagem
            yield from self._inorder(node.right)

    def total_chaves(self) -> int:
        """Número de chaves distintas armazenadas nesta árvore."""
        count = 0
        for _ in self.items():
            count += 1
        return count

# endregion

# ─────────────────────────────────────────────────────────────────────────────
# HASH TABLE
# ─────────────────────────────────────────────────────────────────────────────


class HashTable:
    """Tabela hash com Árvore RNE pra colisões"""

    def __init__(self, tamanho=101):
        self.tamanho = tamanho
        self.tabela = [None] * tamanho  # cada posição tem uma HashRNE

    def _hash(self, chave: str) -> int:
        """Função de dispersão: converte a chave em um índice da tabela."""
        h = 0
        for c in chave:
            h = (h * 31 + ord(c)) % self.tamanho
        return h

    def inserir(self, chave: str):
        """Insere uma palavra ou incrementa sua contagem na árvore RNE."""
        idx = self._hash(chave)
        if self.tabela[idx] is None:
            self.tabela[idx] = HashRNE()
        self.tabela[idx].inserir(chave)

    def buscar(self, chave: str) -> int:
        """Retorna a contagem de uma palavra, ou 0 se não existir."""
        idx = self._hash(chave)
        if self.tabela[idx] is None:
            return 0
        return self.tabela[idx].buscar(chave)

    def items(self):
        """Gera pares (palavra, contagem) de todos os itens da tabela."""
        for arvore in self.tabela:
            if arvore is not None:
                yield from arvore.items()

    def total_chaves(self) -> int:
        """Retorna a quantidade total de palavras distintas na tabela."""
        total = 0
        for arvore in self.tabela:
            if arvore is not None:
                total += arvore.total_chaves()
        return total


def contar_palavras(sentenca_spacy) -> HashTable:
    """Cria uma HashTable com a contagem de palavras relevantes de uma sentença."""
    tabela = HashTable()

    for token in sentenca_spacy:
        if token.is_stop or token.is_punct or token.is_space:
            continue

        palavra = token.lemma_.lower()
        tabela.inserir(palavra)

    return tabela