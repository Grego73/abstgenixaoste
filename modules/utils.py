import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib

# 1. VARIABLES GLOBALES DE L'AMICALE BOULE SAINT-GENIX AOSTE
NOM_CLUB = "Amicale Boule Saint-Genix Aoste"
STATUT_CLUB = "Association déclarée (fondée en décembre 2004)"
ADRESSE_SIEGE = "Café Gojon, Rue des Juifs, 73240 Saint-Genix-les-Villages"
BOULODROMES = "Jeux de La Glière (Saint-Genix) & Terrains d'Aoste"
URL_FACEBOOK = "https://www.facebook.com/p/Amicale-Boule-St-Genix-Aoste-61570273360707/"
# Coordonnées géographiques pour la carte d'accès (Saint-Genix et Aoste)
DONNEES_CARTE = {
    "latitude": [45.6012, 45.5872],
    "longitude": [5.6328, 5.6083],
    "Nom du terrain": ["Jeux de La Glière (Saint-Genix)", "Terrains de boules d'Aoste"]
}

# URL de la boule lyonnaise strieuse demandée
URL_BOULE_IMAGE = "https://taboulot.fr"

# 2. INITIALISATION UNIQUE DE FIREBASE
def initialiser_firebase():
    if not firebase_admin._apps:
        try:
            fb_secrets = dict(st.secrets["firebase"])
            if "private_key" in fb_secrets:
                fb_secrets["private_key"] = fb_secrets["private_key"].replace("\\n", "\n")
            cred = credentials.Certificate(fb_secrets)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Erreur de configuration Firebase : {e}")
            st.stop()
    return firestore.client()

# 3. FONCTIONS REUTILISABLES
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verifier_session():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_pseudo" not in st.session_state:
        st.session_state["user_pseudo"] = ""
    if "verifying_email" not in st.session_state:
        st.session_state["verifying_email"] = None
