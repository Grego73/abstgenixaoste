import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib

# 1. VARIABLES UTILES POUR TOUT LE SITE
NOM_CLUB = "Union Sportive Boule Lyonnaise"
ADRESSE_BOULODROME = "123 Rue du Boulodrome, 73240 Saint-Genix-les-Villages"
TARIF_ADULTE = "60 € / an"
HORAIRES_ENTRAINEMENTS = [
    "Mardi : 17h00 - 20h00",
    "Samedi : 09h00 - 12h00"
]
URL_BOULE_IMAGE = "https://taboulot.fr"

# 2. INITIALISATION UNIQUE DE FIREBASE
def initialiser_firebase():
    """Initialise la connexion Firebase et retourne l'instance Firestore."""
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

# 3. FONCTIONS REUTILISABLES PARTAGEES
def hash_password(password):
    """Sécurise un mot de passe avec l'algorithme SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verifier_session():
    """S'assure que les variables d'état Streamlit existent au démarrage."""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_pseudo" not in st.session_state:
        st.session_state["user_pseudo"] = ""
    if "verifying_email" not in st.session_state:
        st.session_state["verifying_email"] = None
