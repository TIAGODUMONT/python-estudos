def calcular_imc(peso, altura):
    """Recebe o peso em kg e a altura em metros e retorna o IMC."""
    imc = peso / (altura ** 2)
    return round(imc, 2)


# Testando a função
resultado = calcular_imc(80, 1.80)
print(f"Seu IMC é {resultado}")
