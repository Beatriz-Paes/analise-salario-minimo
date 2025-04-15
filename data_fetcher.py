"""Código para buscar e processar dados do salário mínimo no Brasil."""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import DIEESE_CESTA, DIEESE_SALARIO


def fetch_salario() -> None:
    """Busca dados do salário mínimo no Brasil e salva em um arquivo CSV."""
    response = requests.get(DIEESE_SALARIO)
    response.encoding = "utf-8"
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")

    dados = []
    ano_atual = None

    for row in table.find_all("tr"):
        if "subtitulo" in row.get("class", []):
            ano_atual = row.text.strip()
        else:
            cols = row.find_all("td")
            if len(cols) == 3:
                periodo = cols[0].text.strip()
                salario_nominal = cols[1].text.strip()
                salario_necessario = cols[2].text.strip()
                if periodo and salario_nominal and salario_necessario and ano_atual:
                    dados.append([ano_atual, periodo, salario_nominal, salario_necessario])

    df = pd.DataFrame(dados, columns=["Ano", "Período", "Salário Mínimo Nominal", "Salário Mínimo Necessário"])
    df.to_csv("salario_minimo.csv", index=False, encoding="utf-8", sep=";")
    print("Dados processados e salvos em 'salario_minimo.csv' com sucesso!")


def fetch_cesta_basica(cidade: int, data_inicial: str, data_final: str) -> pd.DataFrame:
    """Busca dados da cesta básica para uma cidade e período específico.

    Args:
        cidade (int): ID da cidade (conforme exibido na lista no site do DIEESE).
        data_inicial (str): Data inicial no formato MMAAAA.
        data_final (str): Data final no formato MMAAAA.

    Returns:
        pd.DataFrame: Dados formatados da cesta básica.
    """
    payload = {
        "farinha": "false",
        "produtos": "1",  # Total da cesta
        "tipoDado": "5",  # Gasto mensal
        "cidades": cidade,
        "dataInicial": data_inicial,
        "dataFinal": data_final,
    }

    response = requests.post(DIEESE_CESTA, data=payload)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tabela = soup.find("table", {"id": "dados"})
    if tabela is None:
        raise ValueError("Tabela de dados não encontrada no HTML retornado.")

    header = [th.text.strip() for th in tabela.find("thead").find_all("th")]

    rows = []
    for tr in tabela.find("tbody").find_all("tr"):
        cols = [td.text.strip() for td in tr.find_all("td")]
        rows.append(cols)

    df = pd.DataFrame(rows, columns=header)
    df["Cidade"] = cidade

    return df
