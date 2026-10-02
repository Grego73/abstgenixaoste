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
            # Validation propre des codes de succès standards (200, 201, 202)
            if response.status in [200, 201, 202]:
                return True
    except Exception as e:
        st.error(f"Erreur technique lors de l'envoi de l'e-mail : {e}")
    return False
