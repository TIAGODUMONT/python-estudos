# Versão web do programa de média de notas (o mesmo do ola.py).
# Para rodar: python app.py  →  abra http://127.0.0.1:5000 no navegador.
# Para parar: Ctrl + C no terminal.

from flask import Flask, render_template_string, request

app = Flask(__name__)


def situacao(media):
    """A mesma lógica do seu ola.py, só que RETORNANDO o texto em vez de dar print."""
    if media >= 7:
        return "Aprovado"
    elif media >= 5:
        return "Recuperação"
    else:
        return "Reprovado"


PAGINA = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Média das Notas</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0;
               display: flex; justify-content: center; padding: 48px 16px; }
        .card { background: #1e293b; padding: 32px; border-radius: 12px; width: 100%; max-width: 360px; }
        h1 { margin-top: 0; font-size: 1.4rem; }
        label { display: block; margin-top: 16px; font-size: .9rem; color: #94a3b8; }
        input { width: 100%; padding: 10px; margin-top: 4px; border-radius: 8px; border: 1px solid #334155;
                background: #0f172a; color: #e2e8f0; box-sizing: border-box; }
        button { margin-top: 20px; width: 100%; padding: 12px; border: 0; border-radius: 8px;
                 background: #3b82f6; color: white; font-weight: bold; cursor: pointer; }
        .resultado { margin-top: 20px; padding: 16px; background: #0f172a; border-radius: 8px; text-align: center; }
        .resultado strong { font-size: 2rem; display: block; }
        .Aprovado { color: #4ade80; }
        .Recuperação { color: #facc15; }
        .Reprovado { color: #f87171; }
    </style>
</head>
<body>
    <div class="card">
        <h1>📚 Média das Notas</h1>

        <form method="POST">
            <label>Primeira nota</label>
            <input name="nota1" type="number" step="0.1" min="0" max="10" required placeholder="8">

            <label>Segunda nota</label>
            <input name="nota2" type="number" step="0.1" min="0" max="10" required placeholder="6.5">

            <button type="submit">Calcular média</button>
        </form>

        {% if media is not none %}
            <div class="resultado">
                A média das notas é
                <strong>{{ "%.1f"|format(media) }}</strong>
                <span class="{{ resultado }}">{{ resultado }}</span>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    media = None
    resultado = None

    if request.method == "POST":
        # Antes: nota1 = float(input("Digite a primeira nota: "))
        # Agora: o valor vem do <input name="nota1"> do formulário.
        nota1 = float(request.form["nota1"])
        nota2 = float(request.form["nota2"])
        media = (nota1 + nota2) / 2
        resultado = situacao(media)

    return render_template_string(PAGINA, media=media, resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)
