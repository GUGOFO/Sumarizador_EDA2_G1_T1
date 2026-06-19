from Sumarizador_EDA2_G1_T1.src .structures.hash_table import contar_palavras

# vai fazer o texto rank para calcular o peso das arestas
# Pega 2 sentenças e compara usando o dicionário de `hash_table.py`
"""
    for(int i = 0; i < sentencas.length; i++){
        for(int j = i + 1; j < sentencas.length; j++){
            int peso = calcularPeso(sentencas[i], sentencas[j]);
            if(peso > 0){
                grafo[i][j] = peso;
                grafo[j][i] = peso
            }
        }
    }
"""



def calcular_peso(sentenca1, sentenca2):
    x1 = contar_palavras(sentenca1)
    x2 = contar_palavras(sentenca2)
    ...