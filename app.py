import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# IMPORT DE NOTRE MODULE MAISON
from modules.auth import afficher_espace_membres

# Initialisation sécurisée de Firebase
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

db = firestore.client()

# Initialisation des variables de session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_pseudo" not in st.session_state:
    st.session_state["user_pseudo"] = ""
if "verifying_email" not in st.session_state:
    st.session_state["verifying_email"] = None

# Configuration de la page
st.set_page_config(page_title="Club Boule Lyonnaise", page_icon="🏆", layout="wide")

# Menu de navigation
page = st.sidebar.radio("Navigation", ["Accueil", "Infos Pratiques", "Actualités & Concours", "Contact", "🔑 Espace Membres"])

# --- PAGE ACCUEIL ---
if page == "Accueil":
    st.title("Bienvenue au Club de Boule Lyonnaise")
    st.markdown("---")
    col_texte, col_photo = st.columns(2)
    with col_texte:
        st.write("Suivez toute la vie de notre club, nos entraînements et nos compétitions officielles ici !")
        st.info("Bienvenue sur le site officiel de notre club de Sport-Boules ! Passionnés ou simples amateurs, notre club vous accueille dans une ambiance conviviale.")
    with col_photo:
        st.image("https://taboulot.fr", caption="La Boule Lyonnaise", use_container_width=True)

# --- PAGE INFOS PRATIQUES ---
elif page == "Infos Pratiques":
    st.title("📅 Infos Pratiques")
    st.write("**Horaires :** Mardi 17h-20h / Samedi 9h-12h")

# --- PAGE ACTUALITÉS ---
elif page == "Actualités & Concours":
    st.title("🏆 Actualités & Prochains Concours")

# --- PAGE CONTACT ---
elif page == "Contact":
    st.title("✉️ Nous Contacter")

# --- PAGE AUTHENTIFICATION (APPEL DU MODULE SÉPARÉ) ---
elif page == "🔑 Espace Membres":
    # On passe la connexion 'db' en paramètre pour que le module puisse parler à Firebase
    afficher_espace_membres(db)
