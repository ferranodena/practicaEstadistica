import pandas as pd
import re
from collections import Counter

'''
This script selects the variables we work on, fixes the neighbourhoods and district names,
and computes the professionalism and the premium ammenities count variables.
'''


print("Iniciant el procés de neteja i transformació de dades...")

# 1. Carregar el dataset
df = pd.read_csv(".//barcelona_listings.csv")

# 2. Reduir la mida del dataset (p.ex. agafant només el 25% de les files)
df = df.sample(n= 5000, random_state=42)
print(f"Dataset reduït a {df.shape[0]} files (25% de l'original)")
print(f"Dataset carregat amb {df.shape[0]} files i {df.shape[1]} columnes")

# 3. Seleccionar només les columnes que volem mantenir
columnes_a_mantenir = [
    "host_response_time",
    "host_listings_count",
    "host_has_profile_pic",
    "neighbourhood",
    "property_type",
    "room_type",
    "accommodates",
    "amenities",
    "square_feet",
    "price",
    "minimum_nights",
    "availability_365",
    "number_of_reviews",
    "review_scores_rating"
]

# Crear una còpia reduïda amb les columnes seleccionades
df_reduit = df[columnes_a_mantenir].copy()
print(f"Dataset reduït a {len(columnes_a_mantenir)} columnes")

# 4. Conversió de barris a districtes
print("Normalitzant barris a districtes...")
# Diccionari de correspondència barri-districte
barris_a_districtes = {
    # Districte 1: Ciutat Vella
    'Ciutat Vella': 'Ciutat Vella',
    'el Raval': 'Ciutat Vella',
    'El Raval': 'Ciutat Vella',
    'el Barri Gòtic': 'Ciutat Vella',
    'El Gòtic': 'Ciutat Vella',
    'el Gòtic': 'Ciutat Vella',
    'la Barceloneta': 'Ciutat Vella',
    'La Barceloneta': 'Ciutat Vella',
    'Sant Pere, Santa Caterina i la Ribera': 'Ciutat Vella',
    'Sant Pere/Santa Caterina': 'Ciutat Vella',
    'El Born': 'Ciutat Vella',
    
    # Districte 2: Eixample
    'Eixample': 'Eixample',
    'el Fort Pienc': 'Eixample',
    'la Sagrada Família': 'Eixample',
    'La Sagrada Família': 'Eixample',
    "la Dreta de l'Eixample": 'Eixample',
    "Dreta de l'Eixample": 'Eixample',
    "l'Antiga Esquerra de l'Eixample": 'Eixample',
    "L'Antiga Esquerra de l'Eixample": 'Eixample',
    "la Nova Esquerra de l'Eixample": 'Eixample',
    "La Nova Esquerra de l'Eixample": 'Eixample',
    'Sant Antoni': 'Eixample',
    
    # Districte 3: Sants-Montjuïc
    'Sants-Montjuïc': 'Sants-Montjuïc',
    'el Poble-Sec': 'Sants-Montjuïc',
    'El Poble-sec': 'Sants-Montjuïc',
    'el Poble Sec': 'Sants-Montjuïc',
    'la Marina del Prat Vermell': 'Sants-Montjuïc',
    'la Marina de Port': 'Sants-Montjuïc',
    'la Font de la Guatlla': 'Sants-Montjuïc',
    'Hostafrancs': 'Sants-Montjuïc',
    'la Bordeta': 'Sants-Montjuïc',
    'Sants - Badal': 'Sants-Montjuïc',
    'Sants': 'Sants-Montjuïc',
    
    # Districte 4: Les Corts
    'Les Corts': 'Les Corts',
    'les Corts': 'Les Corts',
    'la Maternitat i Sant Ramon': 'Les Corts',
    'La Maternitat i Sant Ramon': 'Les Corts',
    'Pedralbes': 'Les Corts',
    
    # Districte 5: Sarrià-Sant Gervasi
    'Sarrià-Sant Gervasi': 'Sarrià-Sant Gervasi',
    'Sarrià': 'Sarrià-Sant Gervasi',
    'Vallvidrera, el Tibidabo i les Planes': 'Sarrià-Sant Gervasi',
    'les Tres Torres': 'Sarrià-Sant Gervasi',
    'Les Tres Torres': 'Sarrià-Sant Gervasi',
    'Sant Gervasi - la Bonanova': 'Sarrià-Sant Gervasi',
    'Sant Gervasi - Galvany': 'Sarrià-Sant Gervasi',
    'el Putxet i el Farró': 'Sarrià-Sant Gervasi',
    'El Putget i Farró': 'Sarrià-Sant Gervasi',
    
    # Districte 6: Gràcia
    'Gràcia': 'Gràcia',
    'Vallcarca i els Penitents': 'Gràcia',
    'el Coll': 'Gràcia',
    'El Coll': 'Gràcia',
    'la Salut': 'Gràcia',
    'La Salut': 'Gràcia',
    'la Vila de Gràcia': 'Gràcia',
    'Vila de Gràcia': 'Gràcia',
    "el Camp d'en Grassot i Gràcia Nova": 'Gràcia',
    "Camp d'en Grassot i Gràcia Nova": 'Gràcia',
    
    # Districte 7: Horta-Guinardó
    'Horta-Guinardó': 'Horta-Guinardó',
    'el Baix Guinardó': 'Horta-Guinardó',
    'El Baix Guinardó': 'Horta-Guinardó',
    'Can Baró': 'Horta-Guinardó',
    'el Guinardó': 'Horta-Guinardó',
    'El Guinardó': 'Horta-Guinardó',
    'Guinardó': 'Horta-Guinardó',
    "la Font d'en Fargues": 'Horta-Guinardó',
    "La Font d'en Fargues": 'Horta-Guinardó',
    'Font den Fargues': 'Horta-Guinardó',
    'el Carmel': 'Horta-Guinardó',
    'El Carmel': 'Horta-Guinardó',
    'Carmel': 'Horta-Guinardó',
    'la Teixonera': 'Horta-Guinardó',
    'La Teixonera': 'Horta-Guinardó',
    'Sant Genís dels Agudells': 'Horta-Guinardó',
    'Montbau': 'Horta-Guinardó',
    "la Vall d'Hebron": 'Horta-Guinardó',
    'La Vall d\'Hebron': 'Horta-Guinardó',
    'la Clota': 'Horta-Guinardó',
    'Horta': 'Horta-Guinardó',
    
    # Districte 8: Nou Barris
    'Nou Barris': 'Nou Barris',
    'Vilapicina i la Torre Llobeta': 'Nou Barris',
    'Porta': 'Nou Barris',
    'el Turó de la Peira': 'Nou Barris',
    'El Turó de la Peira': 'Nou Barris',
    'Turó de la Peira - Can Peguera': 'Nou Barris',
    'Can Peguera': 'Nou Barris',
    'la Guineueta': 'Nou Barris',
    'La Guineueta': 'Nou Barris',
    'Canyelles': 'Nou Barris',
    'les Roquetes': 'Nou Barris',
    'Les Roquetes': 'Nou Barris',
    'Verdum': 'Nou Barris',
    'Verdum - Los Roquetes': 'Nou Barris',
    'la Prosperitat': 'Nou Barris',
    'La Prosperitat': 'Nou Barris',
    'la Trinitat Nova': 'Nou Barris',
    'La Trinitat Nova': 'Nou Barris',
    'Trinitat Nova': 'Nou Barris',
    'Torre Baró': 'Nou Barris',
    'Ciutat Meridiana': 'Nou Barris',
    'Vallbona': 'Nou Barris',
    
    # Districte 9: Sant Andreu
    'Sant Andreu': 'Sant Andreu',
    'Sant Andreu de Palomar': 'Sant Andreu',
    'la Trinitat Vella': 'Sant Andreu',
    'La Trinitat Vella': 'Sant Andreu',
    'Baró de Viver': 'Sant Andreu',
    'el Bon Pastor': 'Sant Andreu',
    'El Bon Pastor': 'Sant Andreu',
    'la Sagrera': 'Sant Andreu',
    'La Sagrera': 'Sant Andreu',
    'el Congrés i els Indians': 'Sant Andreu',
    'El Congrés i els Indians': 'Sant Andreu',
    'Navas': 'Sant Andreu',
    
    # Districte 10: Sant Martí
    'Sant Martí': 'Sant Martí',
    "el Camp de l'Arpa del Clot": 'Sant Martí',
    "El Camp de l'Arpa del Clot": 'Sant Martí',
    'el Clot': 'Sant Martí',
    'El Clot': 'Sant Martí',
    'el Parc i la Llacuna del Poblenou': 'Sant Martí',
    'El Parc i la Llacuna del Poblenou': 'Sant Martí',
    'Glòries - El Parc': 'Sant Martí',
    'la Vila Olímpica del Poblenou': 'Sant Martí',
    'La Vila Olímpica del Poblenou': 'Sant Martí',
    'La Vila Olímpica': 'Sant Martí',
    'el Poblenou': 'Sant Martí',
    'El Poblenou': 'Sant Martí',
    'Diagonal Mar i el Front Marítim del Poblenou': 'Sant Martí',
    'Diagonal Mar - La Mar Bella': 'Sant Martí',
    'el Besòs i el Maresme': 'Sant Martí',
    'El Besòs i el Maresme': 'Sant Martí',
    'Provençals del Poblenou': 'Sant Martí',
    'Sant Martí de Provençals': 'Sant Martí',
    'la Verneda i la Pau': 'Sant Martí',
    'La Verneda i La Pau': 'Sant Martí'
}

# Funció millorada per assignar districte a cada barri
def assignar_districte(barri):
    if pd.isna(barri):
        return 'Desconegut'
    
    # Eliminar espais addicionals i normalitzar el text
    barri_net = barri.strip()
    
    # Buscar al diccionari
    if barri_net in barris_a_districtes:
        return barris_a_districtes[barri_net]
    
    # Solució per a barris problemàtics específics (paraules clau)
    barri_lower = barri_net.lower()
    
    if "font d'en fargues" in barri_lower or "font den fargues" in barri_lower:
        return "Horta-Guinardó"
    
    if "can baró" in barri_lower or "can baro" in barri_lower:
        return "Horta-Guinardó"
    
    # Comprovar si són variacions d'altres barris
    for barri_conegut, districte in barris_a_districtes.items():
        if barri_lower in barri_conegut.lower() or barri_conegut.lower() in barri_lower:
            return districte
    
    # Si el barri no està al diccionari, imprimir per depurar
    print(f"Barri no identificat: '{barri_net}'")
    
    # Retornem el valor original
    return barri_net

# Aplicar la funció i crear mapeig
df_reduit['neighbourhood'] = df_reduit['neighbourhood'].apply(assignar_districte)

# 5. Neteja i transformacions bàsiques
# 1. Extraiem totes les llistes d’amenities
amen_lists = df['amenities'] \
    .dropna() \
    .apply(lambda s: [a.strip() for a in s.split(',')])

# 2. Comptem la freqüència de cada amenity
all_amenities = [amen for sub in amen_lists for amen in sub]
freq = Counter(all_amenities)

# 3. Definim el llindar del 10% del nombre total de llistings
threshold = len(df) * 0.10

# 4. Seleccionem les amenities “premium” (freq ≤ 10%)
premium_amenities = {amen for amen, cnt in freq.items() if cnt <= threshold}

# 5. Comptem per llistat quantes premium té
def count_premium(row):
    if pd.isna(row):
        return 0
    items = [a.strip() for a in row.split(',')]
    return sum(1 for a in items if a in premium_amenities)

# 5. Comptem per llistat quantes premium té i creem la nova columna
df['amenities_premium_count'] = df['amenities'].apply(count_premium)


# 5.1 Crear nova columna amb el nombre d'amenities
print("Calculant el nombre d'amenities...")
df_reduit["amenities_count"] = df["amenities"].apply(lambda x: len(re.findall(r'[^,{]+', str(x))) if pd.notna(x) else 0)

# 5.2 Eliminar la columna antiga
df_reduit = df_reduit.drop(columns=["amenities"])

# 5.3 Neteja de la columna price
print("Netejant la columna price...")
df_reduit["price"] = df_reduit["price"].str.replace("$", "")
df_reduit["price"] = df_reduit["price"].str.replace(",", "")
df_reduit["price"] = df_reduit["price"].str.replace(".00", "")

# 5.4 Eliminar files on price no és numèric
files_abans = df_reduit.shape[0]
df_reduit = df_reduit[pd.to_numeric(df_reduit["price"], errors='coerce').notnull()]
files_eliminades = files_abans - df_reduit.shape[0]
print(f"S'han eliminat {files_eliminades} files on price no era numèric")

# 5.5 Convertir price a tipus numèric
df_reduit["price"] = pd.to_numeric(df_reduit["price"])

# 6. Visualitzar distribució dels districtes
print("\nDistribució de les propietats per districte:")
districtes_counts = df_reduit['neighbourhood'].value_counts()
print(districtes_counts)
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

# 7. Desar els resultats
df_reduit['amenities_premium_count'] = df['amenities_premium_count']
df_reduit['professionalism']            = df['professionalism']
df_reduit.to_csv("base_dades_districtes.csv", index=False)
print("Base de dades transformada i guardada com 'base_dades_districtes.csv'")

# Mostrar un resum final
print("\nResum final:")
print(f"Registres inicials: {df.shape[0]}")
print(f"Registres finals: {df_reduit.shape[0]}")
print(f"Columnes seleccionades: {len(columnes_a_mantenir) - 1 + 1}")  # -1 per amenities, +1 per amenities_count
print("Procés completat amb èxit!")