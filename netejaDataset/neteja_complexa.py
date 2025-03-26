import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns

print("Iniciant el procés de neteja i transformació de dades...")

# 1. Carregar el dataset
df = pd.read_csv("barcelona_listings.csv")
# Reduir la mida del dataset (p.ex. agafant només el 25% de les files)
df = df.sample(frac=0.25, random_state=42)
print(f"Dataset reduït a {df.shape[0]} files (25% de l'original)")
print(f"Dataset carregat amb {df.shape[0]} files i {df.shape[1]} columnes")

# 2. Seleccionar només les columnes que volem mantenir
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

# 3. Neteja i transformacions bàsiques
# 3.1 Crear nova columna amb el nombre d'amenities
print("Calculant el nombre d'amenities...")
df_reduit["amenities_count"] = df["amenities"].apply(lambda x: len(re.findall(r'[^,{]+', str(x))) if pd.notna(x) else 0)

# 3.2 Eliminar la columna antiga
df_reduit = df_reduit.drop(columns=["amenities"])

# 3.3 Neteja de la columna price
print("Netejant la columna price...")
df_reduit["price"] = df_reduit["price"].str.replace("$", "")
df_reduit["price"] = df_reduit["price"].str.replace(",", "")
df_reduit["price"] = df_reduit["price"].str.replace(".00", "")

# 3.4 Eliminar files on price no és numèric
files_abans = df_reduit.shape[0]
df_reduit = df_reduit[pd.to_numeric(df_reduit["price"], errors='coerce').notnull()]
files_eliminades = files_abans - df_reduit.shape[0]
print(f"S'han eliminat {files_eliminades} files on price no era numèric")

# 3.5 Convertir price a tipus numèric
df_reduit["price"] = pd.to_numeric(df_reduit["price"])

# 4. Normalització de barris a districtes
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

# Funció per assignar districte a cada barri
def assignar_districte(barri):
    if pd.isna(barri):
        return 'Desconegut'
    
    # Eliminar espais addicionals i normalitzar el text
    barri_net = barri.strip()
    
    # Buscar al diccionari
    if barri_net in barris_a_districtes:
        return barris_a_districtes[barri_net]
    
    # Solució per a barris problemàtics com La Font d'en Fargues i Can Baró
    # Comprovem si el barri conté paraules clau específiques
    barri_lower = barri_net.lower()
    
    if "font d'en fargues" in barri_lower or "font den fargues" in barri_lower:
        return "Horta-Guinardó"
    
    if "can baró" in barri_lower or "can baro" in barri_lower:
        return "Horta-Guinardó"
    
    # Comprovar si són variacions d'altres barris
    for barri_conegut, districte in barris_a_districtes.items():
        if barri_lower in barri_conegut.lower() or barri_conegut.lower() in barri_lower:
            return districte
    
    # Si el barri no està al diccionari i no s'ha trobat cap coincidència, imprimir per depurar
    print(f"Barri no identificat: '{barri_net}'")
    
    # Retornem el valor original
    return barri_net

# Aplicar la funció i crear mapeig
df_reduit['neighbourhood'] = df_reduit['neighbourhood'].apply(assignar_districte)

# Reordena el codi per fixar els errors

# 5. Imputació de valors mancants a square_feet
print("Imputant valors mancants a square_feet...")

# 5.1. Convertir square_feet a tipus numèric i identificar valors buits o nuls
df_reduit["square_feet"] = pd.to_numeric(df_reduit["square_feet"], errors='coerce')
missing_square_feet = df_reduit["square_feet"].isna() | (df_reduit["square_feet"] == 0)

print(f"Nombre total de registres: {len(df_reduit)}")
print(f"Registres sense square_feet vàlid: {missing_square_feet.sum()} ({missing_square_feet.sum()/len(df_reduit):.2%})")

# 5.2. Guardar una còpia de les dades originals abans d'imputar
df_reduit_original = df_reduit.copy()

# 5.3. Imputació sofisticada basada en tipus de propietat i districte
# Primer agrupem per tipus de propietat i districte i calculem estadístiques
print("Calculant estadístiques per tipus de propietat i districte...")

grouped_stats = df_reduit[~missing_square_feet].groupby(
    ["property_type", "neighbourhood"])["square_feet"].agg(["mean", "std", "count"]).reset_index()

# Mostrar estadístiques
print("\nEstadístiques de square_feet per tipus de propietat i districte:")
print(grouped_stats[grouped_stats["count"] >= 5].head(10))  # Mostrem només grups amb almenys 5 observacions

# Crear un diccionari per a les estadístiques
property_district_stats = {}
for _, row in grouped_stats.iterrows():
    key = (row["property_type"], row["neighbourhood"])
    # Utilitzem un mínim de std per evitar valors 0
    std_value = row["std"] if not pd.isna(row["std"]) and row["std"] > 10 else 10
    property_district_stats[key] = {
        "mean": row["mean"],
        "std": std_value,
        "count": row["count"]
    }

# Estadístiques globals per si de cas no trobem la combinació específica
global_mean = df_reduit[~missing_square_feet]["square_feet"].mean()
global_std = max(df_reduit[~missing_square_feet]["square_feet"].std(), 10)
print(f"\nEstadístiques globals: Mitjana = {global_mean:.2f}, Desv. Estàndard = {global_std:.2f}")

# Estadístiques per tipus de propietat
property_stats = df_reduit[~missing_square_feet].groupby("property_type")["square_feet"].agg(["mean", "std", "count"]).reset_index()
property_stats_dict = {}
for _, row in property_stats.iterrows():
    std_value = row["std"] if not pd.isna(row["std"]) and row["std"] > 10 else 10
    property_stats_dict[row["property_type"]] = {
        "mean": row["mean"],
        "std": std_value,
        "count": row["count"]
    }

# Estadístiques per districte
district_stats = df_reduit[~missing_square_feet].groupby("neighbourhood")["square_feet"].agg(["mean", "std", "count"]).reset_index()
district_stats_dict = {}
for _, row in district_stats.iterrows():
    std_value = row["std"] if not pd.isna(row["std"]) and row["std"] > 10 else 10
    district_stats_dict[row["neighbourhood"]] = {
        "mean": row["mean"],
        "std": std_value,
        "count": row["count"]
    }

# 5.4. Imputar valors de square_feet abans de convertir a metres quadrats
print("Realitzant imputació jeràrquica...")
np.random.seed(42)  # Per reproducibilitat

# Recórrer les files amb valors mancants i imputar
for index, row in df_reduit[missing_square_feet].iterrows():
    key = (row["property_type"], row["neighbourhood"])
    
    # Opció 1: Usar estadístiques específiques de tipus i districte
    if key in property_district_stats and property_district_stats[key]["count"] >= 5:
        stats = property_district_stats[key]
        random_value = np.random.normal(stats["mean"], stats["std"])
    
    # Opció 2: Usar estadístiques del tipus de propietat
    elif row["property_type"] in property_stats_dict and property_stats_dict[row["property_type"]]["count"] >= 5:
        stats = property_stats_dict[row["property_type"]]
        random_value = np.random.normal(stats["mean"], stats["std"])
    
    # Opció 3: Usar estadístiques del districte
    elif row["neighbourhood"] in district_stats_dict and district_stats_dict[row["neighbourhood"]]["count"] >= 5:
        stats = district_stats_dict[row["neighbourhood"]]
        random_value = np.random.normal(stats["mean"], stats["std"])
    
    # Opció 4: Usar estadístiques globals
    else:
        random_value = np.random.normal(global_mean, global_std)
    
    # Assegurar que el valor és raonable (mínim 10 peus quadrats)
    random_value = max(round(random_value), 10)
    
    # Assignar el valor generat
    df_reduit.at[index, "square_feet"] = random_value

# 5.5. Convertir de peus quadrats a metres quadrats
print("\nConvertint de peus quadrats a metres quadrats...")
# Factor de conversió: 1 peu quadrat = 0.092903 metres quadrats
factor_conversio = 0.092903

# Crear nova columna amb els valors en metres quadrats
df_reduit["square_meters"] = (df_reduit["square_feet"] * factor_conversio).round(2)

# Guardar l'indicador d'imputació abans d'eliminar square_feet
df_reduit["square_meters_imputed"] = missing_square_feet

# Eliminar la columna en peus quadrats
df_reduit = df_reduit.drop(columns=["square_feet"])

print(f"Conversió completada. Valors ara en metres quadrats.")

# 6. Verificar i mostrar resultats
print("\nEstadístiques després de la imputació:")
print(f"Mitjana de square_meters: {df_reduit['square_meters'].mean():.2f}")
print(f"Desviació estàndard de square_meters: {df_reduit['square_meters'].std():.2f}")
print(f"Valor mínim de square_meters: {df_reduit['square_meters'].min():.2f}")
print(f"Valor màxim de square_meters: {df_reduit['square_meters'].max():.2f}")

# 7. Verificar no hi ha valors nuls
print("\nVerificant valors nuls després de les transformacions:")
print(df_reduit.isnull().sum())

# 8. Visualitzar la distribució dels valors originals vs imputats
plt.figure(figsize=(12, 8))

sns.histplot(df_reduit[~df_reduit["square_meters_imputed"]]["square_meters"], 
             kde=True, stat="density", color="blue", label="Valors originals")
sns.histplot(df_reduit[df_reduit["square_meters_imputed"]]["square_meters"], 
             kde=True, stat="density", color="red", alpha=0.6, label="Valors imputats")

plt.title("Distribució de Metres Quadrats: Original vs Imputat")
plt.xlabel("Metres Quadrats")
plt.ylabel("Densitat")
plt.legend()
plt.savefig("square_meters_distribution.png")
plt.close()

print("S'ha desat el gràfic de distribució com 'square_meters_distribution.png'")

# 9. Desar els resultats
# Opció 1: Desar amb indicador d'imputació
df_reduit.to_csv("base_dades_netejada_amb_indicador.csv", index=False)

# Opció 2: Desar sense indicador d'imputació
df_reduit_final = df_reduit.drop(columns=["square_meters_imputed"])
df_reduit_final.to_csv("base_dades_netejada.csv", index=False)

print("Base de dades netejada i guardada com 'base_dades_netejada.csv'")
print("Base de dades amb indicador d'imputació guardada com 'base_dades_netejada_amb_indicador.csv'")