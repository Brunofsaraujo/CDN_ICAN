#%% ------------------------------------------------------------
#  Clustering dos veículos (colunas A‑D) – script completo
# ------------------------------------------------------------
#  • Normalização (z‑score)
#  • K‑means com escolha automática do número de clusters
#      – método do cotovelo
#      – silhouette score
#  • Cálculo e denormalização dos centróides
#  • Visualizações:
#        • pairplot dos dados brutos
#        • gráfico do cotovelo
#        • gráfico do silhouette
#        • pairplot colorido por cluster (inclui centróides)
# ------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

#%% ------------------------------
# 1. Dados
# ------------------------------

#  Leitura automática da planilha (colunas A‑D)

# 1. Caminho do arquivo – pode ser .xlsx ou .csv
arquivo = "autom.xlsx"          # ajuste se for .csv

# 2. Detecta a extensão e usa a função apropriada
if arquivo.lower().endswith(".xlsx"):
    # lê apenas as colunas A‑D (índices 0‑3) e ignora linhas vazias
    df = pd.read_excel(arquivo, usecols="A:D", engine="openpyxl")
else:   # .csv ou .txt
    df = pd.read_csv(arquivo, usecols=[0, 1, 2, 3])

# 3. Renomeia as colunas para facilitar o código (se necessário)
df.columns = ["automovel", "peso_kg", "potencia_cv", "bagagem_L"]

# 4. Verifica rapidamente o carregamento
print(df.head())
print(f"Número de linhas carregadas: {len(df)}")

#%% ------------------------------
# 2. Pairplot dos dados brutos (sem clusters)
# ------------------------------
sns.pairplot(df[["peso_kg", "potencia_cv", "bagagem_L"]])
plt.suptitle("Pairplot dos atributos (sem clusters)", y=1.02)
plt.show()

#%% ------------------------------
# 3. Normalização (z‑score)
# ------------------------------
features = ["peso_kg", "potencia_cv", "bagagem_L"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

#%% ------------------------------
# 4. Determinação do número ótimo de clusters
# ------------------------------
wcss = []          # Within‑Cluster Sum of Squares (cotovelo)
silhouette = []    # Silhouette score
K_RANGE = range(2, 9)

for k in K_RANGE:
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(X_scaled)
    wcss.append(km.inertia_)
    silhouette.append(silhouette_score(X_scaled, km.labels_))

#%% ----- 4.1 Gráfico do cotovelo -----
plt.figure(figsize=(6, 4))
plt.plot(K_RANGE, wcss, marker='o')
plt.title("Método do Cotovelo")
plt.xlabel("Número de clusters (k)")
plt.ylabel("WCSS")
plt.xticks(K_RANGE)
plt.show()

#%% ----- 4.2 Gráfico do Silhouette -----
plt.figure(figsize=(6, 4))
plt.plot(K_RANGE, silhouette, marker='o', color='orange')
plt.title("Silhouette Score")
plt.xlabel("Número de clusters (k)")
plt.ylabel("Silhouette")
plt.xticks(K_RANGE)
plt.show()

#%% Escolha automática do melhor k (máximo silhouette)
best_k = K_RANGE[np.argmax(silhouette)]
print(f"Melhor número de clusters (máximo silhouette): {best_k}")


#%% ------------------------------
# 5. K‑means final com best_k
# ------------------------------
kmeans = KMeans(n_clusters=best_k, n_init=10, random_state=42)

df["cluster"] = kmeans.fit_predict(X_scaled).astype(str)

# ----- Denormalização dos centróides -------------------------
centroids_scaled = kmeans.cluster_centers_
centroids_denorm = scaler.inverse_transform(centroids_scaled)

centroids_df = pd.DataFrame(centroids_denorm, columns=features)
centroids_df["cluster"] = [str(i) for i in range(best_k)]   # mesma label do cluster
centroids_df["automovel"] = "centroide"

# ------------------------------------------------------------
#  Pairplot dos veículos (hue = cluster)
# ------------------------------------------------------------
sns.set(style="whitegrid")
pair = sns.pairplot(
    df,
    vars=features,
    hue="cluster",
    palette="Set2",          # paleta que será reutilizada
    diag_kind="kde"
)

# ------------------------------------------------------------
#  Sobre‑posição dos centróides (X) com a cor do seu cluster
# ------------------------------------------------------------
# Recupera a paleta que o seaborn usou (mapeamento label → cor)
palette = pair._legend_data   # dicionário {label: <matplotlib Patch>}
# Converte para {label: cor_hex}
color_map = {}
for lbl, handle in palette.items():
    # handle pode ser Line2D (usado para marcadores) ou Patch (usado para
    # áreas preenchidas). Ambos têm um método que devolve a cor.
    if hasattr(handle, "get_facecolor"):          # Patch
        color_map[lbl] = handle.get_facecolor()
    elif hasattr(handle, "get_color"):            # Line2D
        color_map[lbl] = handle.get_color()
    else:
        raise TypeError(f"Handle for label '{lbl}' has no colour method")

# Cada eixo do pairplot é um AxesSubplot; percorremos linhas/colunas
crossSize = 40; borda = 0.3         # para as cruzes
for i, row_var in enumerate(features):
    for j, col_var in enumerate(features):
        ax = pair.axes[i, j]

        # Só plotamos X nos subgráficos que não são a diagonal
        if i != j:
            # Para cada cluster, plota o centróide correspondente
            for _, cent in centroids_df.iterrows():
                cl = cent["cluster"]
                ax.scatter(
                    cent[col_var],          # x‑value
                    cent[row_var],          # y‑value
                    marker="X",
                    s=crossSize,                  # tamanho do X
                    color=color_map[cl],
                    edgecolor="black",
                    linewidth=borda,
                    zorder=5                # garante que fique acima dos pontos
                )
        else:
            # Diagonal (kde) – opcionalmente marcamos o X também
            for _, cent in centroids_df.iterrows():
                cl = cent["cluster"]
                ax.scatter(
                    cent[col_var],
                    0,                     # y‑valor irrelevante (não será exibido)
                    marker="X",
                    s=crossSize,
                    color=color_map[cl],
                    edgecolor="black",
                    linewidth=borda,
                    zorder=5
                )

pair.fig.suptitle("Pairplot por cluster – X = centróides (mesma cor)", y=1.02)
plt.show()

# %%
# [markdown]
# ### Interpretação dos "grandes"clusters
# Onde cada "grande" funde dois em dois
# Cluster	Características típicas	Veículos representativos
# 1	Peso alto, potência moderada‑alta, bagagem grande.	A, E, F, I, J, M
# 2	Peso médio, potência média, bagagem média.	B, C, H, L
# 3	Peso baixo, potência baixa‑média, bagagem variada (moderada a alta).	D, G, K
# 
# Esses grupos podem ser úteis, por exemplo, para segmentar veículos em campanhas de marketing ou para definir faixas de preço baseadas em capacidade de carga e desempenho.
