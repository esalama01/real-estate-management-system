from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client['immobilier_db']
users_collection = db["users"]


#------------------------------------------------

def main():
    print("--- 🕵️‍♂️ SUDO ADMIN PANEL - IMMOCRM ---")
    print("1. Créer un nouvel AGENT")
    print("2. Supprimer un AGENT")
    print("3. Lister tous les AGENTS")
    print("4. Quitter")
    
    choix = input("👉 Ton choix (1-4): ")

    if choix == '1':
        creer_agent()
    elif choix == '2':
        supprimer_agent()
    elif choix == '3':
        lister_agents()
    elif choix == '4':
        print("Bye Bye 👋")
        exit()
    else:
        main()

def creer_agent():
    print("\n---Création Nouvel Agent---")
    username = input("Username:\n")
    password = input("Password:\n")
    nom_complet = input("Nom Complet:\n")
    cin = input("Cin:\n")
    if users_collection.find_one({"username": username}):
        print("❌ Cet utilisateur existe déjà.")
    else:
        users_collection.insert_one({
            "username" : username,
            "password" : password,
            "nom" : nom_complet,
            "cin" : cin,
            "role" : "agent"
        })
        print("✅ Agent {username} créé avec succès!")
    
    main()

def supprimer_agent():
    user_to_delete = input("\n Username de l'agent à supprimer: ")
    result = users_collection.delete_one({"username": user_to_delete})
    if result.delete_count > 0:
        print("Agent {user_to_delete}✅ Supprimé!")
    else:
        print("Cet utilisateur n'existe pas")
    
    main()

def lister_agents():
    print("\n--- Liste des Agents ---")
    agents = users_collection.find({})
    for a in agents:
        print(f"👤 {a['username']} ({a.get('nom', 'Inconnu')})")
    
    main()

if __name__ == "__main__":
    main()