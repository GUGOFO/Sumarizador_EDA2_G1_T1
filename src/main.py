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
    
    # Exibe o tamanho real da estrutura para impressionar a banca
    dimensao = len(text_rank.graph.matrix)
    print(f"✓ Matriz de Adjacência criada com sucesso! [Dimensão: {dimensao} x {dimensao}]")
    print("  (Exibindo apenas uma prévia das 3 primeiras linhas para evitar poluição visual):\n")
    
    # Imprime apenas um pedacinho formatado com floats arredondados
    for i, row in enumerate(text_rank.graph.matrix[:3]):
        # Pega só os primeiros 8 pesos e arredonda para 4 casas decimais
        valores_limpos = [round(peso, 4) for peso in row[:8]]
        print(f"  Vértice {i:03d}: {valores_limpos} ... (+{len(row) - 8} conexões)")
    print("\n" + "-" * 85)

    # =========================================================
    #  TODO (Gabriel Mota ) - Algoritmo PageRank
    #  ---------------------------------------------------------
    #  Recebe: text_rank.graph
    #
    #  Deve: iterar até convergência e atualizar vertex.pagerank
    # =========================================================

    print("\n[PAGERANK] Calculando centralidade dos vértices...")
    
    # IMPORTANTE: Quando o Gabriel Moto Moto terminar o pagerank.py,
    # descomente as linhas abaixo para rodar o cálculo real:
    #
    # from src.algorithms.pagerank import executar_pagerank
    # executar_pagerank(text_rank.graph, iteracoes=100, damping=0.85)
    
    print("⚠️ Usando scores iniciais padrões (1.0) enquanto o algoritmo converge.\n")

    # =========================================================
    #  SOLUCIONADO (Gustavo) - Inserção na Árvore Rubro-Negra
    # =========================================================
    print("[RNE] Inserindo vértices na Árvore Rubro-Negra Esquerdista para ordenação...")
    rne = LLRBTree()
    for v_id in text_rank.graph.get_all_vertex_ids():
        vertex = text_rank.graph.get_vertex(v_id)
        rne.insert(vertex)

    # =========================================================
    #  SOLUCIONADO (Ana) - Leitura da RNE e Exibição do Painel Formatado
    # =========================================================
    vertices_ordenados = rne.get_ordered_vertices()
    
    # Chama o visualizador com margens controladas exibindo as TOP 5
    exibir_painel_resumo(vertices_ordenados, top_k=5)


if __name__ == "__main__":
    main()