# =============================================================
#  SIMULAÇÃO DE UMA ESCOLA EM PYTHON PURO (sem pandas e sem numpy)
#  1000 alunos, 10 turmas, 5 disciplinas
# =============================================================
#  Estrutura do programa:
#   1. Imports        -> só bibliotecas que já vêm com o Python
#   2. Constantes     -> configurações em MAIÚSCULAS no topo
#   3. Funções        -> cada função faz UMA coisa
#   4. main()         -> chama as funções na ordem certa
#   5. if __name__ == "__main__": main()
# =============================================================

# ---------- 1. IMPORTS ----------
import random       # sorteios
import statistics   # média, mediana, moda, desvio padrão
import csv          # salvar arquivo .csv

# ---------- 2. CONSTANTES ----------
QTD_ALUNOS = 1000
TURMAS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
DISCIPLINAS = ["Matemática", "Português", "História", "Geografia", "Ciências"]
MEDIA_APROVACAO = 6.0


# ---------- 3. FUNÇÕES ----------

def sortear_nota():
    """Sorteia uma nota inteira de 0 a 10, quase sempre perto de 6,5."""
    nota = round(random.gauss(6.5, 2.0))  # gauss = distribuição normal
    return max(0, min(10, nota))          # trava entre 0 e 10


def criar_aluno(numero, turma):
    """Cria UM aluno. Cada aluno é um dicionário (parecido com um objeto do JS)."""
    notas = {}
    for disciplina in DISCIPLINAS:
        notas[disciplina] = sortear_nota()

    media = round(statistics.mean(notas.values()), 2)

    return {
        "nome": f"Aluno {numero:04d}",
        "sexo": random.choice(["Menino", "Menina"]),
        "turma": turma,
        "notas": notas,
        "media": media,
        "aprovado": media >= MEDIA_APROVACAO,
    }


def criar_escola():
    """Cria a lista com os 1000 alunos: 100 em cada turma."""
    alunos_por_turma = QTD_ALUNOS // len(TURMAS)  # // é divisão inteira -> 100
    alunos = []
    numero = 1
    for turma in TURMAS:
        for _ in range(alunos_por_turma):  # _ = "não vou usar essa variável"
            alunos.append(criar_aluno(numero, turma))
            numero += 1
    return alunos


def porcentagem(parte, total):
    """Regra de três: quanto 'parte' representa de 'total', em %."""
    if total == 0:
        return 0.0
    return parte / total * 100


def mostrar_estatisticas(alunos):
    medias = [aluno["media"] for aluno in alunos]  # list comprehension

    todas_as_notas = []
    for aluno in alunos:
        todas_as_notas.extend(aluno["notas"].values())  # junta as 5 notas na lista

    print("=" * 45)
    print("ESTATÍSTICAS DA ESCOLA")
    print("=" * 45)
    print(f"Média geral:             {statistics.mean(medias):.2f}")
    print(f"Mediana:                 {statistics.median(medias):.2f}")
    print(f"Desvio padrão:           {statistics.stdev(medias):.2f}")
    print(f"Maior média:             {max(medias):.2f}")
    print(f"Menor média:             {min(medias):.2f}")
    print(f"Moda (nota mais comum):  {statistics.mode(todas_as_notas)}")

    print("\nMédia por disciplina:")
    for disciplina in DISCIPLINAS:
        notas_da_disciplina = [aluno["notas"][disciplina] for aluno in alunos]
        print(f"  {disciplina:<12} {statistics.mean(notas_da_disciplina):.2f}")


def mostrar_aprovacao(alunos):
    aprovados = [aluno for aluno in alunos if aluno["aprovado"]]
    reprovados = [aluno for aluno in alunos if not aluno["aprovado"]]

    print("\n" + "=" * 45)
    print("APROVAÇÃO")
    print("=" * 45)
    print(f"Passaram de ano: {porcentagem(len(aprovados), len(alunos)):.1f}%  ({len(aprovados)} alunos)")
    print(f"Rodaram:         {porcentagem(len(reprovados), len(alunos)):.1f}%  ({len(reprovados)} alunos)")

    print("\nDe cada sexo, quantos % passaram:")
    for sexo in ["Menino", "Menina"]:
        do_sexo = [aluno for aluno in alunos if aluno["sexo"] == sexo]
        passaram = [aluno for aluno in do_sexo if aluno["aprovado"]]
        pct = porcentagem(len(passaram), len(do_sexo))
        print(f"  {sexo}s: {pct:.1f}% ({len(passaram)} de {len(do_sexo)})")

    print("\nEntre os aprovados:")
    for sexo in ["Menino", "Menina"]:
        qtd = len([aluno for aluno in aprovados if aluno["sexo"] == sexo])
        print(f"  {sexo}s: {porcentagem(qtd, len(aprovados)):.1f}%")


def mostrar_ranking_turmas(alunos):
    resumo = []
    for turma in TURMAS:
        da_turma = [aluno for aluno in alunos if aluno["turma"] == turma]
        media_turma = statistics.mean(aluno["media"] for aluno in da_turma)
        qtd_aprovados = sum(1 for aluno in da_turma if aluno["aprovado"])
        resumo.append({
            "turma": turma,
            "media": media_turma,
            "aprovacao": porcentagem(qtd_aprovados, len(da_turma)),
        })

    # ordena da maior média para a menor (key diz POR QUAL campo ordenar)
    resumo.sort(key=lambda item: item["media"], reverse=True)

    print("\n" + "=" * 45)
    print("RANKING DAS TURMAS")
    print("=" * 45)
    for posicao, item in enumerate(resumo, start=1):
        print(f"{posicao:>2}º  Turma {item['turma']}  média {item['media']:.2f}  aprovação {item['aprovacao']:.0f}%")


def melhor_aluno(alunos):
    """Versão 1 (pythônica): max() com key.
    O key diz ao max() QUAL valor comparar em cada aluno: a média."""
    return max(alunos, key=lambda aluno: aluno["media"])


def melhor_aluno_com_for(alunos):
    """Versão 2 (passo a passo): o mesmo resultado, com um for comum.
    Ideia: começo achando que o primeiro é o melhor e vou comparando."""
    melhor = alunos[0]
    for aluno in alunos:
        if aluno["media"] > melhor["media"]:
            melhor = aluno  # achei alguém melhor: troco
    return melhor


def pior_aluno(alunos):
    """Igual ao melhor_aluno, trocando max por min."""
    return min(alunos, key=lambda aluno: aluno["media"])


def pior_aluno_com_for(alunos):
    """Igual à versão com for do melhor, trocando > por <."""
    pior = alunos[0]
    for aluno in alunos:
        if aluno["media"] < pior["media"]:
            pior = aluno
    return pior


def melhor_por_turma(alunos):
    """Devolve um dicionário {turma: melhor aluno daquela turma}.
    Reaproveita a função melhor_aluno(): só filtra os alunos da turma antes."""
    campeoes = {}
    for turma in TURMAS:
        da_turma = [aluno for aluno in alunos if aluno["turma"] == turma]
        campeoes[turma] = melhor_aluno(da_turma)
    return campeoes


def mostrar_pior_aluno(alunos):
    lanterna = pior_aluno(alunos)
    print("\n" + "=" * 45)
    print("ALUNO COM A MENOR MÉDIA")
    print("=" * 45)
    print(f"{lanterna['nome']} | Turma {lanterna['turma']} | média {lanterna['media']:.2f}")
    print(f"Versão com for encontrou: {pior_aluno_com_for(alunos)['nome']}")


def mostrar_melhor_por_turma(alunos):
    print("\n" + "=" * 45)
    print("MELHOR ALUNO DE CADA TURMA")
    print("=" * 45)
    for turma, aluno in melhor_por_turma(alunos).items():
        print(f"Turma {turma}: {aluno['nome']} ({aluno['sexo']}) - média {aluno['media']:.2f}")


def mostrar_melhor_aluno(alunos):
    campeao = melhor_aluno(alunos)
    campeao_for = melhor_aluno_com_for(alunos)

    print("\n" + "=" * 45)
    print("MELHOR ALUNO DA ESCOLA 🏆")
    print("=" * 45)
    print(f"Nome:  {campeao['nome']}")
    print(f"Turma: {campeao['turma']}")
    print(f"Sexo:  {campeao['sexo']}")
    print(f"Média: {campeao['media']:.2f}")
    print("Notas:")
    for disciplina, nota in campeao["notas"].items():  # .items() -> chave e valor
        print(f"  {disciplina:<12} {nota}")

    # As duas versões precisam dar o mesmo aluno
    print(f"\nVersão com for encontrou: {campeao_for['nome']} "
          f"-> {'iguais ✅' if campeao is campeao_for else 'diferentes ❌'}")


def salvar_csv(alunos, caminho):
    with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["nome", "sexo", "turma", *DISCIPLINAS, "media", "situacao"])
        for aluno in alunos:
            situacao = "Aprovado" if aluno["aprovado"] else "Reprovado"
            notas = [aluno["notas"][d] for d in DISCIPLINAS]
            escritor.writerow([aluno["nome"], aluno["sexo"], aluno["turma"], *notas,
                               str(aluno["media"]).replace(".", ","), situacao])
    print(f"\nArquivo salvo em {caminho}")


# ---------- 4. PROGRAMA PRINCIPAL ----------

def main():
    random.seed(42)  # mesmo sorteio toda vez que rodar
    alunos = criar_escola()

    print("Exemplo de um aluno:")
    print(alunos[0], "\n")

    mostrar_estatisticas(alunos)
    mostrar_aprovacao(alunos)
    mostrar_ranking_turmas(alunos)
    mostrar_melhor_aluno(alunos)
    mostrar_pior_aluno(alunos)
    mostrar_melhor_por_turma(alunos)
    salvar_csv(alunos, "dados/escola_notas_python_puro.csv")


# ---------- 5. PONTO DE ENTRADA ----------
# Só roda o main() quando você executa ESTE arquivo direto.
if __name__ == "__main__":
    main()
