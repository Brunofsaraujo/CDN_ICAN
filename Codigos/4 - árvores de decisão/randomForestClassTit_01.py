# TITANIC RANDOM FOREST COM GRÁFICO COMBINADO

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# === Carregar dados ===
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic_data = pd.read_csv(url)

# Pré-processamento
titanic_data = titanic_data.dropna(subset=['Survived'])
X = titanic_data[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare']]
y = titanic_data['Survived']

# Converter 'Sex' para numérico
X['Sex'] = X['Sex'].map({'female': 0, 'male': 1})

# Preencher valores nulos em 'Age' com mediana
X['Age'].fillna(X['Age'].median(), inplace=True)

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Treinar modelo ===
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Avaliação
y_pred = rf_classifier.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Matriz de confusão:\n", confusion_matrix(y_test, y_pred))

# Previsão de um exemplo
sample = X_test.iloc[0:1]
prediction = rf_classifier.predict(sample)
print(f"\nSample Passenger: {sample.iloc[0].to_dict()}")
print(f"Predicted Survival: {'Survived' if prediction[0] == 1 else 'Did Not Survive'}")

# === Importância das features ===
importances = rf_classifier.feature_importances_
feature_names = X.columns
sorted_indices = importances.argsort()[::-1]
sorted_features = [feature_names[i] for i in sorted_indices]
sorted_importances = importances[sorted_indices]

# === Gráfico combinado ===
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Heatmap de correlação
sns.heatmap(X.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=axes[0])
axes[0].set_title("Correlação entre Features")

# Gráfico horizontal de importância
bars = axes[1].barh(sorted_features, sorted_importances, color='skyblue')
axes[1].set_xlabel("Importância")
axes[1].set_title("Importância das Features - Random Forest")
axes[1].invert_yaxis()

# Adicionar valores numéricos nas barras
for bar in bars:
    width = bar.get_width()
    axes[1].text(width + 0.005, bar.get_y() + bar.get_height()/2,
                 f"{width:.3f}", va='center')

plt.tight_layout()
plt.savefig("titanic_feature_analysis.png")
plt.show()
