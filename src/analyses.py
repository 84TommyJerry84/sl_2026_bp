from src.queries import (
    get_max_amplitude_route,
    get_stops_by_mode,
    get_top_10_routes_by_stops,
    get_transfers_by_station,
)


def run_analyses():
    """Exécute et affiche les analyses demandées."""

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
        print(
            f"Premier passage : {debut} | Dernier passage : {fin} | Amplitude : {delta}"
        )

    print("\n--- 4. CORRESPONDANCES PAR STATION ---")
    for station, count in get_transfers_by_station():
        print(f"{station} : {count} arrêts rattachés")
