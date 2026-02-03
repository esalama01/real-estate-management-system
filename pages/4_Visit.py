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
visite = db["visites"]

#------------------
st.set_page_config(page_title = "ImmoCRM-Visites", layout = "wide")
st.write("# Ajouter une visite")

prospects_list = db["prospects"].find({}, {"nom": 1, "prenom": 1, "_id": 1})

dict_prospect = {}

for prospect in prospects_list:
    nom_complet = f"{prospect['nom']} {prospect['prenom']}"
    dict_prospect[nom_complet] = prospect['_id']

prospect_nom = list(dict_prospect.keys())

nom_choisi = st.selectbox("Nom de visiteur", prospect_nom)
if nom_choisi is not None:
    prospect_id_choisi = dict_prospect[nom_choisi]
else:
    st.warning("Veuillez choisir un prospect")

#-----------------
annonces_list = db["annonces"].find({}, {"titre": 1, "_id": 1})

dict_annonces = {}

for annonce in annonces_list:
    dict_annonces[annonce['titre']] = annonce['_id']

annonces_titres = list(dict_annonces.keys())

annonce_choisi = st.selectbox("Titre d'annonce", annonces_titres)
if annonce_choisi is not None:
    annonce_id_choisi = dict_annonces[annonce_choisi]
else:
    st.warning("Veuillez choisir une annonce")

with st.form(key = 'visits_form'):
    date_visite = st.date_input("Date de visite", datetime.date.today())
    commentaire = st.text_area("Rapport de visite", placeholder="Ex: Client intéressé mais trouve le prix un peu élevé.")
    resultat = st.selectbox("Résultat", ["En attente", "Intéressé", "Offre faite", "Pas intéressé"])
    
    submit = st.form_submit_button("Enregistrer la visite")

if submit:
    nouvelle_visite = {
        "id_prospect": prospect_id_choisi,
        "nom_prospect": nom_choisi,
        "id_annonce": annonce_id_choisi,
        "titre_annonce": annonce_choisi,
        "date": str(date_visite),
        "commentaire": commentaire,
        "statut": resultat
    }
    
    try:
        db.visites.insert_one(nouvelle_visite)
        st.success("✅ Visite enregistrée avec succès !")
        st.balloons()
    except Exception as e:
        st.error(f"❌ Erreur: {e}")
