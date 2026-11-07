# =============================================================
#  GRÁFICOS DA ESCOLA (matplotlib)
#  Reaproveita os dados de escola_python_puro.py
# =============================================================
#  4 gráficos, cada um responde UMA pergunta:
#   1. Quantos passaram de ano?         -> rosca (pizza com furo)
#   2. Meninos ou meninas foram melhor? -> barras horizontais
#   3. Qual turma foi melhor?           -> barras ordenadas
#   4. Como as médias se distribuem?    -> histograma
# =============================================================

import os
import random
import statistics

import matplotlib.pyplot as plt

# Importa as funções e constantes do outro arquivo.
# Funciona porque lá o main() está protegido pelo if __name__ == "__main__".
from escola_python_puro import criar_escola, porcentagem, TURMAS, MEDIA_APROVACAO

# ---------- CORES ----------
# Regra de ouro: UMA cor de destaque; o resto fica em cinza.
DESTAQUE = "#7a1fd6"   # roxo (o mesmo do banco Dumont)
CINZA = "#c4c4c4"
TEXTO = "#333333"
PASTA = "graficos_escola"


def estilo_limpo(ax):
    """Tira as bordas de cima e da direita (deixa o gráfico mais leve)."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors=TEXTO)


# ---------- 1. APROVADOS x REPROVADOS ----------
def grafico_aprovacao(ax, alunos):
    aprovados = sum(1 for a in alunos if a["aprovado"])
    reprovados = len(alunos) - aprovados
    pct = porcentagem(aprovados, len(alunos))

    ax.pie(
        [aprovados, reprovados],
        colors=[DESTAQUE, CINZA],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.35, "edgecolor": "white", "linewidth": 2},  # width -> vira rosca
    )
    # número grande no meio da rosca
    ax.text(0, 0.08, f"{pct:.0f}%", ha="center", va="center",
            fontsize=30, fontweight="bold", color=DESTAQUE)
    ax.text(0, -0.22, "passaram de ano", ha="center", va="center", fontsize=11, color=TEXTO)
    ax.legend([f"Aprovados ({aprovados})", f"Reprovados ({reprovados})"],
              loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)
    ax.set_title("3 em cada 4 alunos passaram de ano", loc="left", fontweight="bold", color=TEXTO)


# ---------- 2. APROVAÇÃO POR SEXO ----------
def grafico_por_sexo(ax, alunos):
    sexos = ["Meninos", "Meninas"]
    valores = []
    for sexo in ["Menino", "Menina"]:
        do_sexo = [a for a in alunos if a["sexo"] == sexo]
        passaram = sum(1 for a in do_sexo if a["aprovado"])
        valores.append(porcentagem(passaram, len(do_sexo)))

    # destaca quem foi melhor
    cores = [DESTAQUE if v == max(valores) else CINZA for v in valores]
    barras = ax.barh(sexos, valores, color=cores, height=0.55)
    ax.bar_label(barras, labels=[f"{v:.1f}%" for v in valores], padding=6,
                 fontsize=12, fontweight="bold", color=TEXTO)

    ax.set_xlim(0, 100)
    ax.set_xlabel("% de aprovação")
    ax.invert_yaxis()  # Meninos em cima
    estilo_limpo(ax)
    diferenca = abs(valores[0] - valores[1])
    ax.set_title(f"Meninas passaram mais: {diferenca:.1f} pontos à frente".replace(".", ","),
                 loc="left", fontweight="bold", color=TEXTO)


# ---------- 3. RANKING DAS TURMAS ----------
def grafico_turmas(ax, alunos):
    resumo = []
    for turma in TURMAS:
        da_turma = [a for a in alunos if a["turma"] == turma]
        passaram = sum(1 for a in da_turma if a["aprovado"])
        resumo.append((turma, porcentagem(passaram, len(da_turma))))
    resumo.sort(key=lambda item: item[1], reverse=True)  # maior para menor

    nomes = [f"Turma {t}" for t, _ in resumo]
    valores = [v for _, v in resumo]
    media_escola = porcentagem(sum(1 for a in alunos if a["aprovado"]), len(alunos))

    # destaca a melhor e a pior turma
    # pode haver empate no último lugar, então pego TODAS com a menor %
    piores = [t for t, v in resumo if v == min(valores)]

    cores = [CINZA] * len(valores)
    cores[0] = DESTAQUE
    for i, (turma, _) in enumerate(resumo):
        if turma in piores:
            cores[i] = "#4a4a4a"

    barras = ax.bar(nomes, valores, color=cores, width=0.65)
    ax.bar_label(barras, labels=[f"{v:.0f}%" for v in valores], padding=3, fontsize=9, color=TEXTO)
    ax.axhline(media_escola, color=TEXTO, linestyle="--", linewidth=1)
    ax.text(len(nomes) - 0.5, media_escola + 6, f"média da escola {media_escola:.0f}%",
            ha="right", fontsize=9, color=TEXTO)

    ax.set_ylim(0, 100)
    ax.set_ylabel("% de aprovação")
    ax.tick_params(axis="x", rotation=45)
    estilo_limpo(ax)
    if len(piores) == 1:
        texto_piores = f"Turma {piores[0]} precisa"
    else:
        texto_piores = "Turmas " + " e ".join(piores) + " precisam"
    ax.set_title(f"{nomes[0]} lidera; {texto_piores} de reforço",
                 loc="left", fontweight="bold", color=TEXTO)


# ---------- 4. DISTRIBUIÇÃO DAS MÉDIAS ----------
def grafico_distribuicao(ax, alunos):
    medias = [a["media"] for a in alunos]
    reprovados = [m for m in medias if m < MEDIA_APROVACAO]
    aprovados = [m for m in medias if m >= MEDIA_APROVACAO]
    faixas = [x / 2 for x in range(6, 20)]  # de 3,0 a 9,5, de meio em meio ponto

    # dois histogramas empilhados: cinza abaixo de 6, roxo a partir de 6
    ax.hist([reprovados, aprovados], bins=faixas, stacked=True,
            color=[CINZA, DESTAQUE], edgecolor="white", label=["Reprovados", "Aprovados"])
    ax.axvline(MEDIA_APROVACAO, color=TEXTO, linestyle="--", linewidth=1)
    ax.text(MEDIA_APROVACAO - 0.1, ax.get_ylim()[1] * 0.92, "nota de corte 6,0",
            ha="right", fontsize=9, color=TEXTO)

    media_geral = statistics.mean(medias)
    ax.set_xlabel("Média final do aluno")
    ax.set_ylabel("Quantidade de alunos")
    ax.legend(frameon=False, loc="upper left")
    estilo_limpo(ax)
    ax.set_title(f"A maioria fica perto da média {media_geral:.1f}".replace(".", ","),
                 loc="left", fontweight="bold", color=TEXTO)


# ---------- PROGRAMA PRINCIPAL ----------
def main():
    random.seed(42)            # mesma semente -> mesmos alunos do outro arquivo
    alunos = criar_escola()
    os.makedirs(PASTA, exist_ok=True)  # cria a pasta se não existir

    # Painel com os 4 gráficos (2 linhas x 2 colunas)
    fig, eixos = plt.subplots(2, 2, figsize=(14, 10))
    grafico_aprovacao(eixos[0, 0], alunos)
    grafico_por_sexo(eixos[0, 1], alunos)
    grafico_turmas(eixos[1, 0], alunos)
    grafico_distribuicao(eixos[1, 1], alunos)

    fig.suptitle("Escola Dumont: resultado do ano (1.000 alunos, 10 turmas)",
                 fontsize=18, fontweight="bold", color=TEXTO)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(f"{PASTA}/painel_escola.png", dpi=120)
    print(f"Painel salvo em {PASTA}/painel_escola.png")

    # Cada gráfico também em um arquivo separado (bom para slides e README)
    graficos = {
        "1_aprovacao": grafico_aprovacao,
        "2_por_sexo": grafico_por_sexo,
        "3_turmas": grafico_turmas,
        "4_distribuicao": grafico_distribuicao,
    }
    for nome, funcao in graficos.items():  # funções também podem ir num dicionário!
        fig_sozinha, ax = plt.subplots(figsize=(8, 5.5))
        funcao(ax, alunos)
        fig_sozinha.tight_layout()
        fig_sozinha.savefig(f"{PASTA}/{nome}.png", dpi=120)
        plt.close(fig_sozinha)
        print(f"Gráfico salvo em {PASTA}/{nome}.png")

    plt.show()  # abre a janela com o painel


if __name__ == "__main__":
    main()
