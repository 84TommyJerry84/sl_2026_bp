# from src.connection import get_db_config

from contextlib import closing

from src.connection import get_connection


def list_tables():
    """Retourne la liste des tables du schéma public."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                    """
                )

                return cur.fetchall()


def list_columns(table_name):
    """Retourne les colonnes et leurs types pour une table."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = %s
                    ORDER BY ordinal_position;
                    """,
                    (table_name,),
                )

                return cur.fetchall()


if __name__ == "__main__":
    tables = ["routes", "trips", "stop_times", "stops"]

    for table in tables:
        print(f"\n--- {table} ---")

        for column_name, data_type in list_columns(table):
            print(f"{column_name} : {data_type}")

# def list_tables():
#     connection = None

#     try:
#         connection = psycopg2.connect(**get_db_config())

#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """
#                 SELECT table_name
#                 FROM information_schema.tables
#                 WHERE table_schema = 'public'
#                 ORDER BY table_name;
#                 """
#             )

#             return cursor.fetchall()

#     finally:
#         if connection is not None:
#             connection.close()


# if __name__ == "__main__":
#     tables = list_tables()

#     for table in tables:
#         print(table[0])
