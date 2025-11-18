
#%% [markdown]
# ## Sem train-test split:
#
# Usar **todo o dataset para treinar e avaliar** (sem divisão em treino e teste) tem impactos importantes:
# 
# ---
# 
# ### ✅ **Vantagens**
# 1. **Simplicidade**:
#    - Não há necessidade de gerenciar splits ou validação cruzada.
#    - Útil para datasets muito pequenos (como exemplos didáticos).
# 
# 2. **Visualização completa**:
#    - A árvore gerada reflete **todos os dados disponíveis**, sem deixar nada de fora.
#    - Bom para fins explicativos ou para gerar regras completas.
# 
# ---
# 
# ### ⚠️ **Desvantagens**
# 1. **Overfitting extremo**:
#    - O modelo memoriza os dados, atingindo acurácia **100%** no próprio dataset.
#    - Não indica capacidade de generalização para novos dados.
# 
# 2. **Métricas enganosas**:
#    - Acurácia e F1-score serão **infladas**.
#    - Não é possível avaliar desempenho real em dados não vistos.
# 
# 3. **Risco em produção**:
#    - Árvores muito complexas, com regras específicas para cada exemplo.
#    - Baixa robustez para casos novos.
# 
# ---
# 
# ### ✅ **Quando faz sentido**
# - **Exercícios acadêmicos** (como o exemplo do “Jogar Tênis”).
# - **Explicação de algoritmos** (ID3 vs CART).
# - **Geração de regras completas** para análise exploratória.
# 
# ---
# 
# ### ✅ **Alternativa recomendada**
# - Usar **train/test split** ou **validação cruzada** para medir generalização.
# - Ou aplicar **poda** nas árvores para reduzir complexidade.
# 
# ---


import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

#%%
#  === CONFIGURAÇÃO ===
# file_path = "seu_arquivo.csv"        # Caminho do CSV
# target_column = "nome_da_coluna_y"   # Coluna alvo
# ignore_columns = ["coluna_id1", "coluna_id2", "coluna_id3",...]       # Colunas para desprezar

file_path = "jogarTenis.csv"        # Caminho do CSV
target_column = "Joga"   # Coluna alvo
ignore_columns = ["Dia"]       # Colunas para desprezar

# === LEITURA DO CSV ===
df = pd.read_csv(file_path)
print("Colunas disponíveis:", df.columns.tolist())

# Remove colunas irrelevantes
df = df.drop(columns=[c for c in ignore_columns if c in df.columns])

#%%
#  === SEPARAÇÃO DE FEATURES E TARGET ===
X = df.drop(columns=[target_column])
y = df[target_column]
print(X.head(),'\n')
print(y.head(),'\n')

#%%
#  Detecta tipo da coluna alvo
target_is_nominal = y.dtype == 'object'

# Se alvo for nominal, aplica LabelEncoder
if target_is_nominal:
    enc_target = LabelEncoder()    # ok se classe binária S/N, V/F
    y_encoded = enc_target.fit_transform(y)
else:
    y_encoded = y.values

#%%
#  === ID3 (Entropia) ===
X_id3 = X.copy()
encoders = {}
# Se alguma coluna for nominal, aplica OneHotEncoder    #LabelEncoder
enc2 = OneHotEncoder(sparse_output=False)
for col in X_id3.columns:
    if X_id3[col].dtype == 'object':
        transf = enc2.fit_transform(X_id3[col].to_frame())
        transf_df = pd.DataFrame(transf, 
                                 columns = enc2.get_feature_names_out([col]), 
                                 index=X_id3.index)
        
        # Remove a coluna original e adiciona as novas
        X_id3 = X_id3.drop(columns=[col])
        X_id3 = pd.concat([X_id3, transf_df], axis=1)
        
        encoders[col] = enc2

id3_model = DecisionTreeClassifier(criterion="entropy")
id3_model.fit(X_id3, y_encoded)

#%% Avaliação ID3
id3_preds = id3_model.predict(X_id3)
print("\n=== Métricas ID3 ===")
print("Acurácia:", accuracy_score(y_encoded, id3_preds))
print(classification_report(y_encoded, id3_preds, 
            target_names=(enc_target.classes_ if target_is_nominal else None)))

#%%
#  Mostra árvore ID3
plt.figure(figsize=(12, 6))
plot_tree(id3_model, feature_names=X_id3.columns, 
            class_names=(enc_target.classes_ if target_is_nominal else None), filled=True)
plt.title("ID3 Decision Tree (Entropy)")
plt.savefig("id3_tree.png")
plt.show()

#%%
#  Exporta regras ID3 com valores originais
# Se encoder for binário 0=FALSO e 1=VERDADEIRO
# <= 0.50 --> FALSO
# > 0.50 --> VERDADEIRO

id3_rules_raw = export_text(id3_model, feature_names=list(X_id3.columns))
id3_rules_lines = id3_rules_raw.split('\n')
id3_rules_nominal = []

for line in id3_rules_lines:
    for col, enc in encoders.items():
        if hasattr(enc, 'classes_'):  # LabelEncoder
            for i, cls in enumerate(enc.classes_):
                line = line.replace(f"{col} <= {i}", f"{col} <= {i} ( -> '{col}' é '{cls}' ou anterior)")
                line = line.replace(f"{col} > {i}", f"{col} > {i} ( -> '{col}' é posterior a '{cls}')")
        elif hasattr(enc, 'categories_'):  # OneHotEncoder
            categorias = enc.categories_[0]
            for cls in categorias:
                line = line.replace(f"{col}_{cls} <= 0.5", f"{col}_{cls} <= 0.5 (-> '{col}' ≠ '{cls}')")
                line = line.replace(f"{col}_{cls} > 0.5", f"{col}_{cls} > 0.5 (-> '{col}' == '{cls}')")

    if target_is_nominal and enc_target is not None:
        for i, cls in enumerate(enc_target.classes_):
            line = line.replace(f"class: {i}", f"class: {i} ( -> classe: '{cls}')")

    id3_rules_nominal.append(line)

id3_rules_text = "\n".join(id3_rules_nominal)
print("\nRegras ID3:\n", id3_rules_text)
with open("id3_rules.txt", "w", encoding="utf-8") as f:
    f.write("Regras ID3 (formato IF-THEN):\n")
    f.write(id3_rules_text)

#%%
#  === CART (Gini) ===
categorical_features = X.select_dtypes(include=['object']).columns.tolist()
numerical_features = X.select_dtypes(exclude=['object']).columns.tolist()

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(), categorical_features),
    ("num", "passthrough", numerical_features)
], remainder="drop")

cart_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", DecisionTreeClassifier(criterion="gini"))
])
cart_pipeline.fit(X, y_encoded)

# Avaliação CART
cart_preds = cart_pipeline.predict(X)
print("\n=== CART Métricas ===")
print("Acurácia:", accuracy_score(y_encoded, cart_preds))
print(classification_report(y_encoded, cart_preds, 
            target_names=(enc_target.classes_ if target_is_nominal else None)))

# Feature names após OneHotEncoding
# constrói o atributo (feature) e seu valor para colocar no nó da árvore
encoded_feature_names = []
if categorical_features:
    encoded_feature_names.extend(
        cart_pipeline.named_steps["preprocessor"].named_transformers_["cat"].get_feature_names_out(categorical_features)
    )
encoded_feature_names.extend(numerical_features)

#%%
#  Mostra árvore CART
plt.figure(figsize=(12, 6))
plot_tree(cart_pipeline.named_steps["classifier"], 
          feature_names=encoded_feature_names, 
          class_names=(enc_target.classes_ if target_is_nominal else None), 
          filled=True)
plt.title("CART Decision Tree (Gini)")
plt.savefig("cart_tree.png")
plt.show()

#%%
#  Exporta regras CART
cart_rules = export_text(cart_pipeline.named_steps["classifier"], 
                        feature_names=list(encoded_feature_names))
cart_rules_named = cart_rules
if target_is_nominal:
    for i, cls in enumerate(enc_target.classes_):
        cart_rules_named = cart_rules_named.replace(f"class: {i}", f"class: {cls}")

print("\nRegras CART:\n", cart_rules_named)
with open("cart_rules.txt", "w", encoding="utf-8") as f:
    f.write("CART Rules (IF-THEN format):\n")
    f.write(cart_rules_named)

print("\n✅ Árvores e regras salvas: id3_tree.png, cart_tree.png, id3_rules.txt, cart_rules.txt")

# %% [markdown]
# # O que significa esse `0.50` nas divisões da árvore de decisão.
# 
# ---
# 
# ### 🌳 Contexto: Árvore de Decisão com Variáveis Categóricas Codificadas
# 
# Quando você vê uma regra como:
# 
# ```
# |--- Aparencia_nublado <= 0.50
# ```
# 
# isso indica que a variável **`Aparencia_nublado`** foi transformada em uma **variável binária** (0 ou 1), provavelmente por **OneHotEncoder**.
# 
# #### O que significa `Aparencia_nublado <= 0.50`?
# 
# - O valor **`Aparencia_nublado`** é **0 ou 1**:
#   - `0` → a aparência **não é nublado**
#   - `1` → a aparência **é nublado**
# 
# Então:
# 
# - `Aparencia_nublado <= 0.50` → **não é nublado**
# - `Aparencia_nublado > 0.50` → **é nublado**
# 
# O valor `0.50` aparece porque o modelo está fazendo uma **divisão binária** entre 0 e 1. Como não há valores intermediários, o ponto de corte é `0.5`.
# 
# ---
# 
# ### 🧠 Por que não aparece `== 0` ou `== 1`?
# 
# Porque o `DecisionTreeClassifier` sempre usa **comparações numéricas** (`<=`, `>`) mesmo para variáveis binárias. Ele não sabe que `Aparencia_nublado` é uma variável categórica — só vê números.
# 
# ---
# 
# ### 🧪 Outros exemplos:
# 
# Se obtiver:
# 
# ```python
# |--- Vento_fraco <= 0.50
# ```
# 
# E `Vento_fraco` foi codificado como:
# 
# - `1` → vento é fraco
# - `0` → vento não é fraco
# 
# Então:
# 
# - `<= 0.50` → vento **não é fraco**
# - `> 0.50` → vento **é fraco**
# 
# ---
# 
# ### ✅ Conclusão:
# 
# O valor `0.50` é o **limite entre 0 e 1** usado para dividir variáveis binárias criadas por codificação (como OneHotEncoder). Ele **equivale a uma verificação booleana**:
# 
# - `<= 0.5` → valor é `0` (falso)
# - `> 0.5` → valor é `1` (verdadeiro)
# 
# ---


# %%
