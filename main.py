"""Arquivo principal do projeto, que coordena a execução das etapas de extração, limpeza e visualização dos dados."""
import json

import pandas as pd
from flask import Flask, render_template, request

from config import CRESCIMENTO_FILE, DATA_SOURCE, SALARIO_MINIMO_FILE
from data_analisys import plot_data, processar_dados_economicos
from data_cleaner import clean_cesta_basica, clean_salario
from data_fetcher import fetch_cesta_basica, fetch_salario

app = Flask(__name__)


def load_csv_to_dict(file_path: str, sep: str = ";") -> list[dict]:
    """Load a CSV file and convert it to a list of dictionaries."""
    data_frame = pd.read_csv(file_path, sep=sep)
    return data_frame.to_dict(orient="records")


@app.route("/")
def home() -> str:
    """Rota inicial da aplicação Flask."""
    # Processar os dados gerais
    dados_economicos = processar_dados_economicos()

    # Obter dados históricos
    salario_data = pd.read_csv(SALARIO_MINIMO_FILE, sep=";")
    salario_data = salario_data.drop_duplicates(subset="Ano")
    salario_data["% Salário Comprometido com Cesta"] = (
        (dados_economicos["custo_cesta_basica_media"] / salario_data["Salário Mínimo Nominal"]) * 100
    ).round(2)

    # Preparar dados para o gráfico
    grafico_dados = salario_data.head(10)
    grafico_dados = grafico_dados.iloc[::-1]
    labels = grafico_dados["Ano"].tolist()
    salario_nominal_data = grafico_dados["Salário Mínimo Nominal"].tolist()
    salario_necessario_data = grafico_dados["Salário Mínimo Necessário"].tolist()
    salario_comprometido_data = grafico_dados["% Salário Comprometido com Cesta"].tolist()

    # Retornar o template com os dados serializados em JSON
    return render_template(
        "index.html",
        fonte_dados=DATA_SOURCE,
        salario_nominal_atual=dados_economicos["salario_nominal_atual"],
        salario_necessario_atual=dados_economicos["salario_necessario_atual"],
        custo_cesta_basica_media=dados_economicos["custo_cesta_basica_media"],
        labels=json.dumps(labels),  # Converte listas para JSON
        salario_nominal_data=json.dumps(salario_nominal_data),
        salario_necessario_data=json.dumps(salario_necessario_data),
        salario_comprometido_data=json.dumps(salario_comprometido_data),
    )


@app.route("/salario_minimo")
def analise_salario_minimo() -> str:
    """Rota para a análise do salário mínimo."""
    fetch_salario()
    clean_salario()
    plot_data()
    tabela_salario = load_csv_to_dict(SALARIO_MINIMO_FILE)
    crescimento_data = load_csv_to_dict(CRESCIMENTO_FILE, sep=",")

    return render_template(
        "salario_minimo.html",
        tabela_salario=tabela_salario,
        tabela_crescimento=crescimento_data,
        fonte_dados=DATA_SOURCE,
    )


@app.route("/cesta", methods=["POST", "GET"])
def consulta_cesta_basica() -> str:
    """Rota para consulta da cesta básica."""
    if request.method == "POST":
        cidade = int(request.form.get("cidade", 8))  # Default: São Paulo
        data_inicial = request.form.get("data_inicial", "012023")
        data_final = request.form.get("data_final", "102023")

        data_frame = clean_cesta_basica(fetch_cesta_basica(cidade, data_inicial, data_final))

        return render_template(
            "cesta_basica.html",
            tabela_cesta=data_frame.to_dict(orient="records"),  # Dados transformados para a tabela
            fonte_dados=DATA_SOURCE,
        )

    return render_template("cesta_basica.html", fonte_dados=DATA_SOURCE)


if __name__ == "__main__":
    # Executado apenas em ambiente de desenvolvimento local
    app.run(debug=False, host="0.0.0.0", port=5000)
