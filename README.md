# Projeto de Análise de Criptomoedas

Bem-vindo ao repositório do projeto de análise de criptomoedas! Este projeto foi desenvolvido para extrair, processar e analisar dados históricos de diversas criptomoedas utilizando Python, Selenium, Pandas e PowerBI. A seguir, você encontrará uma descrição detalhada dos arquivos e funcionalidades incluídas neste projeto.

## Descrição Geral

O objetivo deste projeto é fornecer uma solução completa para a extração, atualização e visualização de dados históricos de criptomoedas. Ele inclui as seguintes funcionalidades principais:

1. **Extração de Dados**: Coleta de dados históricos de criptomoedas diretamente do site CoinMarketCap.
2. **Atualização de Dados**: Combina novos dados com um arquivo Excel existente e mantém os dados sempre atualizados.
3. **Armazenamento de Dados**: Salva os dados atualizados em um banco de dados PostgreSQL.
4. **Visualização de Dados**: Utiliza o PowerBI para criar um dashboard interativo que facilita a análise dos dados armazenados.

## Estrutura do Projeto

O projeto está organizado em três arquivos principais:

1. **Extraindo_todos_os_dados.ipynb**
2. **atualizando_dados.py**
3. **BI Gráficos Final.pbix**

### 1. Extraindo_todos_os_dados.ipynb

Este notebook Jupyter é responsável por:

- Utilizar a biblioteca Selenium para navegar no site CoinMarketCap e extrair dados históricos de criptomoedas.
- Processar os dados extraídos usando a biblioteca Pandas.
- Salvar os dados processados em uma planilha Excel.

As 10 criptomoedas cujos dados são extraídos incluem:
- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Solana (SOL)
- Cardano (ADA)
- Dogecoin (DOGE)
- Polkadot (DOT)
- Tron (TRX)
- Uniswap (UNI)
- XRP (XRP)

### 2. atualizando_dados.py

Este script Python é responsável por:

- Carregar o arquivo Excel existente contendo os dados históricos de criptomoedas.
- Atualizar o arquivo Excel com novos dados coletados até a data atual.
- Salvar os dados atualizados em um banco de dados PostgreSQL utilizando a biblioteca psycopg2.

### 3. BI Gráficos Final.pbix

Este arquivo PowerBI contém um dashboard interativo que:

- Conecta-se ao banco de dados PostgreSQL para obter os dados atualizados de criptomoedas.
- Transforma os dados em visualizações gráficas que facilitam a análise e a tomada de decisões.

## Como Utilizar

### Pré-requisitos

- Python 3.7 ou superior
- Selenium
- Pandas
- Psycopg2
- PostgreSQL
- PowerBI Desktop

### Passos para Execução

1. **Extração de Dados**:
   - Abra e execute o notebook `Extraindo_todos_os_dados.ipynb` para coletar e salvar os dados históricos de criptomoedas.

2. **Atualização de Dados**:
   - Execute o script `atualizando_dados.py` para atualizar o arquivo Excel com os dados mais recentes e salvar as informações no banco de dados PostgreSQL.

3. **Visualização de Dados**:
   - Abra o arquivo `BI Gráficos Final.pbix` no PowerBI Desktop e conecte-o ao banco de dados PostgreSQL para visualizar os dados atualizados.

