% https://swish.swi-prolog.org/ 

% Definição das cores disponíveis
cor(vermelho).
cor(verde).
cor(azul).

% Fatos de vizinhança entre os estados do Sudeste
vizinho(sp, rj).
vizinho(sp, mg).
vizinho(rj, mg).
vizinho(mg, es).
vizinho(rj, es).

% Regra para garantir que estados vizinhos não tenham a mesma cor
% A regra member/2 em Prolog é usada para verificar se um elemento pertence a uma lista. 
% Ela também pode ser usada para iterar sobre os elementos da lista, usando 'forall'

restricoes(Estados) :-
    forall(vizinho(A, B),
           (member(A-CorA, Estados),	% par (A-CorA) é da lista?
            member(B-CorB, Estados),	% par (B-CorB) é da lista?
            CorA \= CorB)).		% se for diferente

% Regra principal para atribuir cores aos estados
colorir :-
    Estados = [sp-CorSP, rj-CorRJ, mg-CorMG, es-CorES],		% lista pares estado-cor
    cor(CorSP), cor(CorRJ), cor(CorMG), cor(CorES),		% atualiza cores por estado
    restricoes(Estados),		% verifica as restrições - se F, colorir fica F 
    format('São Paulo: ~w~n', [CorSP]),
    format('Rio de Janeiro: ~w~n', [CorRJ]),
    format('Minas Gerais: ~w~n', [CorMG]),
    format('Espírito Santo: ~w~n', [CorES]).
