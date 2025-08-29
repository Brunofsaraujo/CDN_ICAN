from collections import deque

# Cores ANSI para visualização
RESET   = "\033[0m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
BLUE    = "\033[94m"
GRAY    = "\033[90m"
RED     = "\033[91m"

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
    
    def bfs(self, no_inicial, no_final):
        fila = deque([(no_inicial, [no_inicial])])
        visitados = set()
        pais = {no_inicial: None}
        niveis = {no_inicial: 0}

        print(f"\n🔍 Iniciando BFS de {no_inicial} até {no_final}\n")

        while fila:
            no_atual, caminho = fila.popleft()

            # Exibe status
            fila_str = ", ".join([f"{BLUE}{n[0]}{RESET}" for n in fila])
            print(f"Nó atual: {YELLOW}{no_atual}{RESET}")
            print(f"Caminho até aqui: {' -> '.join(caminho)}")
            print(f"Fila: [{fila_str}]")
            print(f"Visitados: {GRAY}{', '.join(visitados)}{RESET}\n")

            # Verificação de sucesso
            if no_atual == no_final:
                print(f"{GREEN}✅ Caminho encontrado!{RESET}")
                self.desenha_arvore(pais, niveis, no_inicial, caminho)
                return caminho

            # Expansão de nós adjacentes
            if no_atual not in visitados:
                visitados.add(no_atual)
                for no_adjacente in self.nos[no_atual]:
                    if no_adjacente not in visitados:
                        pais[no_adjacente] = no_atual
                        niveis[no_adjacente] = niveis[no_atual] + 1
                        fila.append((no_adjacente, caminho + [no_adjacente]))

        print(f"{RED}❌ Não há caminho encontrado.{RESET}")
        return None
    
    def desenha_arvore(self, pais, niveis, raiz, caminho):
        print("\n🌳 Árvore de Busca (BFS):\n")

        def imprime(no, prefixo="", ultimo=True):
            marcador = "└── " if ultimo else "├── "
            cor = GREEN if no in caminho else GRAY
            print(prefixo + marcador + cor + no + RESET)

            filhos = [filho for filho, p in pais.items() if p == no]
            for i, filho in enumerate(filhos):
                ultimo_filho = (i == len(filhos) - 1)
                novo_prefixo = prefixo + ("    " if ultimo else "│   ")
                imprime(filho, novo_prefixo, ultimo_filho)

        imprime(raiz, "", True)


# Construindo o grafo
grafo = Grafo()
for no in 'ABCDEFGHIJ':
    grafo.adiciona_no(no)

arestas = [
    ('A','C'), ('B','D'), ('B','I'), ('C','E'), ('C','F'), 
    ('D','F'), ('F','I'), ('G','H'), ('H','J'), ('I','J')
]
for no1, no2 in arestas:
    grafo.adiciona_aresta(no1, no2)

print('''
A - C - E   G
      \\     |
B - D - F   H
  \\   /   /
    I - J
''')

# Executando busca
no_inicial = 'B'
no_final = 'E'
caminho = grafo.bfs(no_inicial, no_final)

if caminho:
    print(f"\nCaminho final de {no_inicial} a {no_final}: {GREEN}{' -> '.join(caminho)}{RESET}")
