from pymongo import MongoClient

# --- CONFIGURATION ---
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "immobilier_db"

def get_database():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        print(f"✅ Connecté avec succès à la base : {DB_NAME}")
        return db
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return None

# --- TEST RAPIDE ---
if __name__ == "__main__":
    db = get_database()
    
    if db is not None:
        # Access collections
        annonces = db['annonce']
        prospects = db['prospect']
        visits = db['visits']
        offres = db['offres']
        
        # Test: Count documents
        count = annonces.count_documents({})
        print(f"📊 Nombre d'annonces dans la base : {count}")
        
        # Test: Find one
        one_doc = annonces.find_one()
        if one_doc:
            print(f"🔎 Exemple d'annonce : {one_doc.get('type')} à {one_doc.get('prix')} DH")