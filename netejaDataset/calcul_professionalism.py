import pandas as pd
import numpy as np

# Carregar les dades
df = pd.read_csv('base_dades_districtes.csv')

# Funció per assignar valor a availability_365 segons els rangs especificats
def availability_score(days):
    if pd.isna(days) or days < 0:
        return 0.0
    elif days <= 50:
        return 0.2
    elif days <= 100:
        return 0.4
    elif days <= 200:
        return 0.6
    elif days <= 300:
        return 0.8
    else:
        return 1.0

# Funció per assignar valor a host_listings_count segons els rangs especificats
def listings_score(count):
    if pd.isna(count) or count < 1:
        return 0.0
    elif count == 1:
        return 0.2
    elif count <= 5:
        return 0.4
    elif count <= 10:
        return 0.6
    elif count <= 50:
        return 0.8
    else:
        return 1.0

# Diccionari per assignar valors a host_response_time
response_time_values = {
    'within an hour': 1.0,
    'within a few hours': 0.75,
    'within a day': 0.5,
    'a few days or more': 0.25
}

# Aplicar les funcions per crear les variables de puntuació
df['availability_score'] = df['availability_365'].apply(availability_score)
df['listings_score'] = df['host_listings_count'].apply(listings_score)
df['response_time_score'] = df['host_response_time'].map(response_time_values).fillna(0.0)

# Calcular professionalism com una mitjana ponderada
df['professionalism'] = (
    0.5 * df['availability_score'] +
    0.25 * df['listings_score'] +
    0.25 * df['response_time_score']
)

# Guardar els resultats en un nou arxiu
df.to_csv('base_dades_districtes_amb_professionalism.csv', index=False)