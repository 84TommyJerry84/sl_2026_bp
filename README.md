# sl-2026-bp

## Présentation

Ce projet a pour objectif d'interroger une base de données PostgreSQL distante contenant des données GTFS des transports d'Île-de-France.

Le projet permet de réaliser plusieurs analyses sur les lignes de métro, RER et tramway tout en appliquant de bonnes pratiques de développement Python et SQL.

L'objectif est notamment de travailler sur :

* la gestion sécurisée des informations de connexion ;
* la structuration d'un projet Python ;
* la fermeture correcte des connexions PostgreSQL ;
* l'écriture de requêtes SQL lisibles et maintenables ;
* l'utilisation de Ruff pour le formatage et le contrôle du code.

## Architecture du projet

```text
sl-2026-bp/
│
├── src/
│   ├── __init__.py
│   ├── connection.py
│   ├── queries.py
│   ├── analyses.py
│   └── main.py
│
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Rôle des fichiers

| Fichier            | Rôle                                                                 |
| ------------------ | -------------------------------------------------------------------- |
| `connection.py`    | Charge les variables d'environnement et crée la connexion PostgreSQL |
| `queries.py`       | Contient les requêtes SQL utilisées pour les analyses                |
| `analyses.py`      | Exécute les analyses et affiche les résultats                        |
| `main.py`          | Point d'entrée principal du projet                                   |
| `.env`             | Contient les informations réelles de connexion, non versionnées      |
| `.env.example`     | Montre les variables nécessaires sans contenir de secret             |
| `requirements.txt` | Contient les dépendances Python avec leurs versions                  |

## Prérequis

Le projet nécessite :

```text
Python 3
Git
Un accès à la base PostgreSQL distante

Pour le bonus :
Docker
Docker Compose
```

Il est recommandé d'utiliser un environnement virtuel Python.

## Installation

Cloner le dépôt :

```bash
git clone https://github.com/84TommyJerry84/sl_2026_bp.git
cd sl_2026_bp
```

Créer l'environnement virtuel :

```bash
python -m venv env
```

Sous PowerShell, activer l'environnement :

```powershell
.\env\Scripts\Activate.ps1
```

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

## Configuration de la connexion PostgreSQL

Créer un fichier `.env` à la racine du projet à partir du modèle `.env.example`.

Le fichier doit contenir :

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_SSLMODE=
```

Les valeurs réelles sont fournies séparément et ne doivent jamais être ajoutées au dépôt Git.

Le fichier `.env` est exclu du dépôt grâce au `.gitignore`.

## Gestion des connexions

La connexion PostgreSQL est créée dans `connection.py`.

Les connexions sont utilisées avec `contextlib.closing` :

```python
with closing(get_connection()) as conn:
    with conn:
        with conn.cursor() as cur:
            ...
```

Cette structure permet de gérer plusieurs éléments.

`closing()` garantit la fermeture de la connexion à la fin du traitement.

`with conn` gère la transaction et effectue un commit si le traitement se termine correctement ou un rollback en cas d'erreur.

`with conn.cursor()` garantit la fermeture du curseur après l'exécution de la requête.

Cette gestion est importante car la base PostgreSQL est distante et partagée avec plusieurs utilisateurs.

Lors d'une exécution avec Docker Compose, les variables du fichier `.env` peuvent être configurées pour utiliser la base PostgreSQL locale créée par le service `db`.

## Lancer le projet

Depuis la racine du projet :

```bash
python -m src.main
```

Le programme exécute les quatre analyses demandées et affiche les résultats dans le terminal.

## Analyses réalisées

### 1. Nombre d'arrêts par mode de transport

Cette analyse compte les arrêts distincts desservis pour chaque mode de transport étudié.

Résultats obtenus :

```text
Métro : 803 arrêts
Tramway : 580 arrêts
RER : 242 arrêts
```

L'utilisation de `COUNT(DISTINCT stop_id)` évite de compter plusieurs fois un même arrêt présent dans plusieurs trajets.

### 2. Top 10 des lignes desservant le plus d'arrêts

Résultats obtenus :

```text
8   : 76 arrêts
7   : 76 arrêts
C   : 75 arrêts
T1  : 74 arrêts
9   : 74 arrêts
T3b : 66 arrêts
13  : 65 arrêts
12  : 62 arrêts
D   : 59 arrêts
4   : 58 arrêts
```

Les lignes sont classées par nombre décroissant d'arrêts distincts.

### 3. Ligne avec la plus grande amplitude horaire

Résultat obtenu :

```text
Ligne : T4
Premier passage : 00:00:00
Dernier passage : 25:58:00
Amplitude : 25:58:00
```

Les horaires GTFS pouvant dépasser 24 heures, les champs `arrival_time` et `departure_time`, stockés en texte dans la base, sont convertis en `interval` PostgreSQL avant les calculs.

L'amplitude est obtenue avec la différence entre le dernier et le premier passage de chaque ligne.

### 4. Correspondances par station

Cette analyse utilise la relation entre `parent_station` et `stop_id` dans la table `stops`.

Une station peut avoir plusieurs arrêts rattachés au même lieu.

Exemples de résultats :

```text
République : 10 arrêts rattachés
Châtelet : 10 arrêts rattachés
Nation : 9 arrêts rattachés
Gare Saint-Lazare : 8 arrêts rattachés
Gare Montparnasse : 8 arrêts rattachés
Charles de Gaulle - Étoile : 7 arrêts rattachés
```

## Bonnes pratiques SQL

Les requêtes du projet appliquent plusieurs règles de SQL sain.

Les colonnes sont toujours indiquées explicitement et aucun `SELECT *` n'est utilisé.

Lorsqu'une sous-requête d'exclusion est nécessaire, `NOT EXISTS` est privilégié à `NOT IN`, notamment afin d'éviter les problèmes liés aux valeurs `NULL`.

Pour les comparaisons sur des périodes, les bornes `>=` et `<` sont privilégiées à `BETWEEN`.

Les alias et les noms utilisés dans les requêtes suivent la convention `minuscules_avec_underscores`.

Les requêtes utilisent également des jointures explicites avec `INNER JOIN` afin de rendre les relations entre les tables plus lisibles.

## Formatage et contrôle du code

Le projet utilise Ruff pour formater et contrôler le code Python.

Formater le code :

```bash
ruff format src
```

Contrôler le code :

```bash
ruff check src
```

Le projet doit retourner :

```text
All checks passed!
```

avant le rendu.

## Sécurité

Les informations sensibles de connexion ne sont jamais écrites directement dans le code Python.

Le fichier `.env` contient les vraies valeurs de connexion et est ignoré par Git.

Le fichier `.env.example` est versionné mais ne contient aucune valeur sensible.

Le fichier `dump.sql` utilisé pour le test PostgreSQL local est également ignoré par Git afin de ne pas versionner un fichier de données volumineux.

## Note de lecture

Les résultats montrent que le métro possède le plus grand nombre d'arrêts dans les données étudiées avec 803 arrêts, devant le tramway avec 580 arrêts et le RER avec 242 arrêts.

Les lignes 8 et 7 sont celles qui desservent le plus d'arrêts avec 76 arrêts chacune.

La ligne T4 possède la plus grande amplitude horaire observée, avec un premier passage à minuit et un dernier passage à 25 h 58, soit une amplitude totale de 25 h 58.

Concernant les correspondances, République et Châtelet sont les stations ayant le plus grand nombre d'arrêts rattachés dans les données analysées, avec 10 arrêts chacune.

## Bonus Docker

Le projet peut également être exécuté dans des conteneurs Docker.

Le `Dockerfile` construit une image Python contenant les dépendances du projet
et lance le point d'entrée avec :

```bash
python -m src.main
```
Construire l'image Docker :

```bash
docker build -t sl-2026-bp .
```
### Docker Compose

Le fichier `docker-compose.yml` permet de lancer deux services :

- `db` : une base de données PostgreSQL locale ;
- `app` : l'application Python qui exécute les analyses.

La base PostgreSQL locale est initialisée à partir du fichier `dump.sql`. Ce fichier n'est pas versionné dans Git.

Le service app attend que PostgreSQL soit disponible grâce à un
healthcheck avant de démarrer.

Lancer le projet avec Docker Compose :
```bash
docker compose up --build
```
Vérifier l'état des conteneurs :
```bash
docker compose ps
```
Arrêter les conteneurs :
```bash
docker compose down
```
Pour supprimer également le volume PostgreSQL :
```bash
docker compose down -v
```
Lors des tests, l'application conteneurisée retrouve les mêmes résultats que l'exécution Python classique.