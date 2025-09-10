'''
utilizar o algoritmo de busca A* (A-Star) com uma heurística que 
leva em consideração a distância entre as cidades e a direção correta. 
Neste exemplo, consideraremos que as cidades são representadas por suas 
coordenadas geográficas (latitude e longitude) e que a direção correta 
é indicada por um ângulo em graus.

A busca A* é sensível à escolha da heurística. Uma heurística admissível 
(nunca superestima o custo real) e consistente (a estimativa para alcançar 
o destino a partir de um estado é sempre menor ou igual ao custo real de 
alcançar o destino a partir desse estado) garante que o algoritmo encontre 
a solução ótima.
'''

import math
import heapq

def distancia(cidade1, cidade2):
    # Calcula a distância entre duas cidades utilizando a fórmula de Haversine
    # https://pt.wikipedia.org/wiki/F%C3%B3rmula_de_haversine 
    lat1, lon1 = math.radians(cidade1[0]), math.radians(cidade1[1])
    lat2, lon2 = math.radians(cidade2[0]), math.radians(cidade2[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = 6371 * c  # 6371 é o raio da Terra em km
    return distancia

def direcao(cidade1, cidade2):
    # Calcula a direção de cidade1 para cidade2 em graus
    lat1, lon1 = math.radians(cidade1[0]), math.radians(cidade1[1])
    lat2, lon2 = math.radians(cidade2[0]), math.radians(cidade2[1])
    dlon = lon2 - lon1
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    direcao = math.degrees(math.atan2(y, x))
    if direcao < 0:
        direcao += 360
    return direcao

# ajusta a heurística para premiar direções mais coerentes com o caminho geral para o destino.
def heuristica(cidade_atual, cidade_destino, cidades):
    dist = distancia(cidade_atual, cidade_destino)
    dir_atual = direcao(cidade_atual, cidade_destino)
    dir_destino = direcao(cidades[0], cidade_destino)  # direção geral para o destino
    fator_direcao = 1 - abs(dir_atual - dir_destino) / 180  # fator de direção (0 a 1)
    return dist * fator_direcao   # heurística: minimiza tanto a distância quanto a direção

def busca_informada(cidades, cidade_inicio, cidade_destino):
    # Implementação do algoritmo A\*
    fila = []
    heapq.heappush(fila, (0, cidade_inicio, [cidade_inicio]))
    visitados = set()
    
    while fila:
        (custo, cidade_atual, caminho) = heapq.heappop(fila)
        print(f"Progresso: {cidade_atual} (custo: {custo:.2f})")   # debug

        if cidade_atual == cidade_destino:
            return caminho
        
        if cidade_atual in visitados:
            continue
        
        visitados.add(cidade_atual)
        print(f"Visitada: {cidade_atual}")
        
        for cidade_vizinha in cidades:
            if cidade_vizinha == cidade_atual:
                continue
            
            novo_custo = custo + distancia(cidade_atual, cidade_vizinha)
            novo_caminho = caminho + [cidade_vizinha]
            heuristica_value = heuristica(cidade_vizinha, cidade_destino, cidades)
            heapq.heappush(fila, (novo_custo + heuristica_value, cidade_vizinha, novo_caminho))
    
    return None

# Exemplo de uso
cidades = [
    (52.5200, 13.4050),  # Berlim 0
    (48.8566, 2.3522),   # Paris 1
    (37.7749, -122.4194), # São Francisco 2
    (51.5074, -0.1278),   # Londres 3
    (40.7128, -74.0060),  # Nova York 4
    (-23.5479, -46.6388), # São Paulo 5
    (39.7392, -104.9903), # Denver 6
    (-33.8651, 151.2093), # Sydney 7
    (30.2672, -97.7431),  # Austin 8
    (35.7796, -78.6382),  # Raleigh 9
]

cidade_inicio = cidades[2]
cidade_destino = cidades[4]

caminho = busca_informada(cidades, cidade_inicio, cidade_destino)
if caminho:
    print("Caminho encontrado:", caminho)
    for i, cidade in enumerate(caminho):
        print(f"{i+1}. {cidade}")
else:
    print("Nenhum caminho encontrado.")




