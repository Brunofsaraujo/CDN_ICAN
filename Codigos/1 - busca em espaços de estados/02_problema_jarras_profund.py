from collections import deque

# Capacidades das jarras
JARRA_1_CAPACID = 3
JARRA_2_CAPACID = 5
META = 4
estado_inicial = (0, 0)

# Função para gerar os próximos estados possíveis
def obter_estados_seguintes(estado):
    x, y = estado
    estados = []
    estados.append((JARRA_1_CAPACID, y))   # encher jarra 1
    estados.append((x, JARRA_2_CAPACID))   # encher jarra 2
    estados.append((0, y))         # esvaziar jarra 1
    estados.append((x, 0))         # esvaziar jarra 2
    transfere = min(x, JARRA_2_CAPACID - y)     # calcula qtd a transferir J1 p/ J2
    estados.append((x - transfere, y + transfere))   # transfere J1 p/ J2
    transfere = min(y, JARRA_1_CAPACID - x)     # calcula qtd a transferir J2 p/ J1
    estados.append((x + transfere, y - transfere))   # transfere J2 p/ J1
    return estados

# Algoritmo de busca em profundidade (DFS)
def dfs():
    pilha = [(estado_inicial, [estado_inicial])]
    visitados = set()

    while pilha:
        atual, caminho = pilha.pop()
        x, y = atual
        print(f"Jarra de 3L = {x}L, Jarra de 5L = {y}L")

        if y == META:
            print("\nSolução encontrada!")
            for estado in caminho:
                print(f"Jarra de 3L = {estado[0]}L, Jarra de 5L = {estado[1]}L")
            return

        visitados.add(atual)
        for estado_seguinte in obter_estados_seguintes(atual):
            if estado_seguinte not in visitados:
                pilha.append((estado_seguinte, caminho + [estado_seguinte]))

    print("Nenhuma solução encontrada.")

# Executar o algoritmo
dfs()
