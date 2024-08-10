import os

from dotenv import load_dotenv
from pymilvus import MilvusClient, connections

load_dotenv()


_HOST = os.getenv('MILVUS_HOST')
_PORT = os.getenv('MILVUS_PORT')
_DATABASE = os.getenv('MILVUS_DATABASE')
_COLLECTION = os.getenv('MILVUS_COLLECTION')


def get_connection():
    conn = connections.connect(
        host=_HOST,
        port=_PORT,
        db_name=_DATABASE
    )
    return conn


def get_client():
    try:
        client = MilvusClient(f"http://{_HOST}:{_PORT}")
        client.using_database(_DATABASE)
        return client
    except Exception as e:
        print(f"Could not create a client. Error: {e}")
