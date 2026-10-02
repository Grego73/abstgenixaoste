import streamlit as st
from google.cloud import firestore
import hashlib
import json
import urllib.request

# 1. VARIABLES GLOBALES DE L'AMICALE BOULE SAINT-GENIX AOSTE
NOM_CLUB = "Amicale Boule Saint-Genix Aoste"
STATUT_CLUB = "Association déclarée (fondée en décembre 2004)"
ADRESSE_SIEGE = "Café Gojon, Rue des Juifs, 73240 Saint-Genix-les-Villages"
BOULODROMES = "Jeux de La Glière (Saint-Genix) & Terrains d'Aoste"
URL_FACEBOOK = "https://facebook.com"

DONNEES_CARTE = {
    "latitude": (45.5995592, 45.590435),
    "longitude": (5.6297572, 5.606534),
    "Nom du terrain": ("Jeux de La Glière (Saint-Genix)", "Terrains de boules d'Aoste")
}

URL_BOULE_IMAGE = "https://taboulot.fr"

# 2. INITIALISATION DU CLIENT FIRESTORE SÉCURISÉ (MÉTHODE OFFICIELLE STREAMLIT)
@st.cache_resource
def initialiser_firebase():
    if "firebase" not in st.secrets:
        st.error("❌ Les secrets Firebase sont introuvables dans st.secrets. Vérifiez votre fichier secrets.toml.")
        st.stop()
        
    try:
        # Copie et traitement propre des secrets
        fb_secrets = dict(st.secrets["firebase"])
        if "private_key" in fb_secrets:
            fb_secrets["private_key"] = fb_secrets["private_key"].replace("\\n", "\n").strip()
            
        # Création directe d'un client Firestore sans passer par le package firebase_admin global
        db = firestore.Client.from_service_account_info(fb_secrets)
        return db
        
    except Exception as e:
        st.error(f"❌ Erreur lors de l'initialisation directe de Firestore : {e}")
        st.stop()

# 3. GESTION DES SESSIONS ET DE LA SÉCURITÉ
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verifier_session():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_pseudo" not in st.session_state:
        st.session_state["user_pseudo"] = ""
    if "verifying_email" not in st.session_state:
        st.session_state["verifying_email"] = None

# 4. SERVICE D'E-MAILS BREVO SÉCURISÉ & STABLE

