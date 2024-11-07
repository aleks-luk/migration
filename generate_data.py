import json
import pandas as pd
import sqlalchemy
import csv
import random
import string

OUTPUT_FILE_PATH = "sample_data.csv"


def sample_data_generator(file_path, num_rows=2000000):
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Alphabets", "Numbers"])

        for i in range(num_rows):
            random_string = ''.join(random.choices(string.ascii_letters, k=600))
            random_number = random.randint(1, 1000000)
            writer.writerow([random_string, random_number])


def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def create_mysql_engine(config):
    user_name = config['mysql']['user']
    password = config['mysql']['password']
    engine = sqlalchemy.create_engine(f"mysql+pymysql://{user_name}:{password}@localhost/source_db")
    return engine


def get_data_from_file(path):
    return pd.read_csv(path, delimiter=';')


def put_data_into_mysql(pdf: pd.DataFrame, con, table_name):
    pdf.to_sql(table_name, con)


if __name__ == "__main__":
    sample_data_generator(OUTPUT_FILE_PATH)
    config = load_config('config.json')
    con = create_mysql_engine(config)
    data = get_data_from_file(OUTPUT_FILE_PATH)
    put_data_into_mysql(data, con, 'mysql_sample_table')

