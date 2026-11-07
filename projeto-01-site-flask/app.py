from flask import Flask, render_template, request

# Cria o "site". Parecido com: const app = express()
app = Flask(__name__)


def calcular_imc(peso, altura):
    """Recebe o peso em kg e a altura em metros e retorna o IMC."""
    return round(peso / (altura ** 2), 2)


# Rota da página inicial. Parecido com: app.get("/", ...)
# methods=["GET", "POST"] deixa a mesma rota abrir a página E receber o formulário.
@app.route("/", methods=["GET", "POST"])
def home():
    imc = None

    if request.method == "POST":
        # request.form ≈ req.body no Express. Tudo chega como texto, por isso o float().
        peso = float(request.form["peso"])
        altura = float(request.form["altura"].replace(",", "."))
        imc = calcular_imc(peso, altura)

    # Monta o HTML de templates/index.html e passa a variável imc para ele.
    return render_template("index.html", imc=imc)


# Outra rota, com variável na URL. Teste: /ola/Tiago
@app.route("/ola/<nome>")
def ola(nome):
    return f"<h1>Olá, {nome}! Isso aqui foi gerado pelo Python.</h1>"


# Só roda o servidor quando você executa "python app.py" direto.
if __name__ == "__main__":
    app.run(debug=True)
