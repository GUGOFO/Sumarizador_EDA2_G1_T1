class Vertex:
    """Representa um vértice no grafo (uma frase do texto)."""
    def __init__(self, vertex_id: int, text: str):
        self.id = vertex_id    # identificador único da frase
        self.text = text       # texto original da frase
        self.pagerank = 1.0    # valor inicial do PageRank

    def __str__(self):
        return f"Vertex({self.id}): {self.text[:30]}... [PR: {self.pagerank:.4f}]"


class Graph:
    """Grafo não-direcionado representado por matriz de adjacência."""
    def __init__(self):
        self.vertices = []  # lista de objetos Vertex (indexada pelo vertex_id)
        self.matrix = []    # matriz de adjacência com pesos das arestas

    def add_vertex(self, vertex_id: int, text: str) -> bool:
        """Adiciona um vértice ao grafo. Retorna False se já existir."""
        if vertex_id < len(self.vertices) and self.vertices[vertex_id] is not None:
            return False

        # cresce a lista de vértices até o índice desejado
        while len(self.vertices) <= vertex_id:
            self.vertices.append(None)

        self.vertices[vertex_id] = Vertex(vertex_id, text)

        # cresce a matriz para acomodar o novo vértice
        for row in self.matrix:
            while len(row) <= vertex_id:
                row.append(0)
        while len(self.matrix) <= vertex_id:
            self.matrix.append([0] * (vertex_id + 1))

        return True

    def add_edge(self, v1_id: int, v2_id: int, weight):
        """Cria ou atualiza uma aresta não-direcionada entre dois vértices."""
        if v1_id >= len(self.matrix) or v2_id >= len(self.matrix):
            return
        if self.vertices[v1_id] is None or self.vertices[v2_id] is None:
            return
        self.matrix[v1_id][v2_id] = weight
        self.matrix[v2_id][v1_id] = weight

    def get_neighbors(self, vertex_id: int):
        """Retorna dict {vizinho_id: peso} com os vizinhos do vértice."""
        if vertex_id >= len(self.matrix):
            return {}
        neighbors = {}
        for j, weight in enumerate(self.matrix[vertex_id]):
            if weight != 0 and j != vertex_id:
                neighbors[j] = weight
        return neighbors

    def get_vertex(self, vertex_id: int):
        """Retorna o objeto Vertex pelo ID, ou None se não existir."""
        if vertex_id < len(self.vertices):
            return self.vertices[vertex_id]
        return None

    def get_all_vertex_ids(self):
        """Retorna lista com todos os IDs dos vértices existentes."""
        return [v.id for v in self.vertices if v is not None]

    def get_total_weight(self, vertex_id: int) -> int:
        """Soma dos pesos de todas as arestas que saem do vértice (usado no PageRank)."""
        if vertex_id >= len(self.matrix):
            return 0
        total = 0
        for weight in self.matrix[vertex_id]:
            total += weight
        return total

    def __len__(self):
        """Retorna o número total de vértices no grafo."""
        return len(self.vertices)
