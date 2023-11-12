import os
import mysql.connector
import parameters as params
import re
import logging
import pandas as pd
import csv

# Logger configuration to save to a file
logger = logging.getLogger('data_ingestion')
logger.setLevel(logging.INFO)
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.txt')
log_handler = logging.FileHandler(log_file_path)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

def normalize_table_name(name):
    return re.sub(r'[^a-zA-Z0-9]', '_', name)

def normalize_column_name(column_name):
    return re.sub(r'[^a-zA-Z0-9]', '_', column_name.lower())


def detect_csv_delimiter(file):
    delimiters = [',', ';'] 

    with open(file, 'r', encoding='utf-8') as f:
        first_line = f.readline()

        for delimiter in delimiters:
            if delimiter in first_line:
                return delimiter

    logger.warning("Unable to detect CSV delimiter. Using default delimiter: ','")
    return ','


# Function for data ingestion
def ingest_data(file):
    try:
        delimiter = detect_csv_delimiter(file)
        connection = mysql.connector.connect(**params.bd_config)
        cursor = connection.cursor()
        file_name = os.path.splitext(os.path.basename(file))[0]
        table_name = normalize_table_name(file_name)
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()

        if result:
            logger.info(f"Table '{table_name}' already exists. Deleting the old table...")
            cursor.execute(f"DROP TABLE {table_name}")

        with open(file, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=delimiter)
            header = next(csv_reader) 

            logger.info(f"Detected CSV delimiter: '{delimiter}'")
            logger.info(f"CSV Header: {header}")

            normalized_header = [normalize_column_name(column) for column in header]

            create_table_query = f"CREATE TABLE {table_name} ({', '.join([f'{column} VARCHAR(255)' for column in normalized_header])})"
            logger.info(f"Executing SQL: {create_table_query}")
            cursor.execute(create_table_query)
            logger.info("Table creation complete.")

            for row in csv_reader:
                columns = ', '.join(normalized_header)
                values = ', '.join(['%s'] * len(normalized_header))
                sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                cursor.execute(sql, tuple(row))

        connection.commit()
        logger.info(f"Ingestion of file {file} completed successfully!")

    except mysql.connector.Error as error:
        logger.error(f"MySQL Error: {error}")

    except Exception as e:
        logger.error(f"Error: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    files = [os.path.join(params.folder, f) for f in os.listdir(params.folder) if os.path.isfile(os.path.join(params.folder, f))]
    for file in files:
        if any(file.endswith(ext) for ext in params.target_extensions):
            logger.info(f"Ingesting file: {file}")
            ingest_data(file)
