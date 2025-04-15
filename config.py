"""Configuração para o projeto de análise de dados do salário mínimo."""

DIEESE_URL = "https://www.dieese.org.br"
DIEESE_SALARIO = f"{DIEESE_URL}/analisecestabasica/salarioMinimo.html"

DIEESE_CESTA = f"{DIEESE_URL}/cesta/produto"

DATA_SOURCE = {
    "nome": "DIEESE - Pesquisa Nacional da Cesta Básica de Alimentos",
    "link": "https://www.dieese.org.br/",
}
SALARIO_MINIMO_FILE = "static/tables/salario_minimo_tratado.csv"
CRESCIMENTO_FILE = "static/tables/poder_de_compra_e_crescimento.csv"
CESTA_BASICA_FILE = "static/tables/cesta_basica_tratado.csv"
DADOS_UTEIS = "static/tables/dados_uteis.csv"

# Cidades disponíveis no site do DIEESE
CIDADE_MAP = {
    16: "Aracaju",
    13: "Belém",
    2: "Belo Horizonte",
    22: "Boa Vista",
    9: "Brasília",
    19: "Campo Grande",
    25: "Cuiabá",
    4: "Curitiba",
    1: "Florianópolis",
    11: "Fortaleza",
    10: "Goiânia",
    3: "João Pessoa",
    18: "Macaé",
    21: "Macapá",
    28: "Maceió",
    17: "Manaus",
    15: "Natal",
    26: "Palmas",
    5: "Porto Alegre",
    23: "Porto Velho",
    12: "Recife",
    20: "Rio Branco",
    6: "Rio de Janeiro",
    7: "Salvador",
    27: "São Luís",
    8: "São Paulo",
    24: "Teresina",
    14: "Vitória",
    0: "Todas as cidades",
}

# Mapeamento de meses do português para inglês
MESES_MAP = {
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
