import json
import pandas as pd
import sqlalchemy
import csv
import os
import random
import string

OUTPUT_FILE_PATH = "sample_data.csv"


def sample_data_generator(file_path, num_rows=2000000):
    """
    Generates a CSV file with sample data for testing.

    Parameters:
    - file_path (str): Path to the output CSV file.
    - num_rows (int): Number of rows to generate. For large datasets, this can be set to 2 million rows.

    The resulting file will contain two columns:
    - 'alphabets': Random strings in each row.
    - 'numbers': Sequential integers for each row.

    This function produces a large dataset (over 1 GB for 2 million rows) for testing purposes.
    """
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Alphabets", "Numbers"])

        for i in range(num_rows):
            random_string = ''.join(random.choices(string.ascii_letters, k=600))
            random_number = random.randint(1, 1000000)
            writer.writerow([random_string, random_number])


def load_config(file_path):
    """
    Loads database connection configuration from a JSON file.

    Parameters:
    - file_path (str): Path to the JSON configuration file.

    Returns:
    - dict: Configuration details for connecting to MySQL and PostgreSQL databases.

    """
    with open(file_path, 'r') as f:
        return json.load(f)


def create_mysql_engine(config):
    """
    Creates an SQLAlchemy engine for MySQL.

    Parameters:
    - config (dict): Dictionary containing MySQL connection details.

    Returns:
    - sqlalchemy.engine.Engine: Engine for MySQL connection using SQLAlchemy.
    """
    user_name = config['mysql']['user']
    password = os.environ['MYSQL_PASSWORD']
    engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@localhost/source_db")
    return engine


def get_data_from_file(path):
    """
    Loads data from a CSV file into a DataFrame.

    Parameters:
    - path (str): Path to the CSV file.

    Returns:
    - pandas.DataFrame: Data loaded from the CSV file.
    """
    return pd.read_csv(path, delimiter=';')


def put_data_into_mysql(pdf: pd.DataFrame, con, table_name):
    """
    Inserts data from a DataFrame into a MySQL table.

    Parameters:
    - df (pandas.DataFrame): Data to insert.
    - con (sqlalchemy.engine.Engine): Connection to the MySQL database.
    - table_name (str): Name of the table in MySQL where data will be inserted.
    """
    pdf.to_sql(table_name, con)


if __name__ == "__main__":
    sample_data_generator(OUTPUT_FILE_PATH)
    config = load_config('config.json')
    con = create_mysql_engine(config)
    data = get_data_from_file(OUTPUT_FILE_PATH)
    put_data_into_mysql(data, con, 'mysql_sample_table')

