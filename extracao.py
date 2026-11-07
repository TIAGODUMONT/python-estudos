# FUNCAO PARA GERAR DADOS FICTICIOS

import numpy as np
import pandas as pd


def dsa_gera_dados_churn(num_clientes = 2000):
    """
    Gera um DataFrame de dados fictícios de clientes de uma empresa de telecomunicações.
    """

    # Para reprodutibilidade
    np.random.seed(42)

    # Variáveis
    fidelidade_meses = np.random.randint(1, 73, size = num_clientes)
    tipo_contrato_opts = ['Mensal', 'Anual', 'Dois anos']
    contrato_probs = [0.6, 0.25, 0.15]
    tipo_contrato = np.random.choice(tipo_contrato_opts, size = num_clientes, p = contrato_probs)
    servico_internet_opts = ['Fibra Optica', 'DSL', 'Não']
    internet_probs = [0.55, 0.35, 0.10]
    servico_internet = np.random.choice(servico_internet_opts, size = num_clientes, p = internet_probs)

    fatura_base = {
        'Mensal': np.random.normal(60, 20),
        'Anual': np.random.normal(70, 25),
        'Dois anos': np.random.normal(80, 25)
    }

    fatura_mensal = [fatura_base[c] + fidelidade_meses[i] * 0.2 + np.random.normal(0, 5) for i, c in enumerate(tipo_contrato)]
    fatura_mensal = np.clip(fatura_mensal, 20, 120)

    # Lógica para a probabilidade de Churn
    # Clientes com contrato mensal, baixa fidelidade e fatura alta têm maior chance de churn
    prob_churn_log = -2.5  # Intercepto base (tendência a não cancelar)
    prob_churn_log += -0.05 * fidelidade_meses  # Mais fidelidade, menor chance
    prob_churn_log += np.array([3.0 if c == 'Mensal' else -1.5 if c == 'Anual' else -2.5 for c in tipo_contrato])  # Contrato mensal aumenta muito a chance
    prob_churn_log += np.array([0.8 if s == 'Fibra Optica' else -0.5 for s in servico_internet])  # Fibra tende a ter mais churn (talvez por preço)
    prob_churn_log += 0.03 * fatura_mensal  # Fatura mais alta, mais chance

    # Converte o valor em probabilidade (entre 0 e 1) com a função sigmoide
    prob_churn = 1 / (1 + np.exp(-prob_churn_log))

    # Sorteia se cada cliente cancelou (1) ou não (0)
    churn = np.random.binomial(1, prob_churn)

    # Monta o DataFrame
    df = pd.DataFrame({
        'ID_Cliente': range(1, num_clientes + 1),
        'Fidelidade_Meses': fidelidade_meses,
        'Tipo_Contrato': tipo_contrato,
        'Servico_Internet': servico_internet,
        'Fatura_Mensal': fatura_mensal.round(2),
        'Churn': churn
    })

    return df


if __name__ == "__main__":
    df_clientes = dsa_gera_dados_churn()
    print(df_clientes.head())
    print(f"\nTotal de clientes: {len(df_clientes)}")
    print(f"Taxa de churn: {df_clientes['Churn'].mean():.1%}")

    