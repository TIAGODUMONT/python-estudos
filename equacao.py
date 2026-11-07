# Instalação (rodar no terminal do VS Code, não aqui no arquivo):
#   pip install -q -U watermark scikit-learn seaborn matplotlib joblib

import re
import unicodedata

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from watermark import watermark

# Versões das bibliotecas usadas (o %watermark do Jupyter, em versão .py)
print(watermark(author="Tiago Dumont", packages="numpy,pandas,sklearn,seaborn,matplotlib,joblib"))

"""
CONTEXTO DO PROJETO

Este projeto tem como propósito desenvolver um modelo de classificação automática de
sentimentos em textos, aplicando conceitos fundamentais de Python, Machine Learning e
MLOps.
A iniciativa parte de um problema de negócio: uma empresa de e-commerce que deseja
automatizar a análise de feedbacks de clientes para reduzir custos, aumentar a eficiência e
acelerar a tomada de decisão.
O trabalho é estruturado de forma modular, cobrindo todas as etapas do ciclo de vida de
um projeto de Ciência de Dados. Após a definição do problema e objetivos, o script realiza a
importação das bibliotecas essenciais (Pandas, Scikit-learn, Seaborn, entre outras) e o
carregamento dos dados a partir de um arquivo CSV contendo reviews de produtos. Em seguida,
conduz uma análise exploratória detalhada (EDA) para compreender a distribuição dos
sentimentos e verificar a presença de valores ausentes.
Na etapa de limpeza de dados, é implementada uma função de normalização de texto
(remoção de acentos, pontuações e caracteres especiais), preparando o conteúdo textual para a
engenharia de atributos, onde as classes “positivo” e “negativo” são mapeadas para rótulos
numéricos (1 e 0). O conjunto de dados é então dividido em amostras de treino e teste para
garantir uma avaliação correta da performance do modelo.
O núcleo do projeto é o pipeline de modelagem preditiva, que integra três componentes
principais em um único objeto Python:
- TF-IDF Vectorizer para transformar o texto em representações numéricas;
- StandardScaler para padronização dos vetores esparsos;
- Logistic Regression como algoritmo de classificação supervisionada.
O modelo é otimizado com GridSearchCV, explorando combinações de hiperparâmetros
para maximizar a acurácia. Após o treinamento, o desempenho é avaliado por meio de métricas
como Acurácia, Precisão, Recall e F1-Score, além da visualização da matriz de confusão. O modelo
final é então salvo em disco com a biblioteca joblib, permitindo reuso e integração com sistemas
externos.
Por fim, o projeto inclui uma simulação de deploy (MLOps), utilizando uma função que
carrega o modelo treinado e classifica novos reviews de forma automática. Essa fase demonstra
como o modelo poderia ser integrado em pipelines reais de produção, entregando valor imediato
para as áreas de marketing, suporte e gestão da experiência do cliente.
Trata-se de um projeto completo de Data Science para análise de sentimentos, que
combina teoria e prática em Python, abordando desde o tratamento de dados até a automação
de predições, com uma estrutura profissional alinhada às boas práticas de Data Science e
Machine Learning.
Além de todo o aprendizado técnico, o projeto proporciona uma compreensão prática de como aplicar conceitos de Machine Learning e MLOps em cenários reais de negócio, fortalecendo habilidades essenciais para profissionais de Data Science.
"""


# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================
df = pd.read_csv("dados/reviews.csv")
print("\nPrimeiras linhas:")
print(df.head())
print(f"\nFormato: {df.shape[0]} linhas x {df.shape[1]} colunas")

# ============================================================
# 2. ANÁLISE EXPLORATÓRIA (EDA)
# ============================================================
print("\nTipos das colunas:")
print(df.dtypes)

print("\nValores ausentes por coluna:")
print(df.isna().sum())

print("\nDistribuição dos sentimentos:")
print(df["sentimento"].value_counts())
print(df["sentimento"].value_counts(normalize=True).round(3))

# Gráfico da distribuição (salvo em arquivo para não travar o script)
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="sentimento", hue="sentimento", palette=["#2ecc71", "#e74c3c"])
plt.title("Distribuição dos Sentimentos")
plt.tight_layout()
plt.savefig("graficos_sentimento_distribuicao.png")
plt.close()

# ============================================================
# 3. LIMPEZA DOS DADOS
# ============================================================
# Remove as linhas sem texto de review
df = df.dropna(subset=["review"]).copy()


def limpar_texto(texto: str) -> str:
    """Deixa o texto em minúsculas, sem acentos, pontuação ou caracteres especiais."""
    texto = texto.lower()
    # remove acentos: "péssimo" -> "pessimo"
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    # mantém só letras, números e espaços
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    # troca vários espaços por um só
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


df["review_limpo"] = df["review"].apply(limpar_texto)
print("\nAntes e depois da limpeza:")
print(df[["review", "review_limpo"]].head())

# ============================================================
# 4. ENGENHARIA DE ATRIBUTOS
# ============================================================
# positivo -> 1, negativo -> 0
df["label"] = df["sentimento"].map({"positivo": 1, "negativo": 0})

X = df["review_limpo"]
y = df["label"]

# 80% treino, 20% teste; stratify mantém a mesma proporção de classes nos dois
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTreino: {len(X_treino)} reviews | Teste: {len(X_teste)} reviews")

# ============================================================
# 5. PIPELINE DE MODELAGEM
# ============================================================
pipeline = Pipeline(
    [
        ("tfidf", TfidfVectorizer()),  # texto -> números
        ("scaler", StandardScaler(with_mean=False)),  # with_mean=False: obrigatório para matriz esparsa
        ("modelo", LogisticRegression(max_iter=1000)),  # classificador
    ]
)

# ============================================================
# 6. OTIMIZAÇÃO COM GRIDSEARCHCV
# ============================================================
parametros = {
    "tfidf__ngram_range": [(1, 1), (1, 2)],  # palavras soltas ou pares de palavras
    "tfidf__max_features": [500, 1000],
    "modelo__C": [0.1, 1, 10],  # força da regularização
}

grid = GridSearchCV(pipeline, parametros, cv=5, scoring="accuracy", n_jobs=-1)
grid.fit(X_treino, y_treino)

print("\nMelhores hiperparâmetros:", grid.best_params_)
print(f"Melhor acurácia na validação cruzada: {grid.best_score_:.3f}")

modelo_final = grid.best_estimator_

# ============================================================
# 7. AVALIAÇÃO DO MODELO
# ============================================================
y_previsto = modelo_final.predict(X_teste)

print("\nMétricas no conjunto de teste:")
print(f"Acurácia : {accuracy_score(y_teste, y_previsto):.3f}")
print(f"Precisão : {precision_score(y_teste, y_previsto):.3f}")
print(f"Recall   : {recall_score(y_teste, y_previsto):.3f}")
print(f"F1-Score : {f1_score(y_teste, y_previsto):.3f}")

print("\nRelatório completo:")
print(classification_report(y_teste, y_previsto, target_names=["negativo", "positivo"]))

matriz = confusion_matrix(y_teste, y_previsto)
plt.figure(figsize=(5, 4))
sns.heatmap(
    matriz,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["negativo", "positivo"],
    yticklabels=["negativo", "positivo"],
)
plt.xlabel("Previsto")
plt.ylabel("Real")
plt.title("Matriz de Confusão")
plt.tight_layout()
plt.savefig("graficos_sentimento_matriz_confusao.png")
plt.close()

# ============================================================
# 8. SALVAR O MODELO
# ============================================================
joblib.dump(modelo_final, "modelo_sentimento.pkl")
print("\nModelo salvo em modelo_sentimento.pkl")

# ============================================================
# 9. SIMULAÇÃO DE DEPLOY (MLOps)
# ============================================================


def classificar_reviews(novos_reviews: list[str], caminho_modelo: str = "modelo_sentimento.pkl") -> list[str]:
    """Carrega o modelo salvo e classifica novos reviews como positivo ou negativo."""
    modelo = joblib.load(caminho_modelo)
    textos_limpos = [limpar_texto(r) for r in novos_reviews]
    previsoes = modelo.predict(textos_limpos)
    return ["positivo" if p == 1 else "negativo" for p in previsoes]


novos = [
    "Produto excelente, chegou rápido e funciona muito bem!",
    "Veio quebrado e o atendimento foi péssimo.",
    "Gostei bastante, recomendo.",
    "Não funciona, quero devolver.",
]

print("\nClassificando novos reviews:")
for review, sentimento in zip(novos, classificar_reviews(novos)):
    print(f"[{sentimento:8}] {review}")
