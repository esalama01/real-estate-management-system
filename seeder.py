import random
import http.client
import json
import urllib.parse
from faker import Faker
from pymongo import MongoClient
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & CONNEXION ---
fake = Faker('fr_FR')
client = MongoClient("mongodb://localhost:27017/")
db = client['immobilier_db']

def get_sarouty_data(limit=50):
    print(f"⏳ Récupération de {limit} annonces réelles depuis Sarouty...")
    HOST = "b2c-be-prod.api.sarouty.ma"
    BASE_PATH = "/api/properties"
    
    filters = [{"field": "buy_or_rent", "operator": "eq", "value": 1}]
    filter_str = urllib.parse.quote(json.dumps(filters[0]))
    full_path = f"{BASE_PATH}?limit={limit}&page=1&filters={filter_str}"
    
    conn = http.client.HTTPSConnection(HOST)
    headers = { 'User-Agent': "insomnia/10.3.0" }
    
    try:
        conn.request("GET", full_path, "", headers)
        res = conn.getresponse()
        raw_data = json.loads(res.read().decode("utf-8"))
        
        # FIX dial KeyError: N-qalbou fin kayna l-list dyal l-i3lanat
        data_content = raw_data.get('data', {})
        if isinstance(data_content, list):
            return data_content
        if isinstance(data_content, dict):
            # Qeleb wast 'items' aw 'data' dakhlaniya
            return data_content.get('items', data_content.get('data', []))
        return []
    except Exception as e:
        print(f"⚠️ Erreur Scraping: {e}")
        return []

print("\n--- 🚀 Démarrage du Seeder Complet ---")

# Nettoyage des anciennes données
db.annonces.delete_many({})
db.prospects.delete_many({})
db.visites.delete_many({})

# ==========================================
# 1. GÉNÉRATION DES ANNONCES (REAL DATA)
# ==========================================
real_ads = get_sarouty_data(50)
annonces_ids = []

for i in range(50):
    if i < len(real_ads):
        item = real_ads[i]
        images = item.get('images', [])
        img_url = images[0].get('property_image_url', '') if images else ""
        type_choisi = item.get('property_type_fr', 'Appartement')
        prix = item.get('price', random.randint(500000, 2000000))
        ville = item.get('location_name', 'Maroc')
        quartier = f"Quartier {fake.city_suffix()}"
    else:
        # Fallback fake
        type_choisi = random.choice(["Appartement", "Villa"])
        img_url = "https://via.placeholder.com/400x300?text=Immobilier"
        prix = random.randint(500000, 3000000)
        ville = random.choice(['Casablanca', 'Rabat', 'Tanger'])
        quartier = fake.street_name()

    annonce = {
        "titre": f"{type_choisi} {random.choice(['Spacieux', 'Moderne', 'Luxueux'])} à {ville}",
        "prix": prix,
        "type_recherche": type_choisi, 
        "surface": random.randint(60, 400),
        "statut": random.choice(["Disponible", "Vendue", "Louée"]),
        "quartier": quartier,
        "ville": ville,
        "img_url": img_url,
        "date_d'Ajout": datetime.now() - timedelta(days=random.randint(0, 365))
    }

    res = db.annonces.insert_one(annonce)
    annonces_ids.append({"_id": res.inserted_id, "titre": annonce["titre"]})

print(f"✅ {len(annonces_ids)} Annonces insérées.")

# ==========================================
# 2. GÉNÉRATION DES PROSPECTS 👤
# ==========================================
print("Génération des prospects...")
prospects_ids = []
for _ in range(50):
    nom = fake.last_name()
    prenom = fake.first_name()
    
    prospect = {
        "nom": nom,
        "prenom": prenom,
        "telephone": f"06{random.randint(10000000, 99999999)}",
        "email": f"{prenom.lower()}.{nom.lower()}@gmail.com",
        "budget": random.randint(500000, 5000000),
        "type_recherche": random.choice(["Appartement", "Villa", "Boutique"]),
        "ville": random.choice(['Casablanca', 'Rabat', 'Marrakech', 'Tanger']),
        "date_inscription": datetime.now() - timedelta(days=random.randint(0, 30))
    }
    
    res = db.prospects.insert_one(prospect)
    prospects_ids.append({"_id": res.inserted_id, "nom": f"{nom} {prenom}"})

# ==========================================
# 3. GÉNÉRATION DES VISITES 🤝
# ==========================================
print("Génération des visites...")
if annonces_ids and prospects_ids:
    for _ in range(100):
        rand_ann = random.choice(annonces_ids)
        rand_pros = random.choice(prospects_ids)
        
        visite = {
            "id_prospect": rand_pros["_id"],
            "nom_prospect": rand_pros["nom"],
            "id_annonce": rand_ann["_id"],
            "titre_annonce": rand_ann["titre"],
            "date": str(fake.date_between(start_date='-1y', end_date='today')),
            "commentaire": fake.sentence(nb_words=8),
            "statut": random.choice(["En attente", "Intéressé", "Offre faite", "Pas intéressé"])
        }
        db.visites.insert_one(visite)

# ==========================================
# 4. CRÉATION DE L'ADMIN 👮‍♂️
# ==========================================
if not db.users.find_one({"username": "agent1"}):
    db.users.insert_one({
        "username": "agent1",
        "password": "123",
        "nom": "Agent Immobilier",
        "role": "agent"
    })
    print("✅ Utilisateur 'agent1' créé.")

print("\n🎉 TERMINÉ ! D-data dial Sarouty + Prospects + Visites m-sttfin f MongoDB.")