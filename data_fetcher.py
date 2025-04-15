"""Código para buscar e processar dados do salário mínimo no Brasil."""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import DIEESE_ANALISE_CESTA


def fetch_data() -> None:
    """Busca dados do salário mínimo no Brasil e salva em um arquivo CSV."""
    response = requests.get(DIEESE_ANALISE_CESTA)
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

    # Criar DataFrame e salvar
    df = pd.DataFrame(dados, columns=["Ano", "Período", "Salário Mínimo Nominal", "Salário Mínimo Necessário"])
    df.to_csv("salario_minimo.csv", index=False, encoding="utf-8", sep=";")
    print("Dados processados e salvos em 'salario_minimo.csv' com sucesso!")
