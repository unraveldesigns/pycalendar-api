# Calendar API Client

A python 3.12+ client for the calendar-api API of Moroccan holidays and business days

## Installation

```bash
pip install py-calendar-api --index-url https://gitlab.com/api/v4/projects/71396283/packages/pypi/simple
```

# Français/French

## Configuration via fichier de configuration py-calendar-api.toml

Créer un fichier de configuration `py-calendar-api.toml` et renseigner les variables suivantes:

```toml
CALENDAR_APIKEY = "VOTRE-APIKEY"
```

## Instanciation du client

```python
from pycalendar_api import CalendarApi, ApiConfig

# Depuis fichier de configuration
api = CalendarApi.from_config_file('chemin-du-fichier.toml')

# Depuis les variables d'environnement
api = CalendarApi.from_env()

# Via constructeur (2-steps)
api_conf = ApiConfig(user_email, user_password)
api = CalendarApi(api_conf)
```

## Usage

L'ensemble des domaines exposés par Atlas Market sont accessibles au niveau de CalendarApi où chaque domaine
représente un aspect central du marché financier.

Chaque domaine expose des les méthodes génériques selon sa nature.

- Référentiel
    - **one**: Retourne une entité du domaine identifiée par `key`
    - **many**: Retourne plusieurs entités du domaine identifiées par `list[key]`
    - **mapping**: Retourne un dict entre 2 champs du domaine. ex: (code_isin, description)
    - **filter**: Effectue une recherche multi-citères par clés/valeurs. Voir la doc API pour les paramètres de chaque domaine

- Historique
    - **historique**: Retourne l'historique d'un domaine
    - **historique_dates**: Retourne la liste des dates disponibles dans l'historique

- Performance
    - performance: Retourne la performance d'un instrument financier selon deux types de formats
        - **Spot**: Performance absolue entre 2 dates
        - **Série**: Série des performances quotidiennes couvrant la période entre 2 dates

### Exemple avec les Indices

L'exemple ci-dessous reste valable aux autres domaines. OPCVM, Actions, Obligation, Devise

```python
from pycalendar_api import CalendarApi, ApiConfig, to_date

api = CalendarApi.from_config_file('chemin-du-fichier.toml')
```

#### Référentiel

```python
# ---- Référentiel d'un indice
masi = api.indice.one('MASI')

# ---- Référentiel de plusieurs indices
indices = api.indice.many(['MASI', 'MBI', 'MASI.RB'])

```

#### Historique

```python
# ---- Historique entre 2 dates
histo_masi = api.indice.historique('MASI', date_reference=to_date('30/12/2024'), date_marche=to_date('30/06/2025'))

# ---- Historique sur une période (voir la doc de l'API pour les périodes)
histo_masi = api.indice.historique('MASI', date_marche=to_date('30/06/2025'), periode='YTD')
```
#### Performance

```python
# ---- Performance spot entre 2 dates
perf_masi = api.indice.performance('MASI', date_reference=to_date('30/12/2024'), date_marche=to_date('30/06/2025'))
# ---- Performance spot sur une période
perf_masi = api.indice.performance('MASI', date_marche=to_date('30/06/2025'), periode='YTD')

# ---- Performance série entre 2 dates
perf_masi = api.indice.performance(
    'MASI', date_reference=to_date('30/12/2024'), date_marche=to_date('30/06/2025'),type_performance=TypePerformance.SERIE)
# ---- Performance série sur une période
perf_masi = api.indice.performance(
    'MASI', date_marche=to_date('30/06/2025'), periode='YTD',type_performance=TypePerformance.SERIE)
```
