"""Gera um CSV fictício de reviews de produtos (positivo/negativo) para o projeto de sentimentos."""

import numpy as np
import pandas as pd

np.random.seed(42)  # sempre os mesmos dados

produtos = ["fone de ouvido", "notebook", "celular", "tênis", "cafeteira", "mochila", "relógio", "teclado"]

inicio_pos = ["Adorei o", "Gostei muito do", "Excelente", "Recomendo o", "Muito bom o", "Superou minhas expectativas o"]
meio_pos = [
    "chegou antes do prazo",
    "a qualidade é ótima",
    "vale cada centavo",
    "funciona perfeitamente",
    "bem embalado e original",
    "atendimento nota 10",
]
fim_pos = ["!", "!!", ".", " :)", ", compraria de novo!", ", recomendo a todos."]

inicio_neg = ["Detestei o", "Não gostei do", "Péssimo", "Não recomendo o", "Muito ruim o", "Me arrependi de comprar o"]
meio_neg = [
    "chegou atrasado",
    "a qualidade é horrível",
    "veio com defeito",
    "parou de funcionar em uma semana",
    "veio diferente do anúncio",
    "atendimento péssimo",
]
fim_neg = ["!", "!!!", ".", " :(", ", quero meu dinheiro de volta!", ", nunca mais compro."]


def montar_review(positivo):
    if positivo:
        ini, meio, fim = inicio_pos, meio_pos, fim_pos
    else:
        ini, meio, fim = inicio_neg, meio_neg, fim_neg
    produto = np.random.choice(produtos)
    return f"{np.random.choice(ini)} {produto}, {np.random.choice(meio)}{np.random.choice(fim)}"


num_reviews = 1000
sentimentos = np.random.choice(["positivo", "negativo"], size=num_reviews, p=[0.6, 0.4])
reviews = [montar_review(s == "positivo") for s in sentimentos]

df = pd.DataFrame({"review": reviews, "sentimento": sentimentos})

# alguns valores ausentes de propósito, para a EDA encontrar
df.loc[np.random.choice(df.index, size=15, replace=False), "review"] = np.nan

df.to_csv("dados/reviews.csv", index=False, encoding="utf-8")
print(f"Arquivo dados/reviews.csv criado com {len(df)} reviews.")
print(df.head())
