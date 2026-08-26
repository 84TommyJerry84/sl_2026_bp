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


def get_stops_by_mode():
    """1. Nombre d'arrêts uniques par mode de transport."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        CASE r.route_type
                            WHEN 0 THEN 'Tramway'
                            WHEN 1 THEN 'Métro'
                            WHEN 2 THEN 'RER'
                        END AS mode_transport,
                        COUNT(DISTINCT st.stop_id) AS nombre_arrets
                    FROM routes AS r
                    INNER JOIN trips AS t
                        ON r.route_id = t.route_id
                    INNER JOIN stop_times AS st
                        ON t.trip_id = st.trip_id
                    WHERE r.route_type IN (0, 1, 2)
                    GROUP BY r.route_type
                    ORDER BY nombre_arrets DESC;
                    """
                )

                return cur.fetchall()


def get_top_10_routes_by_stops():
    """2. Top 10 des lignes desservant le plus d'arrêts."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        r.route_short_name,
                        r.route_long_name,
                        COUNT(DISTINCT st.stop_id) AS nombre_arrets
                    FROM routes AS r
                    INNER JOIN trips AS t
                        ON r.route_id = t.route_id
                    INNER JOIN stop_times AS st
                        ON t.trip_id = st.trip_id
                    GROUP BY r.route_id, r.route_short_name, r.route_long_name
                    ORDER BY nombre_arrets DESC
                    LIMIT 10;
                    """
                )
                return cur.fetchall()


def get_max_amplitude_route():
    """3. Ligne avec la plus grande amplitude horaire."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        r.route_short_name,
                        r.route_long_name,
                        MIN(st.departure_time::interval) AS premier_passage,
                        MAX(st.arrival_time::interval) AS dernier_passage,
                        MAX(st.arrival_time::interval)
                            - MIN(st.departure_time::interval) AS amplitude
                    FROM routes AS r
                    INNER JOIN trips AS t
                        ON r.route_id = t.route_id
                    INNER JOIN stop_times AS st
                        ON t.trip_id = st.trip_id
                    GROUP BY
                        r.route_id,
                        r.route_short_name,
                        r.route_long_name
                    ORDER BY amplitude DESC
                    LIMIT 1;
                    """
                )

                return cur.fetchone()


def get_transfers_by_station():
    """4. Nombre d'arrêts rattachés à chaque station."""
    with closing(get_connection()) as conn:  # noqa: SIM117
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        parent.stop_name AS station_nom,
                        COUNT(DISTINCT child.stop_id) AS nombre_arrets_rattaches
                    FROM stops AS parent
                    INNER JOIN stops AS child
                        ON child.parent_station = parent.stop_id
                    WHERE parent.location_type = 1
                    GROUP BY parent.stop_id, parent.stop_name
                    ORDER BY nombre_arrets_rattaches DESC;
                    """
                )

                return cur.fetchall()


if __name__ == "__main__":
    print("\n--- 1. ARRÊTS PAR MODE DE TRANSPORT ---")
    for mode, count in get_stops_by_mode():
        print(f"{mode} : {count} arrêts")

    print("\n--- 2. TOP 10 LIGNES (NOMBRE D'ARRÊTS) ---")
    for short_name, long_name, count in get_top_10_routes_by_stops():
        print(f"[{short_name}] {long_name} : {count} arrêts")

    print("\n--- 3. PLUS GRANDE AMPLITUDE HORAIRE ---")
    amplitude_row = get_max_amplitude_route()
    if amplitude_row:
        short_name, long_name, debut, fin, delta = amplitude_row
        print(f"[{short_name}] {long_name}")
        print(f"Premier passage: {debut} | Dernier passage: {fin} | Amplitude: {delta}")

    print("\n--- 4. CORRESPONDANCES PAR STATION ---")
    for station, count in get_transfers_by_station():
        print(f"{station} : {count} arrêts rattachés")

# if __name__ == "__main__":
#     tables = ["routes", "trips", "stop_times", "stops"]

#     for table in tables:
#         print(f"\n--- {table} ---")

#         for column_name, data_type in list_columns(table):
#             print(f"{column_name} : {data_type}")

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
