#%% bibliotecas
import numpy as np
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

#%% Carregar o dataset Iris
iris = load_iris()
X = iris.data   # numpy.ndarray, não dataframe pandas
X = pd.DataFrame(X)   # transforma array em dataframe
X.columns = iris.feature_names   # inclui cabeçalhos
X.head()
# print(X)

#%% # Criar um pairplot dos dados não escalados
plt.figure(figsize=(10, 8))
sns.pairplot(data=X, vars=iris.feature_names)  
            # , hue=iris.target_names[iris.target])
    ## excluidos os targets, pois é aprend ñ superv.
plt.suptitle('Pairplot dos Dados Não Escalados', y=1.02)
plt.show()

#%% Escalar os dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# print(X_scaled)

#%% # Criar um pairplot dos dados escalados
X_df = pd.DataFrame(X_scaled)   # converte array para dataframe
X_df.columns = iris.feature_names   # inclui cabeçalhos
print(X_df.head())

plt.figure(figsize=(10, 8))
sns.pairplot(data=X_df, vars=iris.feature_names)  
            # , hue=iris.target_names[iris.target])
    ## excluidos os targets, pois é aprend ñ superv.
plt.suptitle('Pairplot dos Dados Escalados', y=1.02)
plt.show()

#%% Agrupamento k-means  - nº ótimo de clusters

wcss=[]   # Within-Cluster Sum of Squares (WCSS).
# O WCSS mede o grau de agrupamento dos pontos de dados em torno 
# de seus respectivos centroides. Ele é definido como a soma das 
# distâncias quadradas entre cada ponto e seu centroide de agrupamento:
silhouette = []    # Silhouette score
K_RANGE = range(2, 9)

for k in K_RANGE:
    kmeans = KMeans(n_clusters=k, random_state=0, max_iter=300)
    kmeans.fit(X_scaled)
    silhouette.append(silhouette_score(X_scaled, kmeans.labels_))    
    wcss.append(kmeans.inertia_)
    ## A inércia é a soma das distâncias quadradas de cada ponto de 
    ## dados até o centro de cluster mais próximo. É essencialmente o 
    ## erro quadrático total do agrupamento. Um valor de inércia menor 
    ## sugere um agrupamento melhor.

#%% Análise pela regra do cotovelo (elbow method)
plt.figure(figsize=(6, 4))
plt.plot(K_RANGE, wcss, marker='o')
plt.title("Método do Cotovelo")
plt.xlabel("Número de clusters (k)")
plt.ylabel("WCSS")
plt.xticks(K_RANGE)
plt.show()

    ## note que a partir de n=4, a curva suaviza
    ## uma boa escolha é n=3 (última quebra pronunciada)

#%% ----- 4.2 Gráfico do Silhouette -----
plt.figure(figsize=(6, 4))
plt.plot(K_RANGE, silhouette, marker='o', color='green')
plt.title("Silhouette Score")
plt.xlabel("Número de clusters (k)")
plt.ylabel("Silhouette")
plt.xticks(K_RANGE)
plt.show()

#%% Escolha automática do melhor k (máximo silhouette)
best_k = K_RANGE[np.argmax(silhouette)]
print(f"Melhor número de clusters (máximo silhouette): {best_k}")

#%% aplicando o classificador k-means aos dados

# Recuperar os dados não escalados
X_orig = scaler.inverse_transform(X_scaled)

# usar best_k determinado pela regra do cotovelo
kmeans = KMeans(n_clusters=3, random_state=0, max_iter=300)
kmeans.fit(X_orig)
y_prev = kmeans.fit_predict(X_orig)

# Obter os centroides (após fit)
centroids = kmeans.cluster_centers_
print(centroids)

#%% # Criar um pairplot dos dados não escalados
X['target'] = iris.target
X['target_name'] = iris.target_names[iris.target]

plt.figure(figsize=(10, 8))
sns.pairplot(data=X, vars=iris.feature_names, hue='target_name')
plt.suptitle('Pairplot dos Dados Não Escalados com Centroides', y=1.02)
plt.show()

#%% # Visualização dos clusters
cols = X.columns
plt.scatter(X.loc[y_prev == 0, cols[0]],
            X.loc[y_prev == 0, cols[1]],
            s=100, c='purple',
            label='Iris-setosa')
plt.scatter(X.loc[y_prev == 1, cols[0]],
            X.loc[y_prev == 1, cols[1]],
            s=100, c='orange',
            label='Iris-versicolour')
plt.scatter(X.loc[y_prev == 2, cols[0]],
            X.loc[y_prev == 2, cols[1]],
            s=100, c='green',
            label='Iris-virginica')

# Plotting the centroids of the clusters
plt.scatter(kmeans.cluster_centers_[:, 0],
            kmeans.cluster_centers_[:, 1],
            s=100, c='red', marker='^',
            label='Centroids')

plt.xlabel(X.columns[0])
plt.ylabel(X.columns[1])

plt.legend()
plt.show()


#%%
