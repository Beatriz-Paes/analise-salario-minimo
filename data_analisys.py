"""Código para análise de dados do salário mínimo no Brasil."""
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter

from config import CIDADE_MAP, DADOS_UTEIS, MESES_MAP, SALARIO_MINIMO_FILE
from data_cleaner import clean_cesta_basica
from data_fetcher import fetch_cesta_basica


def carregar_e_preparar_dados() -> pd.DataFrame:
    """Carrega e prepara os dados necessários."""
    df = pd.read_csv("static/tables/salario_minimo_tratado.csv", sep=";")

    df["Período"] = df["Período"].map(MESES_MAP)

    df["Data"] = df["Período"] + " " + df["Ano"].astype(str)
    df["Data"] = pd.to_datetime(df["Data"], format="%B %Y", errors="coerce")

    if df["Data"].isnull().any():
        print("Aviso: Existem valores inválidos na coluna 'Data' e serão ignorados.")
    df = df.dropna(subset=["Data"])

    df = df.sort_values("Data")
    return df


def grafico_evolucao_salarios(df: pd.DataFrame) -> None:
    """Gera o gráfico de evolução do Salário Nominal e Necessário."""
    plt.figure(figsize=(14, 7))
    sns.set_theme(style="whitegrid")

    sns.lineplot(data=df, x="Data", y="Salário Mínimo Necessário", label="Salário Necessário", marker="o", color="red")
    sns.lineplot(data=df, x="Data", y="Salário Mínimo Nominal", label="Salário Nominal", marker="o", color="blue")

    plt.title("Evolução do Salário Mínimo (Nominal x Necessário)", fontsize=16)
    plt.xlabel("Ano", fontsize=12)
    plt.ylabel("Valor (em milhares de R$)", fontsize=12)

    def formatar_em_milhares(valor: float, _: int) -> str:
        """Formata o valor para milhares."""
        return f"{valor / 1000:.1f}k"

    plt.gca().yaxis.set_major_formatter(FuncFormatter(formatar_em_milhares))

    plt.legend(title="Indicadores", fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/images/salario_minimo_evolucao.png")
    print("Gráfico salvo como 'static/images/salario_minimo_evolucao.png'.")
    plt.close()


def grafico_poder_compra_e_variacoes(df: pd.DataFrame) -> None:
    """Gera o gráfico (agregados por ano, incluindo salário nominal)."""
    df["Poder de Compra (%)"] = (df["Salário Mínimo Nominal"] / df["Salário Mínimo Necessário"]) * 100

    df["Data"] = pd.to_datetime(df["Data"])

    df["Ano"] = df["Data"].dt.year
    df_anual = df.groupby("Ano", as_index=False).agg(
        {
            "Poder de Compra (%)": "mean",
            "Salário Mínimo Nominal": "mean",
        }
    )

    df_anual["Crescimento Nominal (%)"] = df_anual["Salário Mínimo Nominal"].pct_change() * 100
    df_anual.loc[0, "Crescimento Nominal (%)"] = 0

    df_anual.to_csv("static/tables/poder_de_compra_e_crescimento.csv", index=False)
    print(
        "Tabela de poder de compra anual e crescimento nominal salva em "
        "'static/tables/poder_de_compra_e_crescimento.csv'."
    )

    plt.figure(figsize=(14, 7))
    sns.set_theme(style="whitegrid")

    sns.lineplot(
        data=df_anual,
        x="Ano",
        y="Poder de Compra (%)",
        label="Poder de Compra (%) (Média Anual)",
        marker="o",
        color="blue",
    )

    for i in range(len(df_anual)):
        ano = df_anual["Ano"].iloc[i]
        salario = df_anual["Salário Mínimo Nominal"].iloc[i]
        poder_compra = df_anual["Poder de Compra (%)"].iloc[i]

        plt.text(ano, poder_compra - 1, f"R$ {salario:.2f}", horizontalalignment="center", color="black", fontsize=8)

    plt.title("Poder de Compra do Salário Mínimo (Média Anual)", fontsize=16)
    plt.xlabel("Ano", fontsize=12)
    plt.ylabel("Poder de Compra (%)", fontsize=12)

    def formatar_porcentagem(valor: float, _: int) -> str:
        """Formata o valor como porcentagem."""
        return f"{valor:.1f}%"

    plt.gca().yaxis.set_major_formatter(FuncFormatter(formatar_porcentagem))

    plt.legend(title="Indicadores", fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/images/poder_compra.png")
    print("Gráfico salvo como 'static/images/poder_compra.png'.")
    plt.close()


def processar_dados_economicos(cidade_padrao: int = 8) -> dict:
    """Processa os dados do salário mínimo e da cesta básica para retornar informações importantes.

    Args:
        cidade_padrao (int): ID padrão da cidade para calcular a média da cesta básica.

    Returns:
        dict: Dados processados, incluindo salário nominal, salário necessário e custo médio da cesta básica.
    """
    # Carregar dados do salário mínimo
    salario_data = pd.read_csv(SALARIO_MINIMO_FILE, sep=";")

    # Obter os valores mais recentes de salário
    ultimo_registro = salario_data.iloc[1]  # Considerando que o mais recente está no final do arquivo
    salario_nominal_atual = ultimo_registro["Salário Mínimo Nominal"]
    salario_necessario_atual = ultimo_registro["Salário Mínimo Necessário"]

    # Cálculo dos últimos 12 meses
    data_final = datetime.now()
    data_inicial = data_final - timedelta(days=365)  # Aproximando 12 meses para 365 dias
    mes_inicial = f"{data_inicial.month:02d}"
    ano_inicial = data_inicial.year
    mes_final = f"{data_final.month:02d}"
    ano_final = data_final.year

    # Buscar e limpar os dados da cesta básica no intervalo de 12 meses
    cesta_basica = clean_cesta_basica(
        fetch_cesta_basica(
            cidade_padrao,
            f"{mes_inicial}{ano_inicial}",  # Data inicial no formato MMAAAA
            f"{mes_final}{ano_final}",  # Data final no formato MMAAAA
        )
    )

    cesta_filtrada = cesta_basica[cesta_basica["Cidade"] == CIDADE_MAP[cidade_padrao]]
    cesta_filtrada["Custo da Cesta (R$)"] = pd.to_numeric(cesta_filtrada["Custo da Cesta (R$)"], errors="coerce")
    custo_cesta_basica_media = cesta_filtrada["Custo da Cesta (R$)"].mean()

    # Consolidar os dados processados
    dados_resumo = {
        "salario_nominal_atual": round(salario_nominal_atual, 2),
        "salario_necessario_atual": round(salario_necessario_atual, 2),
        "custo_cesta_basica_media": round(custo_cesta_basica_media, 2),
    }

    # Salvar em um arquivo
    df_dados_resumo = pd.DataFrame([dados_resumo])
    df_dados_resumo.to_csv(DADOS_UTEIS, index=False)

    return dados_resumo


def plot_data() -> None:
    """Função principal para gerar os gráficos e tabelas de análise de dados do salário mínimo."""
    df = carregar_e_preparar_dados()
    grafico_evolucao_salarios(df)
    grafico_poder_compra_e_variacoes(df)
