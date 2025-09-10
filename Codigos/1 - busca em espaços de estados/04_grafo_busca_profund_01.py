'''
Depth First Search (DFS) em Grafos

técnica de Depth First Search (DFS) para encontrar 
o caminho entre dois nós em um grafo.
'''

class Grafo:
    def __init__(self):
        self.nos = {}
    
    def adiciona_no(self, no):
        if no not in self.nos:
            self.nos[no] = []
    
    def adiciona_aresta(self, no1, no2):
        if no1 in self.nos and no2 in self.nos:
            self.nos[no1].append(no2)
            self.nos[no2].append(no1)
    
    def dfs(self, no_inicial, no_final):    # depth first search
        visitados = set()
        caminho = []
        
        def dfs_auxiliar(no_atual, caminho_atual):
            visitados.add(no_atual)
            caminho_atual.append(no_atual)
            
            if no_atual == no_final:
                return caminho_atual
            
            for no_adjacente in self.nos[no_atual]:
                if no_adjacente not in visitados:
                    resultado = dfs_auxiliar(no_adjacente, caminho_atual)
                    if resultado:
                        return resultado
            
                print('caminho atual = ', caminho_atual)   # debug

            caminho_atual.pop()
            return None
        
        return dfs_auxiliar(no_inicial, caminho)

# Crie um grafo com 10 nós
grafo = Grafo()
for no in 'ABCDEFGHIJ':
    grafo.adiciona_no(no)

# Adicione algumas arestas aleatórias
arestas = [('A','C'), ('B','D'), ('B','I'), ('C','E'), ('C','F'), 
            ('D','F'), ('F','I'), ('G','H'), ('H','J'), ('I','J')]

'''
A - C - E   G
      \     |
B - D - F   H
  \   /   /
    I - J
'''

for no1, no2 in arestas:
    grafo.adiciona_aresta(no1, no2)

# Encontre o caminho entre dois nós
no_inicial = 'A'
no_final = 'J'
caminho = grafo.dfs(no_inicial, no_final)

if caminho:
    print(f"\nCaminho de {no_inicial} a {no_final}: {' -> '.join(caminho)}")
else:
    print(f"\nNão há caminho de {no_inicial} a {no_final}")


'''
Explicação

    Criamos uma classe Grafo para representar o grafo.
    A classe tem métodos para adicionar nós e arestas ao grafo.
    O método dfs implementa a técnica de Depth First Search para encontrar o caminho entre dois nós.
    A função utiliza uma função auxiliar dfs_auxiliar para realizar a busca em profundidade.
    A função auxiliar utiliza uma lista para manter o caminho atual e um conjunto para manter os nós já visitados.
    A função retorna o caminho entre os dois nós se encontrado, ou None caso contrário.

    Observe caminho_atual.pop() antes de retornar None. 
    Isso garante que o caminho atual seja "desfeito" quando um nó não leva ao nó final, 
    permitindo que a busca em profundidade explore outros caminhos.

Execução

Ao executar o programa, saída:

Caminho de A a J: A -> C -> F -> D -> B -> I -> J

ou outro caminho válido, dependendo das arestas adicionadas ao grafo.
'''
