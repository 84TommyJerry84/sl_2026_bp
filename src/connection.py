import os

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


if __name__ == "__main__":
    config = get_db_config()

    print(f"Host : {config['host']}")
    print(f"Port : {config['port']}")
    print(f"Database : {config['dbname']}")
    print(f"User : {config['user']}")
    print(f"SSL mode : {config['sslmode']}")