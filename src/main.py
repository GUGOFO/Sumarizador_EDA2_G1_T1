import argparse
import os
import sys

project_root = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, project_root)

from src.structures.hash_table import HashTable
from src.structures.graph import Graph
from src.structures.rne import LLRBTree
from src.nlp.processor import TextProcessor
from src.algorithms.textrank import TextRank

def exibir_painel_resumo(vertices_ordenados, top_k=5):

    total_frases = len(vertices_ordenados)
    exibir_top = min(top_k, total_frases)

    LARGURA_MARGEM = 85

    print("\n" + "=" * LARGURA_MARGEM)
    print(f"{'RELATÓRIO DE SUMARIZAÇÃO EXECUTIVA - TEXTRANK':^{LARGURA_MARGEM}}")
    print(f"{'FCTE - UNIVERSIDADE DE BRASÍLIA (UnB) - EDA 2':^{LARGURA_MARGEM}}")
    print("=" * LARGURA_MARGEM)
    
    print(f" Encontradas: {total_frases} sentenças processadas no documento.")
    print(f" Exibindo as {exibir_top} cláusulas mais críticas ordenadas via RNE (Rubro-Negra).")
    print("-" * LARGURA_MARGEM)

    for posicao, vertex in enumerate(vertices_ordenados[:exibir_top], 1):
        header = f" [{posicao}º Lugar] - SCORE PAGERANK: {vertex.pagerank:.4f} (ID: {vertex.id}) "
        print(f"\n{header:-<{LARGURA_MARGEM}}")
        
        texto = vertex.text
        chunk_size = LARGURA_MARGEM - 4
        for i in range(0, len(texto), chunk_size):
            print(f"  {texto[i:i+chunk_size]}")
            
    print("\n" + "-" * LARGURA_MARGEM)
    print(f"{'ANÁLISE ESTATÍSTICA DO CONTRATO':^{LARGURA_MARGEM}}")
    print("-" * LARGURA_MARGEM)
    
    reducao = (1 - (exibir_top / total_frases)) * 100 if total_frases > 0 else 0
    print(f" * Taxa de redução de leitura imposta ao usuário: {reducao:.2f}%")
    print(f" * Status de integridade das estruturas de dados: 100% Manuais (Sem NetworkX/Pandas)")
    print("=" * LARGURA_MARGEM + "\n")

def main():
    parser = argparse.ArgumentParser(description="Sumarizador de textos com TextRank")
    parser.add_argument("--arquivo", required=True, help="Nome do arquivo .txt na pasta inputs/")
    args = parser.parse_args()

    inputs_dir = os.path.join(project_root, "inputs")

    processor = TextProcessor()
    raw_text = processor.load_text_from_file(inputs_dir, args.arquivo)
    processed_sentences = processor.process_contract(raw_text)

    print(f"Texto processado: {len(processed_sentences)} frases relevantes encontradas.\n")

    text_rank = TextRank(processed_sentences)
    text_rank.edge_weight(processed_sentences)

    print("Grafo montado com arestas de similaridade.\n")
    print("Matriz de adjacência:")
    for i, row in enumerate(text_rank.graph.matrix):
        print(f"  Vértice {i}: {row}")

    # =========================================================
    #  TODO (Pessoa 1) - Algoritmo PageRank
    #  ---------------------------------------------------------
    #  Recebe: text_rank.graph
    #    - text_rank.graph.vertices  (lista de objetos Vertex)
    #    - text_rank.graph.matrix    (matriz de adjacência com pesos)
    #    - text_rank.graph.get_neighbors(v_id)  (vizinhos de um vértice)
    #    - text_rank.graph.get_total_weight(v_id) (soma dos pesos das arestas)
    #    - text_rank.graph.get_all_vertex_ids()  (lista com todos os IDs)
    #    - text_rank.graph.__len__()             (número total de vértices)
    #
    #  Deve: iterar até convergência e atualizar vertex.pagerank
    #    Cada vértice já inicia com pagerank = 1.0 (definido em Vertex)
    #
    #  Exemplo de uso esperado:
    #    from src.algorithms.pagerank import executar_pagerank
    #    executar_pagerank(text_rank.graph, iteracoes=100, damping=0.85)
    # =========================================================

    print("\n[PLACEHOLDER] PageRank ainda não implementado.")
    print("Valores de pagerank permanecem em 1.0 para todos os vértices.\n")

    for v_id in text_rank.graph.get_all_vertex_ids():
        v = text_rank.graph.get_vertex(v_id)
        print(f"  {v}")

    # =========================================================
    #  TODO (Pessoa 2) - Inserção na Árvore Rubro-Negra Esquerdista
    #  ---------------------------------------------------------
    #  Recebe: text_rank.graph.get_all_vertex_ids()
    #    Para cada ID: text_rank.graph.get_vertex(v_id) retorna obj Vertex
    #
    #  Deve: criar uma LLRBTree e inserir cada vértice
    #    A comparação da RNE já ordena por pagerank (desc) e id (asc)
    #
    #  Exemplo de uso esperado:
    #    rne = LLRBTree()
    #    for v_id in text_rank.graph.get_all_vertex_ids():
    #        vertex = text_rank.graph.get_vertex(v_id)
    #        rne.insert(vertex)
    # =========================================================

    print("[PLACEHOLDER] Inserção na RNE ainda não implementada.\n")

    rne = LLRBTree()
    for v_id in text_rank.graph.get_all_vertex_ids():
        vertex = text_rank.graph.get_vertex(v_id)
        rne.insert(vertex)

    # =========================================================
    #  TODO (Pessoa 3) - Leitura da RNE e Exibição do Resumo
    #  ---------------------------------------------------------
    #  Recebe: rne.get_ordered_vertices()
    #    Retorna lista de vértices do MAIOR ao MENOR pagerank
    #
    #  Deve: selecionar as top K frases e exibir o resumo
    #
    #  Exemplo de uso esperado:
    #    vertices_ordenados = rne.get_ordered_vertices()
    #    for v in vertices_ordenados:
    #        print(f"[PR: {v.pagerank:.4f}] {v.text}")
    # =========================================================

    print("[PLACEHOLDER] Resumo final ainda não implementado.\n")
    vertices_ordenados = rne.get_ordered_vertices()
    print("Frases ordenadas por pagerank (via RNE):")
    for v in vertices_ordenados:
        print(f"  [PR: {v.pagerank:.4f}] {v.text}")


if __name__ == "__main__":
    main()
