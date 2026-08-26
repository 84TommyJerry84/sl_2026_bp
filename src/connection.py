import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_db_config():
    return {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "sslmode": os.getenv("DB_SSLMODE"),
    }


def get_connection():
    return psycopg2.connect(**get_db_config())


# def test_connection():
#     connection = None

#     try:
#         config = get_db_config()
#         connection = psycopg2.connect(**config)

#         with connection.cursor() as cursor:
#             cursor.execute("SELECT current_database(), current_user;")
#             result = cursor.fetchone()

#         print(f"Base connectée : {result[0]}")
#         print(f"Utilisateur : {result[1]}")

#     finally:
#         if connection is not None:
#             connection.close()


# if __name__ == "__main__":
#     config = get_db_config()

#     print(f"Host : {config['host']}")
#     print(f"Port : {config['port']}")
#     print(f"Database : {config['dbname']}")
#     print(f"User : {config['user']}")
#     print(f"SSL mode : {config['sslmode']}")

# if __name__ == "__main__":
#     test_connection()
