# MariaDB Database File Ingestion Project 🐍📁

This repository contains Python code for ingesting files into a MariaDB database. The project aims to facilitate the loading of data from various file formats, such as CSV or Excel, into a MariaDB database.

## Pre-requisites 📋

Before you begin using the project, ensure that you have the following pre-requisites installed:

- Python 3.x
- Required Python libraries (listed in 'requirements.txt')
- Installed and configured MariaDB

## Usage 🚀

To use the data ingestion script for MariaDB, follow these steps:

1. **Create `parameters.py`:** Create a file named `parameters.py` and define the connection parameters for your MariaDB database. The `parameters.py` file should contain a dictionary named `bd_config` with the required connection details. Here's an example of what this file might look like:

    ```python
    # parameters.py
    bd_config = {
        'user': 'your_username',
        'password': 'your_password',
        'host': 'localhost',
        'database': 'your_database',
    }

    folder = 'path_to_folder_with_text_files'
    ```

    Replace `'your_username'`, `'your_password'`, `'localhost'`, `'your_database'`, and `'path_to_folder_with_text_files'` with your MariaDB credentials and the folder containing the text files you want to ingest.

2. **Create a `requirements.txt` file:** Create a `requirements.txt` file with the necessary library dependencies by running the following commands:

    ```bash
    echo "watchdog==2.1.6" > requirements.txt
    echo "mysql-connector-python==8.0.28" >> requirements.txt
    ```

    Then, you can install the required libraries using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the script:** Execute the main Python script to start monitoring the specified folder for new files and ingesting data into your MariaDB database.

## Contributing 🤝

Feel free to contribute to this project by creating issues, suggesting improvements, or submitting pull requests.

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Happy data ingestion! 🚀
