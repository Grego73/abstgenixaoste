import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
import json
import urllib.request

# 1. VARIABLES GLOBALES DE L'AMICALE BOULE SAINT-GENIX AOSTE
NOM_CLUB = "Amicale Boule Saint-Genix Aoste"
STATUT_CLUB = "Association déclarée (fondée en décembre 2004)"
ADRESSE_SIEGE = "Café Gojon, Rue des Juifs, 73240 Saint-Genix-les-Villages"
BOULODROMES = "Jeux de La Glière (Saint-Genix) & Terrains d'Aoste"
URL_FACEBOOK = "https://facebook.com"

# Coordonnées géographiques pour la carte d'accès (Saint-Genix et Aoste)
DONNEES_CARTE = {
    "latitude": (45.5995592, 45.590435),
    "longitude": (5.6297572, 5.606534),
    "Nom du terrain": ("Jeux de La Glière (Saint-Genix)", "Terrains de boules d'Aoste")
}

# URL de la boule lyonnaise strieuse demandée
URL_BOULE_IMAGE = "https://taboulot.fr"

# 2. INITIALISATION UNIQUE DE FIREBASE
def initialiser_firebase():
    try:
        # Tente de récupérer l'application par défaut si elle existe déjà
        firebase_admin.get_app()
    except ValueError:
        # Si get_app() lève une ValueError, cela signifie qu'elle n'existe pas encore. On l'initialise.
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

# 4. SERVICE DE NOTIFICATION ET D'ENVOI D'E-MAILS (BREVO API v3) https://api.brevo.com/v3/smtp/email
def envoyer_email_brevo(destinataire_email, sujet, message_html):
    """Envoie un e-mail via l'API REST v3 de Brevo de façon sécurisée."""
    try:
        # Récupération des secrets configurés dans Streamlit
        api_key = st.secrets["brevo"]["api_key"]
        sender_email = st.secrets["brevo"]["sender_email"]
        
        url = "https://api.brevo.com/v3/smtp/email"
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
            # Code HTTP de succès pour Brevo (201 Created)
            if response.status in [200, 201, 202]:
                return True
    except Exception as e:
        st.error(f"Erreur technique lors de l'envoi de l'e-mail : {e}")
    return False
