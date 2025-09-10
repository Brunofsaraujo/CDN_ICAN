% EXECUTAR NO SITE https://swish.swi-prolog.org/
% QUE TEM O COMPILADOR PROLOG
% USANDO Create a [Program] = botão azul
% COPIAR E COLAR ESTE CÓDIGO


% Definir a relação pai
pai(joao, maria).
pai(joao, ana).
pai(jose, joao).
pai(jose, pedro).
pai(antonio, jose).

% Definir a relação mãe
mae(maria, carla).
mae(maria, josefina).
mae(ana, julia).
mae(ana, jessica).
mae(josefina, joaozinho).

% Definir a relação filho
filho(X, Y) :- pai(Y, X); mae(Y, X).


% Exemplos de consulta

% ?- pai(joao, maria).
% true.

% ?- filho(X,maria).
% X = carla
% X = josefina
