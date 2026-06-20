RED = True
BLACK = False


class RNode:
    """Nó da Árvore Rubro-Negra Esquerdista que guarda um vértice."""
    def __init__(self, vertex):
        self.vertex = vertex    # objeto Vertex associado a este nó
        self.color = RED        # novos nós sempre começam vermelhos
        self.left = None
        self.right = None


class LLRBTree:
    """Árvore Rubro-Negra Esquerdista para ordenar vértices por pagerank."""
    def __init__(self):
        self.root = None

    def _is_red(self, node) -> bool:
        """Verifica se um nó é vermelho (None é considerado preto)."""
        if node is None:
            return BLACK
        return node.color == RED

    def _rotate_left(self, h: RNode) -> RNode:
        """Rotação para esquerda:平衡a subárvore com filho à direita."""
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        return x

    def _rotate_right(self, h: RNode) -> RNode:
        """Rotação para direita:平衡a subárvore com filho à esquerda."""
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RED
        return x

    def _color_flip(self, h: RNode):
        """Inverte as cores de um nó e seus dois filhos."""
        h.color = not h.color
        if h.left:
            h.left.color = not h.left.color
        if h.right:
            h.right.color = not h.right.color

    def _compare(self, v1, v2) -> int:
        """Compara dois vértices: primeiro por pagerank, depois por id."""
        if v1.pagerank != v2.pagerank:
            return -1 if v1.pagerank < v2.pagerank else 1
        return -1 if v1.id < v2.id else 1

    def insert(self, vertex):
        """Insere um vértice na árvore e平衡a após a inserção."""
        self.root = self._insert(self.root, vertex)
        self.root.color = BLACK

    def _insert(self, h: RNode, vertex) -> RNode:
        """Insere recursivamente e aplicar rotações/flip para manter balanceamento."""
        if h is None:
            return RNode(vertex)

        cmp = self._compare(vertex, h.vertex)
        if cmp < 0:
            h.left = self._insert(h.left, vertex)
        else:
            h.right = self._insert(h.right, vertex)

        if self._is_red(h.right) and not self._is_red(h.left):
            h = self._rotate_left(h)

        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)

        if self._is_red(h.left) and self._is_red(h.right):
            self._color_flip(h)

        return h

    def get_ordered_vertices(self) -> list:
        """Retorna vértices ordenados do maior ao menor pagerank (pós-ordem reversa)."""
        ordered_list = []
        self._reverse_inorder(self.root, ordered_list)
        return ordered_list

    def _reverse_inorder(self, node: RNode, ordered_list: list):
        """Percorre a árvore em pós-ordem reversa (direita → raiz → esquerda)."""
        if node is not None:
            self._reverse_inorder(node.right, ordered_list)
            ordered_list.append(node.vertex)
            self._reverse_inorder(node.left, ordered_list)
