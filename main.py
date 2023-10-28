import os
import mysql.connector
import parameters as params
import time 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler




class MonitorDirectory(FileSystemEventHandler):
    def on_created (self, event):
        if event.is_directory:
            return
        elif any(event.src_path.endswith(ext) for ext in params.target_extensions):
            print(f"New file found: {event.src_path}")
            # Place the data ingestion code here
            ingest_data(event.src_path)

def ingest_data(file):
    try:
        # Establishes connection to the database
        connection = mysql.connector.connect(**params.bd_config)

        # Creates a cursor
        cursor = connection.cursor()

        # Gets the file name without the extension
        table_name = os.path.splitext(os.path.basename(file))[0]

        # Create a table in the database with the same name as the file 
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (column VARCHAR(255))")

        # Open the file for reading
        with open(file, "r") as file:
            # Performs data insertion into the database
            for line in file:
                sql = f"INSERT INTO {table_name} (column) VALUES (%s)"
                cursor.execute(sql, (line.strip(),))

        # Commit the changes
        connection.commit()
        print(f"Ingestion of file {file} completed successfully!")

    except mysql.connector.Error as error:
        print(f"Error: {error}")
    
    finally:
        # Close the cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
        event_handler = MonitorDirectory()
        observer = Observer()
        observer.schedule(event_handler, params.folder, recursive=True)
        observer.start()

        try:
             print(f"Monitoring folder: {params.folder}")
             while True:
                  time.sleep(1)
        except KeyboardInterrupt:
             observer.stop()
        observer.join()