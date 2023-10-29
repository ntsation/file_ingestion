import os
import mysql.connector
import parameters as params
import re  # Importe o módulo 're' para trabalhar com expressões regulares
import logging
import pandas as pd 



logger = logging.getLogger('data_ingestion')
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

def sanitize_table_name(name):
    return re.sub(r'[^a-zA-Z0-9]', '_', name)

def convert_xlsx_to_csv(xlsx_file):
    # Use pandas para ler o arquivo XLSX e converter em CSV
    df = pd.read_excel(xlsx_file)
    csv_file = os.path.splitext(xlsx_file)[0] + ".csv"
    df.to_csv(csv_file, index=False)

    return csv_file

def ingest_data(file):
    try:
        if file.endswith(".xlsx"):
            # Convert the XLSX file to CSV
            csv_file = convert_xlsx_to_csv(file)

            # Establish connection to the database
            connection = mysql.connector.connect(**params.bd_config)

            # Create a cursor
            cursor = connection.cursor()

            # Get the file name without the extension
            file_name = os.path.splitext(os.path.basename(csv_file))[0]

            # Create a sanitized table name
            table_name = sanitize_table_name(file_name)

            # Check if the table already exists
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = cursor.fetchone()

            if result:
                logger.info(f"Table '{table_name}' already exists. Deleting the old table...")
                # Delete the existing table
                cursor.execute(f"DROP TABLE {table_name}")

            # Create a new table in the database with the sanitized name
            create_table_query = f"CREATE TABLE {table_name} (data VARCHAR(255))"
            cursor.execute(create_table_query)

            # Open the CSV file for reading
            with open(csv_file, "r", encoding="utf-8") as file:
                for line in file:
                    sql = f"INSERT INTO {table_name} (data) VALUES (%s)"
                    cursor.execute(sql, (line.strip(),))

            # Commit the changes
            connection.commit()
            logger.info(f"Ingestion of file {csv_file} completed successfully!")

    except mysql.connector.Error as error:
        logger.error(f"Error: {error}")

    except Exception as e:
        logger.error(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":

    # List all files in the folder
    files = [os.path.join(params.folder, f) for f in os.listdir(params.folder) if os.path.isfile(os.path.join(params.folder, f))]

    # Ingest each file in the folder
    for file in files:
        if any(file.endswith(ext) for ext in params.target_extensions):
            logger.info(f"Ingesting file: {file}")
            ingest_data(file)
