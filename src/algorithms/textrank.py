from ..structures.graph import Graph


class TextRank:
    """Implementa a fase de ponderação de arestas do algoritmo TextRank."""
    def __init__(self, sentences: list):
        """Cria o grafo e adiciona cada frase como vértice."""
        self.sentences = sentences
        self.graph = Graph()

        for i, sentence in enumerate(sentences):
            self.graph.add_vertex(i, sentence["original_text"])

    def edge_weight(self, processed_sentences: list):
        """Calcula o peso de cada aresta comparando pares de frases via HashTable.

        Para cada par (i, j), itera as palavras da HashTable de uma frase
        e busca na da outra. Complexidade: O(n² * palavras_por_frase).
        """
        n = len(processed_sentences)

        for i in range(n):
            for j in range(i + 1, n):
                sent_a = processed_sentences[i]
                sent_b = processed_sentences[j]

                hash_a = sent_a["hash_table"]
                hash_b = sent_b["hash_table"]

                common = 0
                total_a = 0

                # itera palavras da frase A e busca na HashTable da frase B
                for word, count_a in hash_a.items():
                    total_a += count_a
                    if hash_b.buscar(word) > 0:
                        common += 1

                # soma total de palavras da frase B
                total_b = 0
                for word, count_b in hash_b.items():
                    total_b += count_b

                total = total_a + total_b

                # peso = palavras em comum / total de palavras (sem repetir comuns)
                if common > 0:
                    weight = common / (total - common)
                    self.graph.add_edge(i, j, weight)

        return self.graph.matrix
