# Análise e Visualização do Salário Mínimo no Brasil

Este projeto tem como objetivo analisar a evolução do salário mínimo no Brasil, comparando valores históricos, crescimento nominal e poder de compra ao longo dos anos. Ele utiliza ferramentas de coleta, limpeza, análise e visualização de dados para transformar informações de fontes confiáveis em gráficos e tabelas interativas.

---

## Funcionalidades Principais

1. **Coleta de Dados:**
   - Os dados são extraídos automaticamente da página do **DIEESE - Pesquisa Nacional da Cesta Básica de Alimentos**.

2. **Limpeza e Tratamento:** 
   - Remoção e formatação de valores como símbolos monetários.
   - Conversão de valores para tipos numéricos, garantindo a consistência dos dados.

3. **Análises e Graficagem:**
   - Análise do crescimento nominal do salário mínimo.
   - Comparação do poder de compra.
   - Geração automática de gráficos e tabelas para visualização.

4. **Visualização Interativa:**
   - Um servidor web exibe as análises por meio de uma interface construída com Flask. 
   - Tabelas interativas e gráficos estilizados com **DataTables** e **Chart.js**.

---

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas:

- **Python 3.8 ou superior**
- **Pip (gerenciador de pacotes do Python)**

---

## Instalação e Configuração

Siga estas etapas para configurar e executar o projeto:

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

### 2. Instale os pacotes necessários
```bash
pip install -r requirements.txt
```

### 3. Execute o programa
A aplicação possui uma interface web que pode ser executada com:
```bash
python main.py
```
Acesse o endereço do servidor local no navegador:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)


---

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

### 1. **Arquivos de Código**
- **`main.py`**: Coordena o fluxo principal do projeto e inicializa o servidor Flask.
- **`data_fetcher.py`**: Coleta os dados brutos da fonte (DIEESE) e salva em um arquivo CSV.
- **`data_cleaner.py`**: Realiza limpeza e normalização dos dados da CSV gerada.
- **`data_analisys.py`**: Contém funções para análise e visualizações baseadas em gráficos.
- **`config.py`**: Contém URLs e configurações globais da aplicação.

### 2. **Recursos de Dados**
- **`salario_minimo.csv`**: Dados coletados brutos, armazenando salários mínimos e necessários.
- **`static/tables/salario_minimo_tratado.csv`**: Dados tratados para análises adicionais.

### 3. **Interface Web**
- **`index.html`**: Apresenta os dados analisados e gráficos interativos no navegador.

### 4. **Dependências**
- **`requirements.txt`**: Lista os pacotes externos necessários para rodar o projeto:
  - `requests` e `beautifulsoup4`: Para coleta de dados.
  - `pandas`: Para tratamento e análise de dados.
  - `matplotlib` e `seaborn`: Para visualização.
  - `pre-commit`: Para consistência e padronização do código.

---

## Funcionamento do Projeto

As principais etapas do fluxo de execução são:

1. **Extração:**
   - O script `data_fetcher.py` coleta a tabela de salários diretamente do DIEESE e salva o arquivo CSV bruto.

2. **Limpeza:**
   - `data_cleaner.py` adequa os dados brutos, remove valores inconsistentes e os salva em um formato processável.

3. **Análises e Visualização:**
   - `data_analisys.py` realiza cálculos detalhados, como:
     - Crescimento nominal do salário (percentual ano a ano).
     - Poder de compra em diferentes períodos.
   - Gráficos de barras e linhas são gerados automaticamente, prontos para visualização.

4. **Apresentação:**
   - `index.html` serve como interface web para exibir os gráficos e tabelas gerados.

---

## Tabelas e Gráficos Gerados

1. **Tabela - Evolução do Salário Mínimo**
   - Exibe os salários nominais e necessários ao longo dos anos.

2. **Gráfico - Crescimento Nominal do Salário Mínimo**
   - Mostra o percentual de crescimento do salário ano a ano.

3. **Gráfico - Evolução do Poder de Compra**
   - Representa o poder de compra em percentual comparativo.

4. **Gráfico - Salário Nominal x Salário Necessário**
   - Exibe a variação dos dois tipos de salário em uma linha do tempo.

---

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar **issues** ou criar um **pull request**.

### Configuração de Pre-Commit Hook

Este projeto utiliza o pacote `pre-commit` para validação de código antes de commitar mudanças. Inicie com:

1. Instale o pre-commit:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. Faça suas modificações e commit normalmente:
   ```bash
   git commit -m "Sua mensagem"
   ```

---

## Fonte dos Dados

Os dados apresentados são coletados da página oficial do DIEESE:
- [DIEESE - Análise da Cesta Básica](https://www.dieese.org.br/analisecestabasica/salarioMinimo.html)

---

## Licença

Este projeto está licenciado sob a licença **MIT**. Consulte o arquivo LICENSE para obter mais informações.

---
