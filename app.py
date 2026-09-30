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

st.set_page_config(page_title=NOM_CLUB, page_icon="🏆", layout="centered")

# Barre de navigation
page = st.sidebar.radio("Navigation", ["Accueil", "La Vie du Club & Concours", "Contact", "🔑 Espace Membres"])

# --- PAGE ACCUEIL ---
if page == "Accueil":
    st.title(f"🏆 {NOM_CLUB}")
    st.subheader(STATUT_CLUB)
    st.markdown("---")
    
    # Tout le texte va maintenant respirer sur une largeur naturelle et lisible
    st.markdown(f"### 📍 Notre Implantation")
    st.write(f"**Siège social :** {ADRESSE_SIEGE}")
    st.write(f"**Lieux d'entraînement et compétitions :** {BOULODROMES}")
    
    st.markdown("### 🎯 Notre Mission")
    st.info(
        "Fondée dans un esprit de franche camaraderie, notre amicale s'attache à développer "
        "la pratique et le rayonnement du sport-boules (Boule Lyonnaise) sur les territoires de "
        "Saint-Genix-les-Villages (Savoie) et d'Aoste (Isère)."
    )
    
    st.write(f"🔗 Suivez l'actualité en direct sur notre [Page Facebook Officielle]({URL_FACEBOOK}).")
    
    # --- SECTION PLAN D'ACCÈS INTERACTIF ---
    st.markdown("---")
    st.markdown("### 🗺️ Plan d'accès aux terrains")
    st.write("Cliquez pour lancer votre application ou copiez les coordonnées pour votre GPS :")
    
    # La carte prendra automatiquement 100% de la largeur du texte, avec une hauteur équilibrée
    st.map(pd.DataFrame(DONNEES_CARTE), latitude="latitude", longitude="longitude", size=40, height=350)

    st.markdown(" ") # Petit espace vertical
    st.markdown("#### 🚗 Configuration du GPS :")
    
    # --- ZONE SAINT-GENIX (Jeux de la Glière) ---
    st.markdown("##### 📍 Jeux de La Glière (Saint-Genix)")
    col_sg1, col_sg2, col_sg3 = st.columns([1, 1, 1.5])
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
        st.text_input("Coordonnées GPS", value="45.6012, 5.6328", key="gps_sg", label_visibility="collapsed")

    st.markdown(" ") # Petit espace vertical

    # --- ZONE AOSTE (Terrains d'Aoste) ---
    st.markdown("##### 📍 Terrains d'Aoste")
    col_aos1, col_aos2, col_aos3 = st.columns([1, 1, 1.5])
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
        st.text_input("Coordonnées GPS", value="45.5872, 5.6083", key="gps_aos", label_visibility="collapsed")
# --- PAGE ACTUALITÉS ---
elif page == "La Vie du Club & Concours":
    st.title("🏆 Résultats & Compétitions")
    st.markdown("---")
    
    # Section Faits Marquants (Issus des données Facebook récupérées)
    st.subheader("✨ Les grands moments du club")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("📈 **Performance Historique !**")
        st.write("Le club a enregistré une performance inédite en qualifiant simultanément **6 équipes aux Championnats de France**.")
    with col2:
        st.success("🥇 **Championnat Individuel**")
        st.write("**Régine Robin** s'est illustrée avec brio en décrochant le titre de **Championne de Savoie en simple F4**.")
        
    st.markdown("---")
    st.subheader("📅 Prochains Concours Officiels")
    
    # Lecture dynamique de Firebase Firestore
    try:
        concours_ref = db.collection("concours")
        docs = concours_ref.stream()
        events_found = False
        for doc in docs:
            events_found = True
            data = doc.to_dict()
            st.markdown(f"🔹 **{data.get('nom')}**")
            st.caption(f"Lieu : {data.get('lieu')} | Date : {data.get('date')}")
            st.write(data.get('description'))
            st.divider()
        if not events_found:
            st.info("Aucun événement encodé dans la base de données. Utilisez l'espace membre pour ajouter un concours.")
    except Exception as e:
        st.caption("Base de données en attente d'éléments.")

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
