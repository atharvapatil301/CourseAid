import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")


def connect():
    try:
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass,
            port=db_port,
        )
        cursor = connection.cursor()

        #execute assistant_queries with cursor
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()
        print(db_version)
        print("connected successfully")
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL:{e}")
        return
    return connection



def close(connection):

        connection.close()
        print("PostgreSQL connection closed.")