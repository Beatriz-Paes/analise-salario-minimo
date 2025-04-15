"""Arquivo principal do projeto, que coordena a execução das etapas de extração, limpeza e visualização dos dados."""
import pandas as pd
from flask import Flask, render_template

from data_analisys import plot_data
from data_cleaner import clean_data
from data_fetcher import fetch_data

app = Flask(__name__)


@app.route("/")
def home() -> str:
    """Rota inicial da aplicação Flask."""
    df = pd.read_csv("static/tables/salario_minimo_tratado.csv", sep=";")
    df_crescimento = pd.read_csv("static/tables/poder_de_compra_e_crescimento.csv")
    tabela_dados_brutos = df.to_dict(orient="records")
    tabela_crescimento = df_crescimento.to_dict(orient="records")

    fonte_dados = {
        "nome": "DIEESE - Pesquisa Nacional da Cesta Básica de Alimentos",
        "link": "https://www.dieese.org.br/",
    }

    return render_template(
        "index.html", tabela_dados=tabela_dados_brutos, tabela_crescimento=tabela_crescimento, fonte_dados=fonte_dados
    )


def main() -> None:
    """Função principal para coordenar o fluxo do programa."""
    try:
        print("\n> Etapa 1: Extração dos Dados...")
        fetch_data()

        print("\n> Etapa 2: Limpeza dos Dados...")
        clean_data()

        print("\n> Etapa 3: Geração do Gráfico...")
        plot_data()
    except Exception as e:
        print(f"Erro encontrado durante a execução: {e}")


if __name__ == "__main__":
    # Executado apenas em ambiente de desenvolvimento local
    main()
    app.run(debug=True, host="0.0.0.0", port=5000)
