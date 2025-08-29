from collections import deque

# Capacidades máximas das jarras
JARRA_1_CAPACID = 3  # jarra menor
JARRA_2_CAPACID = 5  # jarra maior

# Objetivo: obter exatamente 4 litros na jarra de 5 litros
OBJETIVO = 4

# Estado inicial: ambas as jarras estão vazias
estado_inicial = (0, 0)

# Função que gera todos os estados possíveis a partir de um estado atual
def obter_estados_seguintes(estado):
    x, y = estado  # x: quantidade na jarra 1, y: quantidade na jarra 2
    estados = []

    # Encher completamente a jarra 1
    estados.append((JARRA_1_CAPACID, y))
    # Encher completamente a jarra 2
    estados.append((x, JARRA_2_CAPACID))
    # Esvaziar completamente a jarra 1
    estados.append((0, y))
    # Esvaziar completamente a jarra 2
    estados.append((x, 0))
    # Transferir da jarra 1 para a 2 até encher a 2 ou esvaziar a 1
    transferir = min(x, JARRA_2_CAPACID - y)
    estados.append((x - transferir, y + transferir))
    # Transferir da jarra 2 para a 1 até encher a 1 ou esvaziar a 2
    transferir = min(y, JARRA_1_CAPACID - x)
    estados.append((x + transferir, y - transferir))

    return estados

# Função que implementa a busca em largura (BFS) para encontrar a solução
def bfs():
    fila = deque()         # fila para armazenar os estados a serem explorados
    visitado = set()       # conjunto para armazenar os estados já visitados
    predecessor = {}       # dicionário para rastrear o caminho de cada estado

    fila.append(estado_inicial)
    visitado.add(estado_inicial)
    predecessor[estado_inicial] = None

    while fila:
        atual = fila.popleft()
        x, y = atual
        print(f"Jarra {JARRA_1_CAPACID}L= {x}L, Jarra {JARRA_2_CAPACID}L= {y}L")  # imprime o estado atual

        # Verifica se atingimos o objetivo
        if y == OBJETIVO:
            print("\nSolução encontrada!")
            caminho = []
            # Reconstrói o caminho desde o estado inicial até o objetivo
            while atual:
                caminho.append(atual)
                atual = predecessor[atual]
            caminho.reverse()
            # Imprime a sequência de estados que leva à solução
            for estado in caminho:
                print(f"Jarra {JARRA_1_CAPACID}L= {estado[0]}L, Jarra {JARRA_2_CAPACID}L= {estado[1]}L")
            return

        # Gera e explora os próximos estados possíveis
        for estado_seguinte in obter_estados_seguintes(atual):
            if estado_seguinte not in visitado:
                visitado.add(estado_seguinte)
                predecessor[estado_seguinte] = atual
                fila.append(estado_seguinte)

    print("Nenhuma solução encontrada.")

# Executa o algoritmo de busca Breadth First Search
bfs()


''' comentários
A linha de código: from collections import deque
faz parte da biblioteca padrão do Python

collections: é um módulo que fornece tipos de dados especializados, além dos tipos básicos como listas, dicionários, etc.

deque (pronuncia-se “deck”, abreviação de double-ended queue): é uma estrutura de dados semelhante a uma lista, mas otimizada para inserções e remoções rápidas tanto no início quanto no fim da fila.

No algoritmo de busca em largura (BFS), é necessário:

Adicionar novos estados ao final da fila.
Remover o estado atual do início da fila.
A estrutura deque é ideal para isso, pois:

É mais eficiente que uma lista comum (list) para operações de fila.
Tem métodos como .append() e .popleft() que funcionam em tempo constante.
'''
