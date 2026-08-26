import psycopg2

from src.analyses import run_analyses


def main():
    """Point d'entrée principal du projet."""
    try:
        run_analyses()
    except psycopg2.Error as error:
        print(f"Erreur PostgreSQL : {error}")


if __name__ == "__main__":
    main()
