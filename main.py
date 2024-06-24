import os
import mysql.connector
import parametros
import re
import logging
import csv

# Configuração do logger para salvar em um arquivo
logger = logging.getLogger('ingestao_dados')
logger.setLevel(logging.INFO)
log_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'log.txt')
log_handler = logging.FileHandler(log_file_path)
log_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)


def normaliza_tabela(nome):
    return re.sub(r'[^a-zA-Z0-9]', '_', nome)


def normaliza_coluna(nome_coluna):
    return re.sub(r'[^a-zA-Z0-9]', '_', nome_coluna.lower())


def detecta_delimitador(arquivo):
    delimitadores = [',', ';']

    with open(arquivo, 'r', encoding='utf-8') as f:
        primeira_linha = f.readline()

        for delimitador in delimitadores:
            if delimitador in primeira_linha:
                return delimitador

    logger.warning("Não foi possível detectar o delimitador CSV. Usando delimitador padrão : ','")

    return ','


# Função para ingestão de dados
def ingestao_dados(arquivo):
    try:
        delimitador = detecta_delimitador(arquivo)
        conexao = mysql.connector.connect(**parametros.bd_config)
        cursor = conexao.cursor()
        nome_arquivo = os.path.splitext(os.path.basename(arquivo))[0]
        nome_tabela = normaliza_tabela(nome_arquivo)
        cursor.execute(f"SHOW TABLES LIKE '{nome_tabela}'")
        resultado = cursor.fetchone()

        if resultado:
            logger.info(
                f"A tabela '{nome_tabela}' já existe. Excluindo a tabela antiga...")
            cursor.execute(f"DROP TABLE {nome_tabela}")

        with open(arquivo, "r", encoding="utf-8") as arquivo_csv:
            ler_csv = csv.reader(arquivo_csv, delimiter=delimitador)
            header = next(ler_csv)

            logger.info(f"Delimitador CSV detectado: '{delimitador}'")
            logger.info(f"Cabeçalho: {header}")

            normaliza_header = [normaliza_coluna(coluna) for coluna in header]

            cria_tabela_query = f"CREATE TABLE {nome_tabela} ({', '.join(
                [f'{coluna} VARCHAR(255)' for coluna in normaliza_header])})"
            logger.info(f"Executando SQL: {cria_tabela_query}")
            cursor.execute(cria_tabela_query)
            logger.info("Criação de tabela concluída.")

            for linha in ler_csv:
                colunas = ', '.join(normaliza_header)
                valores = ', '.join(['%s'] * len(normaliza_header))
                sql = f"INSERT INTO {
                    nome_tabela} ({colunas}) VALUES ({valores})"
                cursor.execute(sql, tuple(linha))

        conexao.commit()
        logger.info(f"Ingestão do arquivo {arquivo} concluído com sucesso!")

    except mysql.connector.Error as error:
        logger.error(f"Erro MySQL: {error}")

    except Exception as e:
        logger.error(f"Erro: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and conexao.is_connected():
            conexao.close()


if __name__ == "__main__":
    arquivos = [os.path.join(parametros.pasta, f) for f in os.listdir(
        parametros.pasta) if os.path.isfile(os.path.join(parametros.pasta, f))]
    for arquivo in arquivos:
        if any(arquivo.endswith(ext) for ext in parametros.extensoes):
            logger.info(f"Ingerindo arquivo: {arquivo}")
            ingestao_dados(arquivo)
