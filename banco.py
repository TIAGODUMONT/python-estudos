# Simulação de dados de usuários de um e-commerce
# (visitas, tempo no site, itens no carrinho e valor da compra)

# Todos os imports ficam no topo do arquivo (boa prática do Python - PEP 8).
# O pacote watermark é instalado pelo TERMINAL: pip install watermark
# O "!pip install" só funciona em notebook (.ipynb / Google Colab).
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D   # para desenhar a legenda da linha da média
from matplotlib.patches import Patch  # para desenhar a legenda da faixa cinza
from watermark import watermark

# Mostra o autor, a versão do Python e as versões dos pacotes importados
print(watermark(author="Tiago Dumont", python=True, iversions=True, globals_=globals()))

# definir uma semente aleatória para reprodutibilidade dos resultados
np.random.seed(42)

# definir o número de usuários
n_usuarios = 1000

# gerar o número de visitas (entre 1 e 50)
# randint não inclui o número final, por isso 51
n_visitas = np.random.randint(1, 51, size=n_usuarios)

# gerar o tempo no site (distribuição normal, correlacionado com visitas)
# média de 20 minutos, desvio padrão de 5 minutos, com bônus de 0,5 min por visita
tempo_no_site = np.random.normal(20, 5, size=n_usuarios) + n_visitas * 0.5
tempo_no_site = np.maximum(tempo_no_site, 0)  # garantir que o tempo não seja negativo
tempo_no_site = np.round(tempo_no_site, 2)    # arredondar para duas casas decimais

# gerar o número de itens no carrinho (dependente do tempo no site)
# A Poisson nunca gera números negativos, então não precisa de np.maximum aqui.
n_itens_carrinho = np.random.poisson(lam=tempo_no_site / 10, size=n_usuarios)

# gerar valores de compra (dependente do número de itens no carrinho,
# que por sua vez é correlacionado com o tempo no site)
# valor médio de cada item é 35, com ruído normal
valores_compra = (n_itens_carrinho * 35) + np.random.normal(loc=0, scale=10, size=n_usuarios)
valores_compra = np.maximum(valores_compra, 0)  # o ruído não pode deixar uma compra negativa

# se não houver itens no carrinho, o valor da compra é zero
valores_compra[n_itens_carrinho == 0] = 0
valores_compra = np.round(valores_compra, 2)  # arredondar para duas casas decimais

# ---------- Conferindo o resultado ----------
# Junta tudo numa tabela (DataFrame) para ver se os dados fazem sentido
df = pd.DataFrame({
    "visitas": n_visitas,
    "tempo_no_site": tempo_no_site,
    "itens_carrinho": n_itens_carrinho,
    "valor_compra": valores_compra,
})

print(df.head())      # as 5 primeiras linhas
print(df.describe())  # média, mínimo, máximo, desvio padrão de cada coluna

# ---------- Análise descritiva (com as funções do NumPy) ----------
# Um dicionário com as 4 variáveis: nome que vai aparecer -> array com os dados
variaveis = {
    "Visitas": n_visitas,
    "Tempo no site (min)": tempo_no_site,
    "Itens no carrinho": n_itens_carrinho,
    "Valor da compra (R$)": valores_compra,
}

estatisticas = {}
for nome, dados in variaveis.items():  # .items() ≈ Object.entries() do JS
    estatisticas[nome] = {
        "Média": np.mean(dados),
        # ddof=1 = desvio padrão da AMOSTRA (o mesmo que o pandas usa no describe)
        "Desvio padrão": np.std(dados, ddof=1),
        "Mínimo": np.min(dados),
        "Máximo": np.max(dados),
    }

# Transforma o dicionário numa tabela. O .T vira a tabela (linhas <-> colunas).
tabela = pd.DataFrame(estatisticas).T.round(2)
print("\n===== Análise descritiva =====")
print(tabela)


def br(valor, casas=1):
    """Formata número no padrão brasileiro: 1234.5 -> '1.234,5'."""
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------- Gráfico 0: a análise descritiva das 4 variáveis ----------
# As 4 variáveis têm escalas MUITO diferentes (itens vai de 0 a 12, valor vai até R$ 400).
# Num gráfico só, com um eixo só, as pequenas sumiriam. Por isso: 4 mini-gráficos
# (2 linhas x 2 colunas) na MESMA figura, cada um com a sua escala.
fig, eixos = plt.subplots(2, 2, figsize=(13, 8.5))

# zip() anda nas duas listas ao mesmo tempo: cada mini-gráfico recebe uma variável
for ax, (nome, dados) in zip(eixos.flat, variaveis.items()):
    est = estatisticas[nome]
    media, desvio = est["Média"], est["Desvio padrão"]

    # faixa cinza = média ± 1 desvio padrão (onde fica a maior parte dos usuários)
    ax.axvspan(media - desvio, media + desvio, color="#898781", alpha=0.15, zorder=0)

    # itens no carrinho são números inteiros: uma barra para cada valor (0, 1, 2...)
    if nome == "Itens no carrinho":
        faixas = np.arange(dados.min() - 0.5, dados.max() + 1.5)
    else:
        faixas = 25
    ax.hist(dados, bins=faixas, color="#2a78d6", edgecolor="white", linewidth=1.5, zorder=2)

    # linha da média
    ax.axvline(media, color="#0b0b0b", linewidth=2, linestyle="--", zorder=3)

    # título do mini-gráfico + linha com os números
    casas = 2 if "Valor" in nome else 1
    ax.set_title(nome, loc="left", fontsize=12, fontweight="bold", pad=24)
    resumo = (f"Média {br(media, casas)}   ·   Desvio padrão {br(desvio, casas)}   ·   "
              f"Mín. {br(est['Mínimo'], casas)}   ·   Máx. {br(est['Máximo'], casas)}")
    ax.text(0, 1.03, resumo, transform=ax.transAxes, fontsize=9.5, color="#52514e")

    # acabamento discreto
    ax.set_ylabel("Usuários", color="#52514e")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#898781")
    ax.tick_params(colors="#52514e")
    ax.grid(axis="y", color="#e1e0d9", linewidth=0.8)
    ax.set_axisbelow(True)

# legenda única para a figura toda, explicando a linha e a faixa
fig.legend(
    handles=[
        Line2D([0], [0], color="#0b0b0b", linewidth=2, linestyle="--", label="Média"),
        Patch(facecolor="#898781", alpha=0.3, label="Média ± 1 desvio padrão"),
    ],
    loc="upper right", ncol=2, frameon=False, bbox_to_anchor=(0.99, 0.985),
)
fig.suptitle(f"Análise descritiva dos {n_usuarios} usuários",
             x=0.01, ha="left", fontsize=15, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("analise_descritiva.png", dpi=120)

# ---------- Gráfico 1 (matplotlib): tempo que os usuários ficam no site ----------
# Com 1000 usuários, uma barra por usuário ficaria ilegível. O HISTOGRAMA agrupa
# os tempos em faixas (ex.: 25 a 27 min) e mostra QUANTOS usuários caíram em cada uma.
media = df["tempo_no_site"].mean()
mediana = df["tempo_no_site"].median()

fig, ax = plt.subplots(figsize=(10, 5.5))  # fig = a janela, ax = a área do gráfico

ax.hist(
    df["tempo_no_site"],
    bins=30,              # quantidade de faixas
    color="#2a78d6",
    edgecolor="white",    # contorno branco = um respiro entre as barras
    linewidth=2,
)

# linhas verticais marcando a média e a mediana, com o valor escrito ao lado
ax.axvline(media, color="#0b0b0b", linewidth=2, linestyle="--")
ax.axvline(mediana, color="#52514e", linewidth=2, linestyle=":")
topo = ax.get_ylim()[1] * 1.12
ax.set_ylim(0, topo)  # deixa um espaço livre acima das barras para os textos
fundo = {"facecolor": "white", "edgecolor": "none", "pad": 3}  # fundo branco atrás do texto
# média à direita da linha e mediana à esquerda, porque os dois valores são muito próximos
ax.text(media + 0.6, topo * 0.97, f"Média: {media:.1f} min",
        color="#0b0b0b", va="top", ha="left", bbox=fundo)
ax.text(mediana - 0.6, topo * 0.97, f"Mediana: {mediana:.1f} min",
        color="#52514e", va="top", ha="right", bbox=fundo)

ax.set_title("Quanto tempo os usuários ficam no site", loc="left", fontsize=14, fontweight="bold")
ax.set_xlabel("Tempo no site (minutos)", color="#52514e")
ax.set_ylabel("Número de usuários", color="#52514e")

# deixa o "esqueleto" do gráfico discreto, para os dados chamarem a atenção
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["left", "bottom"]].set_color("#898781")
ax.tick_params(colors="#52514e")
ax.grid(axis="y", color="#e1e0d9", linewidth=0.8)
ax.set_axisbelow(True)  # grade atrás das barras

fig.tight_layout()
fig.savefig("grafico_tempo_no_site.png", dpi=120)  # também salva como imagem

# ---------- Gráfico 2 (seaborn): tempo no site x valor da compra ----------
plt.figure(figsize=(8, 5))  # abre uma figura NOVA (senão ele desenha em cima do gráfico 1)
sns.scatterplot(data=df, x="tempo_no_site", y="valor_compra")
plt.title("Tempo no site x valor da compra")

plt.show()  # abre as duas janelas (feche uma para ver a outra)

np.median(df["tempo_no_site"])  # 22.0

#colocar a mediana no gráfico de dispersão
plt.figure(figsize=(8, 5))  # abre uma figura NOVA (senão ele desenha em cima do gráfico 1)
sns.scatterplot(data=df, x="tempo_no_site", y="valor_compra")
plt.axvline(np.median(df["tempo_no_site"]), color='red', linestyle='--', label='Mediana do tempo no site')
plt.title("Tempo no site x valor da compra")
plt.legend()

