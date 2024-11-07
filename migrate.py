import pandas as pd
import time
import psycopg2
import psycopg2.extras
from generate_data import create_mysql_engine, load_config
from memory_profiler import memory_usage

TABLE_NAME = 'pg_sample_table'


def create_postgres_connection(config):
    user_name = config['postgres']['user']
    password = config['postgres']['password']
    connection = psycopg2.connect(
        host="localhost",
        database="target_db",
        user=user_name,
        password=password,
    )
    connection.autocommit = True

    return connection


def create_staging_table(cursor):
    cursor.execute("""
    DROP TABLE IF EXISTS staging_pg_table;
    CREATE TABLE staging_pg_table (
        alphabets   TEXT,
        numbers     INTEGER
    )
    """)


def read_data_from_mysql(query, con):
    return pd.read_sql(query, con)


# def insert_data_to_postgres(connection, data, page_size=100):
#     with connection.cursor() as cursor:
#         create_staging_table(cursor)
#
#         rows = data[['Alphabets', 'Numbers']].values.tolist()
#
#         psycopg2.extras.execute_batch(cursor, """
#             INSERT INTO staging_pg_table (alphabets, numbers)
#                 VALUES (%s, %s)
#         """, rows, page_size)
#         connection.close()

def insert_data_to_postgres(connection, data, page_size):
    with connection.cursor() as cursor:
        create_staging_table(cursor)

        rows = [tuple(x) for x in data[['Alphabets', 'Numbers']].values]

        psycopg2.extras.execute_values(cursor, """
            INSERT INTO staging_pg_table (alphabets, numbers)
                VALUES %s
        """, rows, page_size=page_size)
        connection.close()


def migration_memory_usage(connection, data):
    mem_before = memory_usage()[0]
    start_time = time.time()
    insert_data_to_postgres(connection, data, 2000)
    end_time = time.time()
    mem_after = memory_usage()[0]

    execution_time = end_time - start_time
    memory_used = mem_before - mem_after
    print(f"Time: {execution_time:.2f}")
    print(f"Memory: {memory_used:.2f} MB")


if __name__ == '__main__':
    query = "SELECT * FROM mysql_sample_table"
    config = load_config('config.json')
    ms = create_mysql_engine(config)
    data = read_data_from_mysql(query, ms)
    connection = create_postgres_connection(config)
    migration_memory_usage(connection, data)
