import streamlit as st
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['immobilier_db']
annonces = db["annonces"]

st.set_page_config(page_title="ImmoCRM-Rechercher", layout="wide")
st.write("# Rechercher une annonce")

st.sidebar.header("Filtrer Par:")

# 1. Filtres
villes_disponible = annonces.distinct("ville")
choix_ville = st.sidebar.selectbox("Ville", ["Toutes"] + villes_disponible)

types_disponible = ["Villa", "Appartement", "Boutique"]
choix_type = st.sidebar.selectbox("Type", ["Tous"] + types_disponible)

max_budget = st.sidebar.slider("Budget Maximum (DH)", 0, 20000000, 5000000, step=10000)

if st.sidebar.button("Chercher"):
    query = {}
    if choix_ville != "Toutes":
        query["ville"] = choix_ville
    
    if choix_type != "Tous":
        query["type_recherche"] = choix_type
    
    # FIX l-Mouchkil dial l-Filtre:
    # Kandiro query 3la 'prix.price' hit f MongoDB d-data dyal Sarouty m-sttefa hakka
    query["prix.price"] = {"$lte": max_budget}
    
    # Ila knti derti l-fallback f seeder (raqm), tqder t-dir OR query:
    # query["$or"] = [{"prix.price": {"$lte": max_budget}}, {"prix": {"$lte": max_budget}}]

    houses = list(annonces.find(query))
    
    if len(houses) > 0:
        for house in houses:
            with st.container(border=True):
                col_img, col_info = st.columns([1, 2])
                
                with col_img:
                    img_url = house.get('img_url')
                    if img_url:
                        st.image(img_url, use_container_width=True)
                    else:
                        st.header("🏠")
                    
                with col_info:
                    st.subheader(house.get('type_recherche', 'Bien Immobilier'))
                    st.write(f"📍 {house.get('ville', '-')}")
                    
                    # FIX l-Mouchkil dial l-Affichge:
                    prix_data = house.get('prix', 0)
                    if isinstance(prix_data, dict):
                        prix_final = prix_data.get('price', 0)
                    else:
                        prix_final = prix_data
                    
                    st.markdown(f"### 💰 {prix_final:,} DH")
                    
                    # Bouton khallih wast col_info bach y-welli clickable mzyan
                    st.button("Voir", key=str(house['_id']))
    else:
        st.warning("🚫 Aucun résultat ! Aucun bien ne correspond à ces critères.")
else:
    st.info("👈 Utilisez les filtres à gauche pour trouver des annonces.")