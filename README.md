# Projeto de ingestão de arquivos de banco de dados 🐍📁

Este repositório contém código Python para ingerir arquivos em um banco de dados MariaDB.O projeto visa facilitar o carregamento de dados de vários formatos de arquivo, como CSV ou Excel, em um banco de dados.

## Pré-requisitos 📋

Antes de começar a usar o projeto, verifique se você possui os seguintes pré-requisitos instalados:

- Python 3.x
- Bibliotecas Python Necessárias (Listadas em 'requirements.txt')
- Instale e configure o Banco de dados.

## Uso 🚀

Para usar o script de ingestão de dados para o Banco de dados, siga estas etapas:

1. **`parameters.py`:** Modifique o arquivo chamado `parameters.py` e defina os parâmetros de conexão para o seu banco de dados. O `parametros.py` deve conter um dicionário nomeado `bd_config` com os detalhes de conexão necessários.Aqui está um exemplo de como esse parâmetro pode ser:

    ```python
    # parametros.py
    bd_config = {
        "host": "SEU_HOST",
        "user": "SEU_USUÁRIO",
        "password": "SUA_SENHA",
        "database": "NOME_DATABASE"
    }

    pasta = 'caminho_da_pasta_com_arquivos'
    ```

    Substitua `'SEU_USUÁRIO'`, `'SUA_SENHA'`, `'SEU_HOST'`, `'NOME_DATABASE'`, e `'caminho_da_pasta_com_arquivos'` com suas credenciais de MariaDB e a pasta que contém os arquivos de texto que você deseja ingerir.

2. **`requirements.txt`** O arquivo `requirements.txt` contem as dependências necessárias da biblioteca, você pode instalar o usando `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. **Execute o script:** Execute o script `main.py` para começar a monitorar a pasta especificada para novos arquivos e ingerir dados no seu banco de dados.

## Contribuição 🤝

Sinta -se à vontade para contribuir com este projeto, criando problemas, sugerindo melhorias ou enviando solicitações de puxar.
