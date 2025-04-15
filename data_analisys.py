"""Código para análise de dados do salário mínimo no Brasil."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Mapeamento de meses do português para inglês
MESES_MAPA = {
    "Janeiro": "January",
    "Fevereiro": "February",
    "Março": "March",
    "Abril": "April",
    "Maio": "May",
    "Junho": "June",
    "Julho": "July",
    "Agosto": "August",
    "Setembro": "September",
    "Outubro": "October",
    "Novembro": "November",
    "Dezembro": "December",
}


def carregar_e_preparar_dados() -> pd.DataFrame:
    """Carrega e prepara os dados necessários."""
    df = pd.read_csv("static/tables/salario_minimo_tratado.csv", sep=";")

    df["Período"] = df["Período"].map(MESES_MAPA)

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


def plot_data() -> None:
    """Função principal para gerar os gráficos e tabelas de análise de dados do salário mínimo."""
    df = carregar_e_preparar_dados()
    grafico_evolucao_salarios(df)
    grafico_poder_compra_e_variacoes(df)
