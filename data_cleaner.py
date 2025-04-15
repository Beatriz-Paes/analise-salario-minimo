"""Código para limpeza de dados do salário mínimo no Brasil."""
import pandas as pd


def tratar_valores(valor: str) -> float:
    """Remove o prefixo 'R$', separadores de milhar e converte para float."""
    return float(valor.replace("R$", "").replace(".", "").replace(",", "."))


def clean_data() -> None:
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
