'''
 A função astar_search imprime o g_score calculado, o valor heurístico (h)
 e o custo total estimado (f = g + h) para cada cidade à medida que ela
 é avaliada.
'''
#%%
# bibliotecas

import heapq
import math
import networkx as nx
import matplotlib.pyplot as plt

#%%
# funções

def heuristic(current_city, goal_city, city_coordinates, map_data):

    """
    Calcula o valor (distância) heurístico entre duas cidades usando
    a fórmula de Haversine e considerando a distância mínima de um vizinho

    Args:
        current_city: O nome da cidade atual.
        goal_city: O nome da cidade de destino.
        city_coordinates: Um dicionário de coordenadas da cidade (latitude, longitude).
        map_data: Um dicionário que representa os dados do mapa.

    Retorna:
        O valor heurístico calculado.
    """

    '''
    # Calcule a distância em linha reta (distância euclidiana)
    x1, y1 = city_coordinates[current_city]
    x2, y2 = city_coordinates[goal_city]
    straight_line_distance = math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
    '''

    # Fórmula de Haversine para calcular a distância em linha reta na superfície da Terra
    lat1, lon1 = city_coordinates[current_city]
    lat2, lon2 = city_coordinates[goal_city]

    R = 6371  # Earth radius in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    straight_line_distance = R * c
    print("straight_line_distance  =", straight_line_distance)   # debug


    # Considere a distância mínima para qualquer vizinho da cidade atual
    min_neighbor_distance = float('inf')   # inicia com inf e vai diminuindo

    # Check if map_data[current_city] is not empty
    if current_city in map_data and map_data[current_city]:
        for neighbor, distance in map_data[current_city].items():
            min_neighbor_distance = min(min_neighbor_distance, distance)
    else:
        min_neighbor_distance = 0 # Sem vizinhos, sem heurística adicional dos vizinhos

    print("min_neighbor_distance = ", min_neighbor_distance)

    # Combine a distância em linha reta e a consideração das distâncias vizinhas
    # Essa é uma combinação simples, e poderia ser usada uma heurística mais complexa
    heuristic_value = straight_line_distance + (min_neighbor_distance * 0.1)
       ## Distância ponderada de vizinhança

    return heuristic_value


def astar_search(map_data, city_coordinates, start_city, goal_city):

    """
    Encontra o caminho mais curto entre duas cidades usando a pesquisa A*.

    Args:
        map_data: Um dicionário que representa os dados do mapa.
        city_coordinates: Um dicionário de coordenadas da cidade.
        start_city: O nome da cidade inicial.
        goal_city: O nome da cidade de destino.

    Retorna:
        Uma tupla contendo o custo total e o caminho do início à meta,
        ou (float('inf'), None) se nenhum caminho for encontrado.
    """

    # Fila de prioridade: lojas (estimated_total_cost, current_city, path)
    priority_queue = []
    # Push inicial com custo total estimado (g=0 + h)
    heapq.heappush(priority_queue, (heuristic(start_city, goal_city,
                                              city_coordinates, map_data
                                              ),
                                    start_city, [start_city]
                                    )
                    )

    # Rastreie o menor custo para chegar a cada cidade encontrada até o momento
    g_score = {city: float('inf') for city in map_data}
    g_score[start_city] = 0

    # Mantenha o controle das cidades visitadas para evitar processamento redundante
    visited = set()

    print(f"\nINÍCIO BUSCA A* DE {start_city} PARA {goal_city}")

    while priority_queue:
        # Obtenha a cidade com o menor custo total estimado
        current_f_score, current_city, current_path = heapq.heappop(priority_queue)

        # Calcule g, h e f para a cidade atual
        current_g_score = g_score[current_city]
        current_h_score = heuristic(current_city, goal_city, city_coordinates, map_data)
        # current_f_score já foi retirado da fila de prioridade

        print(f"\nEvaluating city: {current_city}")
        print(f"  Path: {current_path}")
        print(f"  g(n): {current_g_score:.2f}, h(n): {current_h_score:.2f}, f(n) = g(n) + h(n): {current_f_score:.2f}")


        # Se a meta for alcançada, retorne o caminho e o custo
        if current_city == goal_city:
            print(f"\nGoal reached: {goal_city}")
            return g_score[goal_city], current_path

        # Se já tivermos visitado essa cidade com um custo menor ou igual, pule
        if current_city in visited:
            print(f"  Skipping already visited city: {current_city}")
            continue

        # Marcar a cidade atual como visitada
        visited.add(current_city)
        print(f"  Visited: {visited}")

        # Explorar os vizinhos
        if current_city in map_data:
            print(f"  Exploring neighbors of {current_city}:")
            for neighbor, distance in map_data[current_city].items():
                tentative_g_score = g_score[current_city] + distance

                print(f"    Considering neighbor: {neighbor} with distance {distance}")

                # Se o novo caminho para o vizinho for mais curto
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g_score
                    # Calcule o custo total estimado (g + h)
                    estimated_total_cost = tentative_g_score + heuristic(neighbor,
                                                                         goal_city,
                                                                         city_coordinates,
                                                                         map_data)
                    # Adicionar o vizinho à fila de prioridade
                    new_path = current_path + [neighbor]
                    heapq.heappush(priority_queue, (estimated_total_cost,
                                                    neighbor, new_path))
                    print(f"      Adding/Updating neighbor {neighbor} to priority queue with estimated cost {estimated_total_cost:.2f} and tentative path {new_path}")
                else:
                    print(f"      Neighbor {neighbor} already has a better or equal path.")


    # Se a fila de prioridades estiver vazia e a meta não tiver sido atingida
    print("\nPriority queue is empty. No path found.")
    return float('inf'), None



#%%
# Dados para o mapa da Romênia retirados do livro "Artificial Intelligence"
# de Russell e Norvig
# distância entre cidades

map_data = {
    'Arad': {'Zerind': 75, 'Timisoara': 118, 'Sibiu': 140},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

# Coordenadas geográficas (lat, long) aproximadas das cidades da Romênia
# (para heurística) - para considerar distância em linha reta

city_coordinates = {
    'Arad': (46.18, 21.31),
    'Zerind': (46.62, 21.51),
    'Oradea': (47.06, 21.94),
    'Sibiu': (45.80, 24.13),
    'Timisoara': (45.75, 21.23),
    'Lugoj': (45.69, 21.90),
    'Mehadia': (44.90, 22.36),
    'Drobeta': (44.63, 22.66),
    'Craiova': (44.33, 23.80),
    'Rimnicu Vilcea': (45.10, 24.37),
    'Fagaras': (45.84, 24.98),
    'Pitesti': (44.85, 24.87),
    'Bucharest': (44.43, 26.10),
    'Giurgiu': (43.90, 25.97),
    'Urziceni': (44.72, 26.64),
    'Hirsova': (44.67, 27.94),
    'Eforie': (44.05, 28.64),
    'Vaslui': (46.64, 27.72),
    'Iasi': (47.15, 27.58),
    'Neamt': (46.98, 26.37)
}

print("Romania Map Data:")
print(map_data)
print("\nRomania City Coordinates:")
print(city_coordinates)


#%%
# Escolha uma cidade de início e uma cidade de destino no mapa da Romênia
# start_city_romania = 'Arad'
# goal_city_romania = 'Bucharest'

start_city_romania = 'Bucharest'
goal_city_romania = 'Arad'

# Execute a pesquisa A* no mapa da Romênia
cost_romania, path_romania = astar_search(map_data, city_coordinates,
                                          start_city_romania, goal_city_romania)

if path_romania:
    print(f"\nShortest path from {start_city_romania} to {goal_city_romania}: {path_romania}")
    print(f"Total cost: {cost_romania}")
else:
    print(f"\nNo path found from {start_city_romania} to {goal_city_romania}")



#%%
## Visualize o mapa da Romênia e o caminho

#  Criar um grafo
G_romania = nx.Graph()

# Adicionar nós com posições
for city, pos in city_coordinates.items():
    G_romania.add_node(city, pos=pos)

# Adicionar arestas
for city, neighbors in map_data.items():
    for neighbor, distance in neighbors.items():
        G_romania.add_edge(city, neighbor, weight=distance)

# Criar lista de cores de arestas
edge_colors_romania = []
for u, v in G_romania.edges():
    if path_romania and ((u in path_romania and v in path_romania and abs(path_romania.index(u) - path_romania.index(v)) == 1) or (v in path_romania and u in path_romania and abs(path_romania.index(v) - path_romania.index(u)) == 1)):
        edge_colors_romania.append('red')
    else:
        edge_colors_romania.append('gray')

# Criar lista de cores de nós
node_colors_romania = []
for node in G_romania.nodes():
    if path_romania and node in path_romania:
        node_colors_romania.append('red')
    else:
        node_colors_romania.append('gray')

# Desenhe o grafo
plt.figure(figsize=(12, 10))
pos_romania = nx.get_node_attributes(G_romania, 'pos')
nx.draw(G_romania, pos_romania, with_labels=True, node_color=node_colors_romania,
        edge_color=edge_colors_romania, node_size=700, font_size=10, alpha=0.8)

# Exibir o gráfico
plt.title("Romania Map with Shortest Path (A* Search)")
plt.show()

# %%
