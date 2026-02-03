import streamlit as st
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['immobilier_db']
annonces = db["annonces"]


st.set_page_config(page_title = "ImmoCRM-Rechercher", layout = "wide")
st.write("# Rechercher une annonce")


st.sidebar.header("Filtrer Par: ")


#Filtrage parr:

#villes
villes_disponible = annonces.distinct("ville")
choix_ville = st.sidebar.selectbox("Ville", ["Toutes"] + villes_disponible)


#types
types_disponible = ["Villa","Appartement","Boutique"]
choix_type = st.sidebar.selectbox("Type", ["Tous"] + types_disponible)

#Budget
max_budget = st.sidebar.slider("Budget Maximum(DH)", 0, 10000000, 5000000, step = 1000)

if st.sidebar.button("Chercher"):
    query = {}
    if choix_ville != "Toutes":
        query["ville"] = choix_ville
    
    if choix_type != "Tous":
        query["type_recherche"] = choix_type
    
    query["prix"] = {"$lte": max_budget}
    
    houses_mongo = annonces.find(query)
    houses = list(houses_mongo)
    if len(houses) > 0:
        for house in houses:
            with st.container(border=True):
                col_img, col_info = st.columns([1, 2]) # Qssem l-Card l Jouj (Tswira sghira, ktba ktira)
                
                with col_img:
                    st.header("🏠")
                    
                with col_info:
                    st.subheader(house.get('type_recherche', 'Bien Immobilier'))
                    st.write(f"📍 {house['ville']}") # Blasa
                    st.write(f"💰 **{house['prix']} DH**") # Taman
                    
            # Bouton l-taht
            st.button("Voir", key=str(house['_id']))
    else:
        st.warning("🚫 Aucun résultat ! Aucun bien ne correspond à ces critères.")

else:
    st.info("👈 Utilisez les filtres à gauche pour trouver des annonces.")
