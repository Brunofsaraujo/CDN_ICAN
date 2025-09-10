% EXECUTAR NO SITE https://swish.swi-prolog.org/
% QUE TEM O COMPILADOR PROLOG
% USANDO Create a [Program] = botão azul
% COPIAR E COLAR ESTE CÓDIGO

:- dynamic cidade/2.

% Carregar os dados do grafo
cidade('Arad', ['Zerind': 75, 'Timisoara': 118, 'Sibiu': 140]).
cidade('Zerind', ['Arad': 75, 'Oradea': 71]).
cidade('Oradea', ['Zerind': 71, 'Sibiu': 151]).
cidade('Sibiu', ['Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80]).
cidade('Timisoara', ['Arad': 118, 'Lugoj': 111]).
cidade('Lugoj', ['Timisoara': 111, 'Mehadia': 70]).
cidade('Mehadia', ['Lugoj': 70, 'Drobeta': 75]).
cidade('Drobeta', ['Mehadia': 75, 'Craiova': 120]).
cidade('Craiova', ['Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138]).
cidade('Rimnicu Vilcea', ['Sibiu': 80, 'Craiova': 146, 'Pitesti': 97]).
cidade('Fagaras', ['Sibiu': 99, 'Bucharest': 211]).
cidade('Pitesti', ['Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101]).
cidade('Bucharest', ['Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85]).
cidade('Giurgiu', ['Bucharest': 90]).
cidade('Urziceni', ['Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142]).
cidade('Hirsova', ['Urziceni': 98, 'Eforie': 86]).
cidade('Eforie', ['Hirsova': 86]).
cidade('Vaslui', ['Urziceni': 142, 'Iasi': 92]).
cidade('Iasi', ['Vaslui': 92, 'Neamt': 87]).
cidade('Neamt', ['Iasi': 87]).

% Definir o predicado para encontrar o caminho
caminho(Origem, Destino, Caminho) :-
    dfs(Origem, Destino, [Origem], Caminho).

% Algoritmo de busca em profundidade (DFS)
dfs(Cidade, Cidade, Caminho, Caminho).
dfs(Cidade, Destino, [Cidade|Caminho], Resultado) :-
    cidade(Cidade, Ligacoes),
    member(Destino1: _, Ligacoes),
    \+ member(Destino1, [Cidade|Caminho]),
    dfs(Destino1, Destino, [Destino1, Cidade|Caminho], Resultado).

% Testar o predicado
% EXECUTAR NO QUADRO ?- À DIREITA EMBAIXO
% caminho('Arad', 'Bucharest', Caminho).
% ?- caminho('Arad', 'Bucharest', Caminho).
