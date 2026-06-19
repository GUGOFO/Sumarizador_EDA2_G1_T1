class Vertex:
    """Representa um vértice no grafo (uma frase do termo de serviço)."""
    def __init__(self, vertex_id: int, text: str):
        self.id = vertex_id        # Um identificador único (ex: 0, 1, 2...)
        self.text = text          # O texto original da frase
        self.pagerank = 1.0       # Valor inicial padrão do PageRank para cada página/frase

    def __str__(self):
        return f"Vértice({self.id}): {self.text[:30]}... [PR: {self.pagerank:.4f}]"


class Graph:
    """Representa o Grafo Não-Direcionado usando Lista de Adjacência."""
    def __init__(self):
        # NOTA DE EDA 2: No futuro, você vai substituir estes dicionários nativos ({})
        # pela sua própria classe HashTable feita à mão (hash_table.py).
        self.vertices = {}          # Mapeia: vertex_id -> Objeto Vertex
        self.adjacency_list = {}    # Mapeia: vertex_id -> {vizinho_id: peso_da_aresta}

    def add_vertex(self, vertex_id: int, text: str) -> bool:
        """Adiciona uma nova frase como vértice no grafo."""
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = Vertex(vertex_id, text)
            self.adjacency_list[vertex_id] = {}  # Inicia a lista de adjacência deste vértice
            return True
        return False

    def add_edge(self, v1_id: int, v2_id: int, weight: int):
        """Cria ou atualiza uma aresta não-direcionada com um determinado peso."""
        if v1_id in self.vertices and v2_id in self.vertices:
            # Como o grafo não é direcionado, a relação existe bidirecionalmente
            self.adjacency_list[v1_id][v2_id] = weight
            self.adjacency_list[v2_id][v1_id] = weight

    def get_neighbors(self, vertex_id: int):
        """Retorna os identificadores dos vértices vizinhos e os seus pesos."""
        return self.adjacency_list.get(vertex_id, {})

    def get_vertex(self, vertex_id: int) -> Vertex:
        """Retorna o objeto Vertex pelo ID."""
        return self.vertices.get(vertex_id)

    def get_all_vertex_ids(self):
        """Retorna uma lista com todos os IDs dos vértices (útil para o PageRank)."""
        return list(self.vertices.keys())

    def get_total_weight(self, vertex_id: int) -> int:
        """
        Calcula a soma dos pesos de todas as arestas que saem deste vértice.
        Isto é CRUCIAL para a fórmula do PageRank: PR(A) / C(A).
        """
        neighbors = self.get_neighbors(vertex_id)
        # No futuro, se a sua HashTable não tiver sum(), faça um loop manual
        total = 0
        for weight in neighbors.values():
            total += weight
        return total

    def __len__(self):
        """Retorna o número total de vértices no grafo."""
        return len(self.vertices)