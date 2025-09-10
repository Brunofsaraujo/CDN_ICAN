'''
Breadth First Search (BFS) em Grafos
técnica de Breadth First Search (BFS) para encontrar o caminho entre dois nós em um grafo.
'''

from collections import deque

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
    
    def bfs(self, no_inicial, no_final):    # breadth first search
        fila = deque([(no_inicial, [no_inicial])])
        visitados = set()
        
        while fila:
            no_atual, caminho = fila.popleft()
            
            if no_atual == no_final:
                return caminho
            
            if no_atual not in visitados:
                visitados.add(no_atual)
                
                for no_adjacente in self.nos[no_atual]:
                    fila.append((no_adjacente, caminho + [no_adjacente]))

            print('fila =',fila)
            print('caminho atual = ', caminho)
        return None

# Crie um grafo com 10 nós
grafo = Grafo()
for no in 'ABCDEFGHIJ':
    grafo.adiciona_no(no)

# arestas (conj de duplas)
arestas = [ ('A','C'), ('B','D'), ('B','I'), ('C','E'), ('C','F'), 
            ('D','F'), ('F','I'), ('G','H'), ('H','J'), ('I','J') ]

'''
A - C - E   G
      \     |
B - D - F   H
  \   /   /
    I - J
'''

# constroi o grafo
for no1, no2 in arestas:
    grafo.adiciona_aresta(no1, no2)

# Encontre o caminho entre dois nós
no_inicial = 'A'
no_final = 'G'
caminho = grafo.bfs(no_inicial, no_final)

if caminho:
    print(f"\nCaminho de {no_inicial} a {no_final}: {' -> '.join(caminho)}")
else:
    print(f"\nNão há caminho de {no_inicial} a {no_final}")


