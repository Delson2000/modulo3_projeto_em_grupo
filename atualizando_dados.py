from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime
import pandas as pd
import psycopg2




servico = Service(ChromeDriverManager().install()) 
navegador = webdriver.Chrome(service=servico)
navegador.maximize_window()

# Função para clicar em um botão especificado pelo XPath
def clicar(botao):
    try:
        # Espera até que o botão seja clicável
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, botao)))
        # Rola a página até o botão
        botao_element = navegador.find_element(By.XPATH, botao)
        navegador.execute_script("arguments[0].scrollIntoView(true);", botao_element)
        # Clica no botão
        botao_element.click()
    except TimeoutException:
        print("O botão não está mais disponível para clique.")

# XPath do botão "carregar mais"
carregar_mais = '/html/body/div[1]/div[2]/div/div[2]/div/div/div/div[2]/div/p[1]/button'

# DataFrame para armazenar os dados de todas as moedas
dados_completos = pd.DataFrame()

lista_moedas = ['bitcoin','ethereum','bnb','solana','cardano','dogecoin','polkadot-new','tron','uniswap','xrp']
# Iterar sobre cada moeda
for moeda in lista_moedas:
    corpo_link = f'https://coinmarketcap.com/pt-br/currencies/{moeda}/historical-data/'
    navegador.get(corpo_link)
    atualizar = 0
    if atualizar:
        # Rola a página para baixo e clica no botão "carregar mais" até que o botão desapareça
        while True:
            try:
                # Verifica se o botão está presente na página
                botao_element = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, carregar_mais)))
                # Clica no botão "carregar mais"
                clicar(carregar_mais)
                print("Botão 'Carregar mais' clicado")
                # Espera um pouco para a página carregar mais conteúdo
                time.sleep(2)
            except TimeoutException:
                # Se o botão não estiver mais presente, sai do loop
                print("Botão 'Carregar mais' não encontrado, assumindo que a tabela foi totalmente carregada.")
                break
    time.sleep(2)
    # Localiza a tabela após carregar mais conteúdo
    tabela = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/table')
    # Pega todas as linhas da tabela
    linhas = tabela.find_elements(By.TAG_NAME, 'tr')
    dados_tabela = []
    # Itera sobre as linhas e colunas para extrair os dados
    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, 'td')
        dados_linha = [coluna.text for coluna in colunas]
        print(dados_linha)
        # Adiciona o nome da moeda à lista de dados da linha
        dados_linha.append(moeda.capitalize())  # Adiciona o nome da moeda capitalizado
        dados_tabela.append(dados_linha)

    colunas = ['Data', 'abertura', 'maximo', 'minimo', 'fechamento', 'Volume', 'Cap_de_Mercado', 'Nome']

    # Cria um DataFrame a partir dos dados
    df_moeda = pd.DataFrame(dados_tabela, columns=colunas)
    df_moeda = df_moeda.drop(index=0)
    # Reseta os índices do DataFrame
    df_moeda.reset_index(drop=True, inplace=True)
    
    # Adiciona os dados desta moeda ao DataFrame principal
    dados_completos = pd.concat([dados_completos, df_moeda], ignore_index=True)

def tratar_dataframe(df):
    # Converter a coluna 'Data' para o formato dd/mm/aaaa
    df['Data'] = pd.to_datetime(df['Data'], format='%b %d, %Y').dt.strftime('%d/%m/%Y')
    
    # Converter colunas de valores para float
    for col in ['abertura', 'maximo', 'minimo', 'fechamento', 'Volume', 'Cap_de_Mercado']:
        df[col] = df[col].replace({'R\$': '', ',': ''}, regex=True).astype(float)

    df['Nome'] = df['Nome'].str.capitalize()  # Capitaliza o nome da moeda
    
    return df

df1 = tratar_dataframe(dados_completos)
# Salva os dados completos em um arquivo Excel
df1.to_excel('dados_moedas.xlsx', index=False)

df_antigo = pd.read_excel('dados_moedas2.xlsx')
nomes_desejados = [
    'Bitcoin', 'Ethereum', 'Bnb', 'Solana', 'Cardano',
    'Dogecoin', 'Polkadot-new', 'Tron', 'Uniswap', 'Xrp'
]

# Filtrar o DataFrame para incluir apenas as linhas com os nomes desejados
df_antigo = df_antigo[df_antigo['Nome'].isin(nomes_desejados)]


df_principal = pd.concat([df1,df_antigo]).drop_duplicates()

df_principal['Data'] = pd.to_datetime(df_principal['Data'], format="%d/%m/%Y")
df_principal =df_principal.sort_values(by=['Nome','Data'])
df_principal['Data'] = df_principal['Data'].dt.strftime('%d/%m/%Y')

df_principal.to_excel('dados_moedas_top10.xlsx', index=False)

navegador.quit()
###########################################################

moedas = df_principal

# Conecte-se ao banco de dados PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5434",
    database="postgres",
    user="postgres",
    password="senac@123",
    client_encoding="utf-8"
)

# Comando SQL para criar a tabela
create_table_query = """
CREATE TABLE IF NOT EXISTS dados_moedas (
    Data DATE,
    abertura NUMERIC,
    maximo NUMERIC,
    minimo NUMERIC,
    fechamento NUMERIC,
    Volume NUMERIC,
    Cap_de_Mercado NUMERIC,
    Nome VARCHAR(255),
    PRIMARY KEY (Data, Nome)
);
"""

# Criar um cursor para executar operações SQL
cur = conn.cursor()
# Executar o comando SQL para criar a tabela
cur.execute(create_table_query)

# Commit para confirmar a criação da tabela
conn.commit()

# Converter o DataFrame em uma lista de tuplas (cada tupla representa uma linha)
rows = [tuple(row) for row in moedas.values]

# Criar um cursor para executar operações SQL
cur = conn.cursor()

# Construir o comando SQL para inserção, com ON CONFLICT DO NOTHING
insert_query = """
INSERT INTO dados_moedas (Data, abertura, maximo, minimo, fechamento, Volume, Cap_de_Mercado, Nome)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (Data, Nome) DO NOTHING;
"""

# Executar a inserção de todos os registros
cur.executemany(insert_query, rows)

# Commit para confirmar a inserção
conn.commit()

# Fechar o cursor e a conexão
cur.close()
conn.close()

