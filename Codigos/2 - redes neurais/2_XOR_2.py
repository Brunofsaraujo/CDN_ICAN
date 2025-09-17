#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 23:22:36 2019

@author: waldemar
"""

#%% BIBLIOTECAS

from sklearn.neural_network import MLPClassifier

#%% CARGA DOS DADOS

X = [ [0,0], [0,1], [1,0], [1,1] ]
y = [0, 1, 1, 0]

#%% CONFIG REDE NEURAL

mlp = MLPClassifier(verbose=True, 
                    hidden_layer_sizes=(4,3), 
                    max_iter=10000, 
                    tol=1e-6, 
                    activation='relu')

#%% TREINAMENTO DA REDE

mlp.fit(X,y)      # executa treinamento - ver console

#%% teste
for caso in X :
    print('caso: ', caso, ' previsto: ', mlp.predict([caso]) )

'''
print( mlp.predict( [ [0,0] ] ) )
print( mlp.predict( [ [0,1] ] ) )
print( mlp.predict( [ [1,0] ] ) )
print( mlp.predict( [ [1,1] ] ) )
'''

#%% ALGUNS PARÂMETROS DA REDE

print("Classes = ", mlp.classes_)     # lista de classes
print("Erro = ", mlp.loss_)        # fator de perda (erro)
print("Amostras visitadas = ", mlp.t_)           # número de amostras de treinamento visitadas 
print("Atributos de entrada = ", mlp.n_features_in_)   # número de atributos de entrada (campos de X)
print("N ciclos = ", mlp.n_iter_)      # númerode iterações no treinamento
print("N de camadas = ", mlp.n_layers_)    # número de camadas da rede
print("Tamanhos das camadas ocultas: ", mlp.hidden_layer_sizes)
print("N de neurons saida = ", mlp.n_outputs_)   # número de neurons de saida
print("F de ativação = ", mlp.out_activation_)  # função de ativação utilizada

