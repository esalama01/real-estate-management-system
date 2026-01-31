from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta

# 1. Connexion
client = MongoClient("mongodb://localhost:27017/")
db = client['immobilier_db']

# Collections (Singular names kima derti f main dyalek)
col_annonce = db['annonce']
col_prospect = db['prospect']
col_visite = db['visite']
col_offre = db['offre']

# Nettoyage (Kat-mseh qbel ma tbda bach mat-doubléch data)
col_annonce.drop()
col_prospect.drop()
col_visite.drop()
col_offre.drop()

fake = Faker() # Générateur de noms
print("⏳ Génération des données en cours...")

# --- ETAPE 1 : ANNONCES ---
types = ['Appartement', 'Villa', 'Studio', 'Terrain']
quartiers_casa = ['Maarif', 'Gauthier', 'Racine', 'CIL', 'Ain Diab', 'Sidi Maarouf']
ids_annonces = []

for _ in range(30): # 30 Annonces
    t = random.choice(types)
    
    # Logic prix logique
    if t == 'Villa':
        prix = random.randint(3000000, 15000000)
        surface = random.randint(300, 1000)
    elif t == 'Studio':
        prix = random.randint(300000, 800000)
        surface = random.randint(30, 60)
    else:
        prix = random.randint(800000, 3000000)
        surface = random.randint(70, 200)

    doc = {
        "type": t,
        "prix": prix,
        "surface": surface,
        "ville": "Casablanca",
        "quartier": random.choice(quartiers_casa),
        "statut": random.choice(["disponible", "disponible", "vendu"]),
        "equipements": random.sample(["Garage", "Ascenseur", "Piscine", "Jardin"], k=random.randint(0, 3)),
        "date_creation": datetime.now() - timedelta(days=random.randint(0, 90))
    }
    
    # Insert & Save ID
    res = col_annonce.insert_one(doc)
    ids_annonces.append(res.inserted_id)

print(f"✅ {len(ids_annonces)} Annonces générées.")

# --- ETAPE 2 : PROSPECTS ---
ids_prospects = []

for _ in range(15): # 15 Clients
    doc = {
        "nom": fake.name(),
        "telephone": fake.phone_number(),
        "budget": random.randint(500000, 5000000),
        "preferences": {
            "quartier": random.choice(quartiers_casa),
            "type": random.choice(types)
        }
    }
    res = col_prospect.insert_one(doc)
    ids_prospects.append(res.inserted_id)

print(f"✅ {len(ids_prospects)} Prospects générés.")

# --- ETAPE 3 : VISITES (Liaison Prospect <-> Annonce) ---
for _ in range(40): # 40 Visites
    p_id = random.choice(ids_prospects)
    a_id = random.choice(ids_annonces)
    
    doc = {
        "id_prospect": p_id,  # Clé étrangère
        "id_annonce": a_id,   # Clé étrangère
        "date": datetime.now() - timedelta(days=random.randint(0, 30)),
        "retour": random.choice(["Positif", "Négatif", "A revoir", "Trop cher"]),
        "agent": fake.first_name()
    }
    col_visite.insert_one(doc)

print("✅ Visites générées (Liaisons créées).")

# --- ETAPE 4 : OFFRES (Liaison) ---
# Gher li 3jabhom l-hal darou offre
for _ in range(10): 
    p_id = random.choice(ids_prospects)
    a_id = random.choice(ids_annonces)
    
    col_offre.insert_one({
        "id_prospect": p_id,
        "id_annonce": a_id,
        "montant": random.randint(1000000, 3000000),
        "statut": "En attente",
        "date": datetime.now()
    })

print("✅ Offres générées.")
print("🎉 Base de données prête ! Lance 'app.py' maintenant.")