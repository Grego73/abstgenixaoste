python
# Dans modules/utils.py
import streamlit as st
import firebase_admin
from google.oauth2 import service_account
from google.cloud import firestore as gc_firestore  # 👈 Nouvel import officiel
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

# 2. INITIALISATION DU CLIENT FIRESTORE EN MODE REST
@st.cache_resource
def initialiser_firebase():
    if "firebase" not in st.secrets:
        st.error("❌ Les secrets Firebase sont introuvables dans st.secrets. Vérifiez votre fichier secrets.toml.")
        st.stop()
        
    try:
        fb_secrets = dict(st.secrets["firebase"])
        if "private_key" in fb_secrets:
            fb_secrets["private_key"] = fb_secrets["private_key"].replace("\\n", "\n")
        
        # 🔑 Génération des accès Google Auth standard
        creds = service_account.Credentials.from_service_account_info(fb_secrets)
        
        # 🎯 LE COMPOSANT MAGIQUE : transport="rest" 
        # Force le SDK à utiliser de simples requêtes HTTPS au lieu du tunnel gRPC bloqué.
        db = gc_firestore.Client(credentials=creds, project=fb_secrets["project_id"], transport="rest")
        return db
        
    except Exception as e:
        st.error(f"❌ Erreur lors de l'initialisation de Firestore en mode REST : {e}")
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

# 4. SERVICE D'E-MAILS BREVO
def envoyer_email_brevo(destinataire_email, sujet, message_html):
    try:
        api_key = st.secrets["brevo"]["api_key"]
        sender_email = st.secrets["brevo"]["sender_email"]
        
        url = "https://brevo.com"
        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }
        
        payload = {
            "sender": {"name": "Amicale Boule St-Genix Aoste", "email": sender_email},
            "to": [{"email": destinataire_email}],
            "subject": sujet,
            "htmlContent": message_html
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req) as response:
            if response.status in [200, 201, 202]:
                return True
    except Exception as e:
        st.error(f"Erreur technique lors de l'envoi de l'e-mail : {e}")
    return False
