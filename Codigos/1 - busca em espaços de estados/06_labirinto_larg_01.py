'''
Criar uma representação do labirinto 
utilizando caracteres ASCII. 
O labirinto será representado por uma matriz 10x10, onde:

    | representa paredes do labirinto
     (espaço) representa corredores do labirinto
    E representa a entrada do labirinto
    S representa a saída do labirinto

exemplo:

||||||||||
|E      ||
| |  ||| |
| |  |   |
| || ||  |
|   |    |
|  |||  ||
|  |     |
|  ||  S ||
||||||||||

Implementação em Python
busca em largura (Breadth-First Search, BFS) para encontrar o 
caminho da entrada até a saída do labirinto.

'''

from collections import deque

# Define o labirinto
'''
labirinto = [
    list("||||||||||"),
    list("E |     ||"),
    list("| |  | | |"),
    list("| |  |   |"),
    list("| || ||  |"),
    list("|      | |"),
    list("| ||||   |"),
    list("| ||   |||"),
    list("| |||    |"),
    list("|||||||S||")
]

labirinto = [
    list("|||||||||"),
    list("|   |   |"),
    list("| | | | |"),
    list("E |   | |"),
    list("| | | | |"),
    list("|||||||S|")
]

labirinto = [
    list("|||||||||"),
    list("|   |   |"),
    list("E |   | |"),
    list("|||||||S|")
]

'''

labirinto = [
    list("|| ||"),
    list("|   |"),
    list("E | |"),
    list("|||S|")
]

# Função para imprimir o labirinto
def imprimir_labirinto(labirinto, caminho=None):
    for y, linha in enumerate(labirinto):
        for x, celula in enumerate(linha):
            if caminho and (x, y) in caminho:
                print('*', end='')
            else:
                print(celula, end='')
        print()

# Função para encontrar a entrada
def encontrar_entrada(labirinto):
    for y, linha in enumerate(labirinto):
        for x, celula in enumerate(linha):
            if celula == 'E':
                return (x, y)

# Função para encontrar a saída
def encontrar_saida(labirinto):
    for y, linha in enumerate(labirinto):
        for x, celula in enumerate(linha):
            if celula == 'S':
                return (x, y)

# Busca em largura (BFS)
def bfs(labirinto, inicio, fim):
    direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # direita, esquerda, baixo, cima
    fila = deque([(inicio, [inicio])])
    visitados = set([inicio])

    while fila:
        (x, y), caminho = fila.popleft()
        if (x, y) == fim:
            return caminho

        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(labirinto[0]) and 0 <= ny < len(labirinto) and
                    labirinto[ny][nx] != '|' and (nx, ny) not in visitados):
                fila.append(((nx, ny), caminho + [(nx, ny)]))
                visitados.add((nx, ny))

        print('fila=',fila)
        print('caminho=', caminho)

    return None

# Encontrar entrada e saída
inicio = encontrar_entrada(labirinto)
fim = encontrar_saida(labirinto)

# Executar BFS
caminho = bfs(labirinto, inicio, fim)

# Imprimir resultado
if caminho:
    print("\nCaminho encontrado:")
    imprimir_labirinto(labirinto, caminho)
else:
    print("\nNenhum caminho encontrado.")

'''
Este programa primeiro define o labirinto, 
encontra a entrada e a saída, e então utiliza 
a busca em largura para encontrar um caminho da 
entrada para a saída. 
O caminho é representado por asteriscos (*). 
Se um caminho for encontrado, o labirinto com o 
caminho será exibido; caso contrário, uma mensagem 
informará que nenhum caminho foi encontrado.

A busca em largura (BFS) é particularmente útil para 
encontrar o caminho mais curto em grafos ou labirintos, 
pois ela explora todos os nós (ou células, no caso do 
labirinto) de nível igual antes de prosseguir para o 
próximo nível. 
Isso garante que, se um caminho existir, o BFS encontrará 
o caminho mais curto até o destino.
'''