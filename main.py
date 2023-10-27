import os
import mysql.connector
import parameters as params

try:
    # Establishes connection to the database
    connection = mysql.connector.connect(**params.bd_config)

    # Creates a cursor
    cursor = connection.cursor()

    # Lists all files in the folder
    for arquivo in os.listdir(params.folder):
        if os.path.isfile(os.path.join(params.folder, arquivo)):
            # Gets the file name without the extension
            table_name = os.path.splitext(arquivo)[0]
            # Open the file for reading 
            with open(os.path.join(params.folder, arquivo), "r") as file:
                # Performs data insertion into the database
                for linha in file:
                    # Suppose each line of the file contains a value to be inserted into a table  called "your_table"
                    sql = "INSERT {table_name} (column) VALUES (%s)"
                    cursor.execute(sql, (linha.strip(),))

    # Commit the changes
    connection.commit()
    print("Ingestion completed successfully!")

except mysql.connector.Error as error:
    print(f"Error: {error}")

finally:
    # Close the cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals() and connection.is_connected():
        connection.close()
