import os
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv
from psycopg2 import pool


load_dotenv()

_DATABASE = os.getenv('POSTGRES_DATABASE')
_USERNAME = os.getenv('POSTGRES_USERNAME')
_PASSWORD = os.getenv('POSTGRES_PASSWORD')
_HOST = os.getenv('POSTGRES_HOST')
_PORT = os.getenv('POSTGRES_PORT')


# def get_postgres_connection():
#     try:
#         conn = psycopg2.connect(
#             dbname=_DATABASE, user=_USERNAME, password=_PASSWORD, host=_HOST, port=_PORT
#         )
#         return conn
#
#     except (Exception, psycopg2.Error) as error:
#         print(f"There is an error when trying to connect to postgres: {error}")


class PostgreSQLHandler:
    def __init__(self, db_config):
        self.pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=10, **db_config)

    @contextmanager
    def get_cursor(self):
        conn = self.pool.getconn()
        try:
            yield conn.cursor()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
            raise
        finally:
            self.pool.putconn(conn)

    def insert_mapping(self, milvus_id, filename):
        with self.get_cursor() as cur:
            cur.execute(
                "INSERT INTO file_mappings (milvus_id, filename) VALUES (%s, %s) ON CONFLICT (milvus_id) DO NOTHING",
                (milvus_id, filename)
            )

    def get_filename(self, milvus_id):
        with self.get_cursor() as cur:
            cur.execute(
                "SELECT filename FROM file_mappings WHERE milvus_id = %s",
                (milvus_id,)
            )
            result = cur.fetchone()
            return result[0] if result else None


db_config = {
    "database": _DATABASE,
    "user": _USERNAME,
    "password": _PASSWORD,
    "host": _HOST,
    "port": _PORT
}


db_handler = PostgreSQLHandler(db_config)
