import streamlit as st
from pymongo import MongoClient
import datetime

# 1. Connexion
client = MongoClient("mongodb://localhost:27017/")
db = client['immobilier_db']
prospect = db["prospects"]

st.set_page_config(page_title = "ImmoCRM-Prospects", layout = "wide")
st.title("🏘️ Agence Immobilière - Prospect Form")

villes_maroc = ['agadir', 'al_hoceima', 'asilah', 'azemmour', 'azilal', 'azrou', 'beni_mellal', 'benslimane', 'berkane', 'berrechid', 'boujdour', 'bouznika', 'casablanca', 'chefchaouen', 'dakhla', 'el_hajeb', 'el_jadida', 'el_kelaa_des_sraghna', 'errachidia', 'essaouira', 'es_semara', 'fes', 'fnideq', 'fqih_ben_salah', 'guelmim', 'guercif', 'ifrane', 'inezgane', 'jerada', 'kenitra', 'khemisset', 'khenifra', 'khouribga', 'ksar_el_kebir', 'laayoune', 'larache', 'marrakech', 'martil', 'mdiq', 'meknes', 'midelt', 'mohammedia', 'nador', 'ouarzazate', 'ouazzane', 'oujda', 'rabat', 'safi', 'sale', 'sefrou', 'settat', 'sidi_bennour', 'sidi_ifni', 'sidi_kacem', 'sidi_slimane', 'skhirat', 'souk_el_arbaa', 'tanger', 'tan_tan', 'taounate', 'taroudant', 'tata', 'taza', 'temara', 'tetouan', 'tinghir', 'tiznit', 'youssoufia', 'zagora']
villes = []
for ville in villes_maroc:
    villes.append(ville.capitalize())

type = st.selectbox("Type",["Villa","Appartement", "Boutique"])
with st.form(key = 'prospect_form'):
    nom = st.text_input("Nom: ")
    prenom = st.text_input("Prénom: ")
    birthday = st.date_input("Date de naissance", 
                            value = None, 
                            min_value = datetime.date(1900,1,1),
                            max_value = datetime.date.today(),
                            format = "DD/MM/YYYY")
    num = st.text_input("Num de tel ",placeholder = "xxxxxx")
    email = st.text_input("Email")
    budget = st.number_input("Budget", min_value = 1)
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
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    #print("Okay")
    nouvel_prospect = {
        "nom": nom,
        "prenom": prenom,
        "date_naissance": str(birthday),
        "telephone": num,
        "email": email,
        "budget": budget,
        "type_recherche": type, 
        "surface_min": surface,
        "quartier_prefere": quartier,
        "ville": ville,
        "date_inscription": datetime.datetime.now()
    }

    if type == "Villa":
        nouvel_prospect["piscine"] = piscine
    elif type == "Appartement":
        nouvel_prospect["etage"] = etage

    try:
        prospect.insert_one(nouvel_prospect)
        st.success(f"✅ Prospect {nom} {prenom} ajouté avec succès !")
        st.balloons()
    except Exception as e:
        st.error(f"❌ Erreur: {e}")