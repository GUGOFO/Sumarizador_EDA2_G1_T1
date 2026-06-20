from __future__ import annotations

from typing import Optional


def Pagerank(
    grafo,
    damping: float = 0.85,
    tolerancia: float = 1e-6,
    max_iteracoes: int = 100,
    verbose: bool = True,
):
    """Executa o PageRank ponderado sobre o grafo de frases.

    O cálculo considera os pesos das arestas como a força da ligação entre
    frases. Cada vértice recebe sua relevância iterativamente até a variação
    máxima entre duas iterações ficar abaixo da tolerância informada.

    Args:
        grafo: instância de Graph contendo vertices, matrix e helpers.
        damping: fator de amortecimento do PageRank.
        tolerancia: critério de parada por convergência.
        max_iteracoes: limite máximo de iterações.
        verbose: se True, imprime o progresso da convergência.

    Returns:
        O próprio grafo, com cada vertex.pagerank atualizado.
    """
    vertex_ids = grafo.get_all_vertex_ids()
    n = len(vertex_ids)

    if n == 0:
        if verbose:
            print("[PAGERANK] Grafo vazio. Nenhum score calculado.")
        return grafo

    pr_atual = {vertex_id: 1.0 / n for vertex_id in vertex_ids}
    pr_novo = {vertex_id: 0.0 for vertex_id in vertex_ids}

    for vertex_id in vertex_ids:
        vertex = grafo.get_vertex(vertex_id)
        if vertex is not None:
            vertex.pagerank = pr_atual[vertex_id]

    if n == 1:
        if verbose:
            print("[PAGERANK] Apenas um vértice encontrado. Score fixado em 1.0.")
        return grafo

    for iteracao in range(1, max_iteracoes + 1):
        valor_base = (1.0 - damping) / n

        for vertex_id in vertex_ids:
            pr_novo[vertex_id] = valor_base

        dangling_mass = 0.0
        for vertex_id in vertex_ids:
            if grafo.get_total_weight(vertex_id) <= 0:
                dangling_mass += pr_atual[vertex_id]

        dangling_share = damping * dangling_mass / n
        for vertex_id in vertex_ids:
            pr_novo[vertex_id] += dangling_share

        for origem_id in vertex_ids:
            peso_saida = grafo.get_total_weight(origem_id)
            if peso_saida <= 0:
                continue

            vizinhos = grafo.get_neighbors(origem_id)
            if not vizinhos:
                continue

            contribuicao_origem = damping * pr_atual[origem_id] / peso_saida
            for destino_id, peso_aresta in vizinhos.items():
                pr_novo[destino_id] += contribuicao_origem * peso_aresta

        delta_max = 0.0
        for vertex_id in vertex_ids:
            diff = abs(pr_novo[vertex_id] - pr_atual[vertex_id])
            if diff > delta_max:
                delta_max = diff

        if verbose:
            print(
                f"[PAGERANK] Iteração {iteracao:03d} | delta máximo = {delta_max:.8f}"
            )

        pr_atual, pr_novo = pr_novo, pr_atual

        if delta_max < tolerancia:
            if verbose:
                print(
                    f"[PAGERANK] Convergência atingida na iteração {iteracao} "
                    f"(tolerância={tolerancia})."
                )
            break
    else:
        if verbose:
            print(
                f"[PAGERANK] Limite de {max_iteracoes} iterações atingido "
                f"sem convergir totalmente."
            )

    for vertex_id in vertex_ids:
        vertex = grafo.get_vertex(vertex_id)
        if vertex is not None:
            vertex.pagerank = pr_atual[vertex_id]

    return grafo
