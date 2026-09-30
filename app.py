import streamlit as st

# IMPORTS DE NOS MODULES CENTRALISÉS
from modules.utils import initialiser_firebase, verifier_session, NOM_CLUB, URL_BOULE_IMAGE, HORAIRES_ENTRAINEMENTS, TARIF_ADULTE, ADRESSE_BOULODROME
from modules.auth import afficher_espace_membres

# Lancement des configurations communes
db = initialiser_firebase()
verifier_session()

# Configuration de l'onglet de la page
st.set_page_config(page_title=NOM_CLUB, page_icon="🏆", layout="wide")

# Menu de navigation
page = st.sidebar.radio("Navigation", ["Accueil", "Infos Pratiques", "Actualités & Concours", "Contact", "🔑 Espace Membres"])

# --- PAGE ACCUEIL ---
if page == "Accueil":
    st.title(f"🥎 Bienvenue au {NOM_CLUB}")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Suivez toute la vie de notre club à l'adresse suivante : {ADRESSE_BOULODROME}")
        st.info("Rejoignez-nous sur les jeux pour partager la passion du Sport-Boules !")
    with col2:
        st.image(URL_BOULE_IMAGE, caption=NOM_CLUB, use_container_width=True)

# --- PAGE INFOS PRATIQUES ---
elif page == "Infos Pratiques":
    st.title("📅 Informations Pratiques")
    st.markdown("---")
    st.subheader("⏰ Entraînements")
    for horaire in HORAIRES_ENTRAINEMENTS:
        st.write(f"- {horaire}")
    st.subheader("💳 Adhésion")
    st.write(f"Le prix de la licence adulte est fixé à : **{TARIF_ADULTE}**")

# --- AUTRES PAGES SANS RÉPÉTITION ---
elif page == "Actualités & Concours":
    st.title("🏆 Actualités")

elif page == "Contact":
    st.title("✉️ Contactez-nous")

elif page == "🔑 Espace Membres":
    afficher_espace_membres(db)
