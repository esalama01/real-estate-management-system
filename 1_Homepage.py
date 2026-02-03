import streamlit as st
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client['immobilier_db']

st.set_page_config(
    page_title="Immobiler-Ecom App",
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = "visiteur"

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3607/3607444.png", width=100)
    st.write("### Espace Agent")
    
    if not st.session_state.logged_in:
        # Formulaire Login
        username = st.text_input("Identifiant")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            user = db.users.find_one({"username": username, "password": password})
            if user:
                st.session_state.logged_in = True
                st.session_state.role = "agent"
                st.session_state.nom = user['nom']
                st.rerun()
            else:
                st.error("Accès refusé")
    else:
        # Deja connecté
        st.success(f"Bonjour {st.session_state.get('nom', 'Agent')}")
        if st.button("Se déconnecter"):
            st.session_state.logged_in = False
            st.session_state.role = "visiteur"
            st.rerun()
st.title("🏡 Bienvenue chez Immo-Ecom")
st.write("Découvrez nos dernières offres.")

st.write("---")
recent_ads = list(db.annonces.find().sort("_id", -1).limit(20))
if recent_ads:
    cols = st.columns(3)
    
    for index, ad in enumerate(recent_ads):
        with cols[index % 3]: 
            with st.container(border=True):
                st.header("🏠")
                
                st.subheader(ad.get('type_recherche', 'Bien Immobilier'))
                st.write(f"📍 **{ad.get('ville', '-')}**")
                
                prix = ad.get('prix', 0)
                st.markdown(f"### 💰 {prix:,} DH")
                
                st.button("Voir détails", key=f"home_btn_{ad['_id']}")
else:
    st.info("Aucune annonce disponible pour le moment.")

st.sidebar.success("Select a page above.")
