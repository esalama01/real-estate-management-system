import streamlit as st
import json
from pymongo import MongoClient
import datetime

# --- SECURITE AGENT ---
if not st.session_state.get('logged_in', False):
    st.error("⛔ Zone Réservée aux Agents !")
    st.write("Veuillez vous connecter sur la page d'accueil.")
    st.stop() 
# ----------------------

# 1. Connexion
client = MongoClient("mongodb://localhost:27017/")
db = client['immobilier_db']
annonce = db["annonces"]


villes_maroc = ['agadir', 'al_hoceima', 'asilah', 'azemmour', 'azilal', 'azrou', 'beni_mellal', 'benslimane', 'berkane', 'berrechid', 'boujdour', 'bouznika', 'casablanca', 'chefchaouen', 'dakhla', 'el_hajeb', 'el_jadida', 'el_kelaa_des_sraghna', 'errachidia', 'essaouira', 'es_semara', 'fes', 'fnideq', 'fqih_ben_salah', 'guelmim', 'guercif', 'ifrane', 'inezgane', 'jerada', 'kenitra', 'khemisset', 'khenifra', 'khouribga', 'ksar_el_kebir', 'laayoune', 'larache', 'marrakech', 'martil', 'mdiq', 'meknes', 'midelt', 'mohammedia', 'nador', 'ouarzazate', 'ouazzane', 'oujda', 'rabat', 'safi', 'sale', 'sefrou', 'settat', 'sidi_bennour', 'sidi_ifni', 'sidi_kacem', 'sidi_slimane', 'skhirat', 'souk_el_arbaa', 'tanger', 'tan_tan', 'taounate', 'taroudant', 'tata', 'taza', 'temara', 'tetouan', 'tinghir', 'tiznit', 'youssoufia', 'zagora']
villes = []
for ville in villes_maroc:
    villes.append(ville.capitalize())
st.set_page_config(page_title="ImmoCRM-Annonces", layout="wide")
st.title("🏘️ Agence Immobilière - Annonces Form")

type = st.selectbox("Type",["Villa","Appartement", "Boutique"])

with st.form(key = 'user_form'):
    #id_annonce = st.number_input("id") i ll let mongodb generate it
    
    titre = st.text_input("Titre")
    piscine = False
    etage = 0
    if type == "Villa":
        st.write("Options Villa:")
        piscine = st.checkbox("Avec Piscine?")
    if type == "Appartement":
        st.write("Options Appartement:")
        etage = st.number_input("Étage", min_value=0)
    surface = st.number_input("Surface", min_value = 0)
    quartier = st.text_input("Quartier")
    ville = st.selectbox("Ville", villes)
    description = st.text_area("Description")
    statut = st.selectbox("Statut", ["Disponible","Vendue","Louée"])
    prix = st.number_input("Prix", min_value = 0)
    submit_button = st.form_submit_button(label='Submit')
if submit_button:
    #print("hola")
    nouvel_annonce = {
        "titre": titre,
        "prix": prix,
        "type_recherche": type, 
        "surface": surface,
        "statut" : statut,
        "quartier": quartier,
        "ville": ville,
        "date_d'Ajout": datetime.datetime.now()
    }
    if type == "Villa":
        nouvel_annonce["piscine"] = piscine
    elif type == "Appartement":
        nouvel_annonce["etage"] = etage
    
    try:
        result = annonce.insert_one(nouvel_annonce)
        st.success(f"✅ Annonce {result.inserted_id}ajouté avec succès !")
        st.balloons()
    except Exception as e:
        st.error(f"❌ Erreur: {e}")