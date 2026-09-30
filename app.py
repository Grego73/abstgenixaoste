import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Connexion sécurisée à Firebase (Firestore)
# On utilise st.secrets pour masquer les clés privées sur GitHub
if not firebase_admin._apps:
    fb_credentials = dict(st.secrets["firebase"])
    cred = credentials.Certificate(fb_credentials)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Configuration de la page
st.set_page_config(page_title="Club Boule Lyonnaise", page_icon="🥎", layout="wide")

# Barre latérale pour la navigation
page = st.sidebar.radio("Navigation", ["Accueil", "Infos Pratiques", "Actualités & Concours", "Contact"])

# --- PAGE ACCUEIL ---
if page == "Accueil":
    st.title("🥎 Bienvenue au Club de Boule Lyonnaise")
    st.image("https://unsplash.com", caption="Notre passion, le Sport-Boules")
    st.write("Suivez toute la vie du club, nos entraînements et nos compétitions officielles ici !")

# --- PAGE INFOS PRATIQUES ---
elif page == "Infos Pratiques":
    st.title("📅 Infos Pratiques")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Horaires d'entraînements")
        st.write("- Mardi : 17h00 - 20h00")
        st.write("- Samedi : 09h00 - 12h00")
    with col2:
        st.subheader("Tarifs Licences")
        st.write("- Adultes : 60 € / an")
        st.write("- Jeunes (-18 ans) : Gratuit")

# --- PAGE ACTUALITÉS & CONCOURS (Données issues de Firebase) ---
elif page == "Actualités & Concours":
    st.title("🏆 Actualités & Prochains Concours")
    
    # Lecture des données dans Firebase
    concours_ref = db.collection("concours").order_by("date")
    docs = concours_ref.stream()
    
    events_found = False
    for doc in docs:
        events_found = True
        data = doc.to_dict()
        st.subheader(f"🔹 {data.get('nom')}")
        st.caption(f"Date : {data.get('date')} | Lieu : {data.get('lieu')}")
        st.write(data.get('description'))
        st.divider()
        
    if not events_found:
        st.info("Aucun concours de planifié pour le moment. Revenez bientôt !")

# --- PAGE CONTACT (Envoi de données vers Firebase) ---
elif page == "Contact":
    st.title("✉️ Nous Contacter")
    
    with st.form("contact_form", clear_on_submit=True):
        nom = st.text_input("Votre Nom et Prénom")
        email = st.text_input("Votre Adresse E-mail")
        message = st.text_area("Votre Message")
        submit = st.form_submit_button("Envoyer le message")
        
        if submit:
            if nom and email and message:
                # Envoi direct dans la collection "messages" de Firebase
                db.collection("messages").add({
                    "nom": nom,
                    "email": email,
                    "message": message,
                    "statut": "Non lu"
                })
                st.success("Votre message a bien été envoyé au secrétariat du club !")
            else:
                st.error("Veuillez remplir tous les champs du formulaire.")
