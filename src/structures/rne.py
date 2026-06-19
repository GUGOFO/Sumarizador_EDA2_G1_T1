RED = True
BLACK = False

class RNode:
    def __init__(self, vertex):
        self.vertex = vertex        
        self.color = RED            
        self.left = None
        self.right = None


class LLRBTree:
    def __init__(self):
        self.root = None

    def _is_red(self, node) -> bool:
        if node is None:
            return BLACK
        return node.color == RED

    def _rotate_left(self, h: RNode) -> RNode:
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        return x

    def _rotate_right(self, h: RNode) -> RNode:
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RED
        return x

    def _color_flip(self, h: RNode):
        h.color = not h.color
        if h.left:
            h.left.color = not h.left.color
        if h.right:
            h.right.color = not h.right.color

    # --- LÓGICA DE COMPARAÇÃO E INSERÇÃO ---

    def _compare(self, v1, v2) -> int:
        if v1.pagerank != v2.pagerank:
            return -1 if v1.pagerank < v2.pagerank else 1
        return -1 if v1.id < v2.id else 1

    def insert(self, vertex):
        self.root = self._insert(self.root, vertex)
        self.root.color = BLACK  

    def _insert(self, h: RNode, vertex) -> RNode:
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
            
        # 3. Se ambos os filhos são vermelhos: divide a árvore (color flip)
        if self._is_red(h.left) and self._is_red(h.right):
            self._color_flip(h)

        return h

    def get_ordered_vertices(self) -> list:
        ordered_list = []
        self._reverse_inorder(self.root, ordered_list)
        return ordered_list

    def _reverse_inorder(self, node: RNode, ordered_list: list):
        if node is not None:
            self._reverse_inorder(node.right, ordered_list)
            ordered_list.append(node.vertex)
            self._reverse_inorder(node.left, ordered_list)