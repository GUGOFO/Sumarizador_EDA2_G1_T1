import argparse
import os
import sys
import textwrap

project_root = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, project_root)

from src.structures.hash_table import HashTable
from src.structures.graph import Graph
from src.structures.rne import LLRBTree
from src.nlp.processor import TextProcessor
from src.algorithms.textrank import TextRank
from src.algorithms.pagerank import Pagerank

def exibir_painel_resumo(vertices_ordenados, porcentagem_corte):
    """
    Formata e exibe o resultado final no terminal de forma organizada,
    destacando a cláusula mais importante e listando o corte percentual dinâmico.
    """
    total_frases = len(vertices_ordenados)
    if total_frases == 0:
        print("[ERRO] Nenhum vértice disponível para exibição.")
        return

    # Calcula dinamicamente o número de frases com base na porcentagem escolhida
    limite_frases = max(1, int(total_frases * (porcentagem_corte / 100)))
    
    LARGURA_MARGEM = 85

    print("\n" + "=" * LARGURA_MARGEM)
    print(f"{'RELATÓRIO DE SUMARIZAÇÃO EXECUTIVA - TEXTRANK':^{LARGURA_MARGEM}}")
    print(f"{'FCTE - UNIVERSIDADE DE BRASÍLIA (UnB) - EDA 2':^{LARGURA_MARGEM}}")
    print("=" * LARGURA_MARGEM)
    
    print(f" Total no Documento: {total_frases} sentenças processadas.")
    print(f" Corte Selecionado : {porcentagem_corte}% do texto (Resultando em {limite_frases} frases).")
    print("-" * LARGURA_MARGEM)

    primeiro = vertices_ordenados[0]
    print(f"\n🏆 CLÁUSULA CRÍTICA SOBERANA (1º LUGAR) - SCORE PR: {primeiro.pagerank:.6f} (ID: {primeiro.id})")
    print(" " + "═" * (LARGURA_MARGEM - 2))
    
    linhas_texto_1 = textwrap.wrap(primeiro.text, width=LARGURA_MARGEM - 8)
    for linha in linhas_texto_1:
        print(f"   {linha}")
    print(" " + "═" * (LARGURA_MARGEM - 2))

    if limite_frases > 1:
        print(f"\n📋 OUTRAS SENTENÇAS RELEVANTES DENTRO DOS {porcentagem_corte}% DO CORTE:")
        print("-" * LARGURA_MARGEM)
        
        for posicao, vertex in enumerate(vertices_ordenados[1:limite_frases], 2):
            header = f" [{posicao}º Lugar] - SCORE PR: {vertex.pagerank:.6f} (ID: {vertex.id}) "
            print(f" {header:-<{LARGURA_MARGEM-2}}")
            
            # Aplica a mesma quebra inteligente para as demais frases
            linhas_texto = textwrap.wrap(vertex.text, width=LARGURA_MARGEM - 8)
            for linha in linhas_texto:
                print(f"   {linha}")
            print()
            
    print("-" * LARGURA_MARGEM)
    print(f"{'ANÁLISE ESTATÍSTICA DO CONTRATO':^{LARGURA_MARGEM}}")
    print("-" * LARGURA_MARGEM)
    
    reducao = (1 - (limite_frases / total_frases)) * 100
    print(f" * Taxa de compressão de leitura imposta ao usuário: {reducao:.2f}%")
    print(f" * Status de integridade das estruturas de dados: 100% Manuais (Sem NetworkX/Pandas)")
    print("=" * LARGURA_MARGEM + "\n")


def main():
    parser = argparse.ArgumentParser(description="Sumarizador de textos com TextRank")
    parser.add_argument("--arquivo", required=True, help="Nome do arquivo .txt na pasta inputs/")
    # Nova flag adicionada para capturar a porcentagem dinâmica informada pelo usuário
    parser.add_argument("--porcentagem", type=int, default=20, help="Porcentagem de frases para o resumo (ex: 20)")
    args = parser.parse_args()

    inputs_dir = os.path.join(project_root, "inputs")

    processor = TextProcessor()
    raw_text = processor.load_text_from_file(inputs_dir, args.arquivo)
    processed_sentences = processor.process_contract(raw_text)

    print(f"Texto processado: {len(processed_sentences)} frases relevantes encontradas.\n")

    text_rank = TextRank(processed_sentences)
    text_rank.edge_weight(processed_sentences)

    print("Grafo montado com arestas de similaridade.\n")
    
    dimensao = len(text_rank.graph.matrix)
    print(f"✓ Matriz de Adjacência criada com sucesso! [Dimensão: {dimensao} x {dimensao}]")
    print("  (Exibindo apenas uma prévia das 3 primeiras linhas para evitar poluição visual):\n")
    
    for i, row in enumerate(text_rank.graph.matrix[:3]):
        valores_limpos = [round(peso, 4) for peso in row[:8]]
        print(f"  Vértice {i:03d}: {valores_limpos} ... (+{len(row) - 8} conexões)")
    print("\n" + "-" * 85)

    print("\n[PAGERANK] Calculando centralidade dos vértices...")
    Pagerank(
        text_rank.graph,
        damping=0.85,
        tolerancia=1e-6,
        max_iteracoes=100,
        verbose=True,
    )
    print("[PAGERANK] Scores finais atualizados nos vértices.\n")

    print("[RNE] Inserindo vértices na Árvore Rubro-Negra Esquerdista para ordenação...")
    rne = LLRBTree()
    for v_id in text_rank.graph.get_all_vertex_ids():
        vertex = text_rank.graph.get_vertex(v_id)
        rne.insert(vertex)

    vertices_ordenados = rne.get_ordered_vertices()
    
    # Passa a lista ordenada pela sua RNE e a porcentagem vinda do terminal
    exibir_painel_resumo(vertices_ordenados, porcentagem_corte=args.porcentagem)


if __name__ == "__main__":
    main()