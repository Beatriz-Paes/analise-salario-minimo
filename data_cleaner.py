"""Código para limpeza de dados do salário mínimo no Brasil."""
import pandas as pd

from config import CESTA_BASICA_FILE, CIDADE_MAP


def tratar_valores(valor: str) -> float | str:
    """Remove o prefixo 'R$', separadores de milhar e converte para float, ou retorna 'Sem dados' se o valor for '-'."""
    if valor == "-":
        return "Sem dados"
    return float(valor.replace("R$", "").replace(".", "").replace(",", "."))


def clean_salario() -> None:
    """Limpa e trata os dados do arquivo CSV de salário mínimo."""
    df = pd.read_csv("salario_minimo.csv", sep=";")

    colunas_esperadas = ["Ano", "Período", "Salário Mínimo Nominal", "Salário Mínimo Necessário"]
    for coluna in colunas_esperadas:
        if coluna not in df.columns:
            raise ValueError(f"Coluna '{coluna}' ausente no arquivo CSV")

    df["Salário Mínimo Nominal"] = df["Salário Mínimo Nominal"].fillna("0").apply(tratar_valores)
    df["Salário Mínimo Necessário"] = df["Salário Mínimo Necessário"].fillna("0").apply(tratar_valores)

    df.to_csv("static/tables/salario_minimo_tratado.csv", index=False, encoding="utf-8", sep=";")
    print("Arquivo tratado salvo como 'static/tables/salario_minimo_tratado.csv'.")


def clean_cesta_basica(df: pd.DataFrame) -> pd.DataFrame:
    """Realiza o tratamento dos dados retornados da pesquisa da cesta básica.

    Args:
        df (pd.DataFrame): DataFrame bruto com os dados da cesta básica.

    Returns:
        pd.DataFrame: Dados tratados e prontos para uso.
    """
    df.columns = ["Data", "Custo da Cesta (R$)", "Cidade"]
    df["Custo da Cesta (R$)"] = df["Custo da Cesta (R$)"].fillna("0").apply(tratar_valores)
    df["Cidade"] = df["Cidade"].astype(int)
    df["Cidade"] = df["Cidade"].map(CIDADE_MAP)

    df.to_csv(CESTA_BASICA_FILE, index=False, encoding="utf-8", sep=";")
    print(f"Arquivo tratado salvo como {CESTA_BASICA_FILE}.")
    return df
