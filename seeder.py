import random
from faker import Faker
from pymongo import MongoClient
from datetime import datetime, timedelta

# Configuration & Connexion
fake = Faker('fr_FR')
client = MongoClient("mongodb://localhost:27017/")
db = client['immobilier_db']

# Suppression des anciennes données (Optionnel - décommenter si besoin)
# db.annonces.delete_many({})
# db.prospects.delete_many({})
# db.visites.delete_many({})
# db.users.delete_many({})

print("--- 🚀 Démarrage de la génération de données ---")

# Listes de données
villes_maroc = ['Casablanca', 'Rabat', 'Marrakech', 'Tanger', 'Agadir', 'Fes', 'Meknes', 'Oujda', 'Kenitra', 'Tetouan']
quartiers = ['Maarif', 'Gueliz', 'Hay Riad', 'Centre Ville', 'Hay Mohammadi', 'Ocean', 'Agdal', 'California']

# ==========================================
# 1. GÉNÉRATION DES ANNONCES 🏠
# ==========================================
print("Génération des annonces...")
types_biens = ["Appartement", "Villa", "Boutique", "Terrain"]
annonces_ids = [] 

for _ in range(50):
    type_choisi = random.choice(types_biens)
    ville = random.choice(villes_maroc)
    quartier = random.choice(quartiers)
    
    # Logique de Prix & Surface
    if type_choisi == "Villa":
        prix = random.randint(2000000, 15000000)
        surface = random.randint(200, 1000)
    elif type_choisi == "Appartement":
        prix = random.randint(300000, 2500000)
        surface = random.randint(50, 200)
    else:
        prix = random.randint(100000, 5000000)
        surface = random.randint(20, 500)

    annonce = {
        "titre": f"{type_choisi} {random.choice(['Spacieux', 'Moderne', 'Luxueux', 'Coquet'])} à {quartier}",
        "prix": prix,
        "type_recherche": type_choisi, 
        "surface": surface,
        "statut": random.choice(["Disponible", "Vendue", "Louée"]),
        "quartier": quartier,
        "ville": ville,
        "date_d'Ajout": datetime.now() - timedelta(days=random.randint(0, 365))
    }

    if type_choisi == "Villa":
        annonce["piscine"] = random.choice([True, False])
    if type_choisi == "Appartement":
        annonce["etage"] = random.randint(1, 10)

    res = db.annonces.insert_one(annonce)
    annonces_ids.append({"_id": res.inserted_id, "titre": annonce["titre"]})

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
        "date_naissance": str(fake.date_of_birth(minimum_age=25, maximum_age=70)),
        "telephone": f"06{random.randint(10000000, 99999999)}",
        "email": f"{prenom.lower()}.{nom.lower()}@gmail.com",
        "budget": random.randint(500000, 5000000),
        "type_recherche": random.choice(types_biens),
        "surface_min": random.randint(50, 200),
        "quartier_prefere": random.choice(quartiers),
        "ville": random.choice(villes_maroc),
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
        rand_annonce = random.choice(annonces_ids)
        rand_prospect = random.choice(prospects_ids)
        
        visite = {
            "id_prospect": rand_prospect["_id"],
            "nom_prospect": rand_prospect["nom"],
            "id_annonce": rand_annonce["_id"],
            "titre_annonce": rand_annonce["titre"],
            "date": str(fake.date_between(start_date='-1y', end_date='today')),
            "commentaire": fake.sentence(nb_words=10),
            "statut": random.choice(["En attente", "Intéressé", "Offre faite", "Pas intéressé"])
        }
        db.visites.insert_one(visite)

# ==========================================
# 4. CRÉATION DE L'ADMIN 👮‍♂️
# ==========================================
if not db.users.find_one({"username": "agent1"}):
    db.users.insert_one({
        "username": "agent1",
        "password": "1234",
        "nom": "Agent Super",
        "role": "agent"
    })
    print("✅ Utilisateur 'agent1' créé (Mot de passe : 1234)")

print("\n🎉 TERMINÉ ! Données générées avec succès.")