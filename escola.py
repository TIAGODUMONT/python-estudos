# =============================================================
#  SIMULAÇÃO DE UMA ESCOLA: 1000 alunos, 10 turmas, 5 disciplinas
# =============================================================
#  Roteiro (organize as ideias ANTES de codar):
#   1. Configuração   -> os "números mágicos" ficam no topo
#   2. Alunos         -> nome, sexo e turma de cada um
#   3. Notas          -> 5 notas por aluno (0 a 10)
#   4. Média e situação -> média >= 6 é Aprovado
#   5. Estatísticas   -> média, mediana, moda, desvio padrão
#   6. Percentuais    -> aprovados x reprovados, meninos x meninas
#   7. Por turma      -> qual turma foi melhor
#   8. Salvar em CSV
# =============================================================

import numpy as np
import pandas as pd

# ---------- 1. CONFIGURAÇÃO ----------
QTD_ALUNOS = 1000
TURMAS = [f"Turma {letra}" for letra in "ABCDEFGHIJ"]  # 10 turmas
DISCIPLINAS = ["Matemática", "Português", "História", "Geografia", "Ciências"]
MEDIA_APROVACAO = 6.0

rng = np.random.default_rng(42)  # semente: o sorteio sai igual toda vez

# ---------- 2. ALUNOS ----------
alunos = pd.DataFrame({
    "aluno": [f"Aluno {i:04d}" for i in range(1, QTD_ALUNOS + 1)],  # Aluno 0001...
    "sexo": rng.choice(["Menino", "Menina"], size=QTD_ALUNOS),
    # np.repeat repete cada turma 100 vezes -> 100 alunos por turma
    "turma": np.repeat(TURMAS, QTD_ALUNOS // len(TURMAS)),
})

# ---------- 3. NOTAS ----------
# Distribuição normal: a maioria tira perto de 6,5; poucos tiram 0 ou 10.
notas = rng.normal(loc=6.5, scale=2.0, size=(QTD_ALUNOS, len(DISCIPLINAS)))
notas = np.clip(np.round(notas), 0, 10).astype(int)  # arredonda e trava entre 0 e 10
alunos[DISCIPLINAS] = notas  # cada coluna da matriz vira uma disciplina

# ---------- 4. MÉDIA E SITUAÇÃO ----------
alunos["media"] = alunos[DISCIPLINAS].mean(axis=1).round(2)  # axis=1 -> média da LINHA
alunos["aprovado"] = alunos["media"] >= MEDIA_APROVACAO       # True / False
alunos["situacao"] = np.where(alunos["aprovado"], "Aprovado", "Reprovado")

print("Primeiros alunos:")
print(alunos.head(), "\n")

# ---------- 5. ESTATÍSTICAS ----------
todas_as_notas = alunos[DISCIPLINAS].stack()  # as 5000 notas numa coluna só

print("=" * 45)
print("ESTATÍSTICAS DA ESCOLA")
print("=" * 45)
print(f"Média geral dos alunos:  {alunos['media'].mean():.2f}")
print(f"Mediana das médias:      {alunos['media'].median():.2f}")
print(f"Desvio padrão:           {alunos['media'].std():.2f}")
print(f"Maior média:             {alunos['media'].max():.2f}")
print(f"Menor média:             {alunos['media'].min():.2f}")
# mode() devolve uma lista, porque pode haver empate; [0] pega a primeira
print(f"Moda (nota mais comum):  {todas_as_notas.mode()[0]}")

print("\nMédia por disciplina:")
print(alunos[DISCIPLINAS].mean().round(2).to_string())

# ---------- 6. PERCENTUAIS ----------
# Truque: True vale 1 e False vale 0, então a MÉDIA de um True/False é a proporção.
pct_aprovados = alunos["aprovado"].mean() * 100
pct_reprovados = 100 - pct_aprovados

print("\n" + "=" * 45)
print("APROVAÇÃO")
print("=" * 45)
print(f"Passaram de ano: {pct_aprovados:.1f}%  ({alunos['aprovado'].sum()} alunos)")
print(f"Rodaram:         {pct_reprovados:.1f}%  ({(~alunos['aprovado']).sum()} alunos)")

# Pergunta A: "dos meninos, quantos % passaram?" (e das meninas)
aprovacao_por_sexo = alunos.groupby("sexo")["aprovado"].mean() * 100
print("\nDe cada sexo, quantos % passaram:")
for sexo, pct in aprovacao_por_sexo.items():
    total = (alunos["sexo"] == sexo).sum()
    print(f"  {sexo}s: {pct:.1f}% de {total}")

# Pergunta B: "de quem passou, quantos % são meninos e quantos são meninas?"
aprovados = alunos[alunos["aprovado"]]  # filtro: só as linhas com True
composicao = aprovados["sexo"].value_counts(normalize=True) * 100
print("\nEntre os aprovados:")
for sexo, pct in composicao.items():
    print(f"  {sexo}s: {pct:.1f}%")

# ---------- 7. POR TURMA ----------
por_turma = alunos.groupby("turma").agg(
    media=("media", "mean"),
    aprovacao_pct=("aprovado", "mean"),
    alunos=("aluno", "count"),
)
por_turma["aprovacao_pct"] = por_turma["aprovacao_pct"] * 100
por_turma = por_turma.round(1).sort_values("media", ascending=False)

print("\n" + "=" * 45)
print("RANKING DAS TURMAS (pela média)")
print("=" * 45)
print(por_turma)

# ---------- 8. SALVAR ----------
alunos.to_csv("dados/escola_notas.csv", sep=";", decimal=",", index=False, encoding="utf-8-sig")
print("\nArquivo salvo em dados/escola_notas.csv")
