% EXECUTAR NO SITE https://swish.swi-prolog.org/
% QUE TEM O COMPILADOR PROLOG
% USANDO Create a [Program] = botão azul
% COPIAR E COLAR ESTE CÓDIGO


hanoi(N) :- move(N, esquerdo, central, direito).

move(0, _, _, _) :- !.

move(N, A, B, C) :-
    M is N - 1,
    move(M, A, C, B),
    inform(A, B),
    move(M, C, B, A).

inform(X, Y) :-
    format('Mova o disco do pino ~w para o pino ~w.~n', [X, Y]).
