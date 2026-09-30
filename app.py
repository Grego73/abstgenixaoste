import streamlit as st
import pandas as pd
# Imports depuis le fichier de configuration centralisé
from modules.utils import (
    initialiser_firebase, verifier_session, NOM_CLUB, STATUT_CLUB,
    ADRESSE_SIEGE, BOULODROMES, URL_FACEBOOK, URL_BOULE_IMAGE, DONNEES_CARTE
)
from modules.auth import afficher_espace_membres

# Lancement des configurations et de la base de données
db = initialiser_firebase()
verifier_session()

st.set_page_config(page_title=NOM_CLUB, page_icon="🏆", layout="wide")

# Barre de navigation
page = st.sidebar.radio("Navigation", ["Accueil", "La Vie du Club & Concours", "Contact", "🔑 Espace Membres"])

    # --- SECTION PLAN D'ACCÈS INTERACTIF ---
    st.markdown("---")
    st.markdown("### 🗺️ Plan d'accès aux terrains")
    st.write("Retrouvez l'emplacement de nos terrains. Cliquez pour lancer votre application ou copiez les coordonnées pour un autre GPS :")
    
    # Affichage de la carte interactive
    df_carte = pd.DataFrame(DONNEES_CARTE)
    st.map(df_carte, latitude="latitude", longitude="longitude", size=40)

    st.markdown("#### 🚗 Lancer la navigation ou copier les coordonnées :")
    
    # --- ZONE SAINT-GENIX (Jeux de la Glière) ---
    st.markdown("##### 📍 Jeux de La Glière (Saint-Genix)")
    col_sg1, col_sg2, col_sg3 = st.columns([1, 1, 1])
    with col_sg1:
        st.link_button(
            "🗺️ Google Maps", 
            "https://google.com",
            use_container_width=True
        )
    with col_sg2:
        st.link_button(
            "🚙 Waze", 
            "https://waze.com",
            use_container_width=True
        )
    with col_sg3:
        # Permet de copier facilement les coordonnées brutes pour n'importe quel autre outil
        st.text_input("Autre GPS (Coordonnées à copier)", value="45.6012, 5.6328", key="gps_sg", label_visibility="collapsed")

    st.markdown(" ") # Petit espace vertical

    # --- ZONE AOSTE (Terrains d'Aoste) ---
    st.markdown("##### 📍 Terrains d'Aoste")
    col_aos1, col_aos2, col_aos3 = st.columns([1, 1, 1])
    with col_aos1:
        st.link_button(
            "🗺️ Google Maps", 
            "https://google.com",
            use_container_width=True
        )
    with col_aos2:
        st.link_button(
            "🚙 Waze", 
            "https://waze.com",
            use_container_width=True
        )
    with col_aos3:
        st.text_input("Autre GPS (Coordonnées à copier)", value="45.5872, 5.6083", key="gps_aos", label_visibility="collapsed")


# --- PAGE CONTACT ---
elif page == "Contact":
    st.title("✉️ Contacter le Secrétariat")
    st.markdown("---")
    with st.form("contact_form", clear_on_submit=True):
        nom = st.text_input("Votre Nom / Prénom")
        email = st.text_input("Votre Adresse E-mail")
        message = st.text_area("Votre Message")
        if st.form_submit_button("Envoyer au bureau"):
            if nom and email and message:
                db.collection("messages").add({"nom": nom, "email": email, "message": message, "statut": "Non lu"})
                st.success("Votre message a bien été transmis aux bénévoles du club !")
            else:
                st.error("Veuillez remplir l'intégralité du formulaire.")

# --- PAGE AUTHENTIFICATION ---
elif page == "🔑 Espace Membres":
    afficher_espace_membres(db)
