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

# --- PAGE ACCUEIL ---
if page == "Accueil":
    st.title(f"🏆 {NOM_CLUB}")
    st.subheader(STATUT_CLUB)
    st.markdown("---")
    
    col_texte, col_photo = st.columns(2)
    with col_texte:
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
        
    with col_photo:
        st.image(URL_BOULE_IMAGE, caption="La Boule Lyonnaise strieuse", use_container_width=True)

    # --- SECTION PLAN D'ACCÈS INTERACTIF ---
    st.markdown("---")
    st.markdown("### 🗺️ Plan d'accès aux terrains")
    st.write("Retrouvez l'emplacement de nos terrains. Cliquez sur les boutons ci-dessous pour lancer l'itinéraire sur votre GPS :")
    
    # Affichage de la carte interactive
    df_carte = pd.DataFrame(DONNEES_CARTE)
    st.map(df_carte, latitude="latitude", longitude="longitude", size=40)

    # Ajout des boutons de redirection GPS vers Google Maps ou Waze
    st.markdown("#### 🚗 Lancer la navigation vers vos smartphones :")
    
    # Ligne pour Saint-Genix (Jeux de la Glière)
    col_sg1, col_sg2 = st.columns([1, 3])
    with col_sg1:
        st.write("**📍 Jeux de La Glière :**")
    with col_sg2:
        # Liens profonds pour Saint-Genix (Latitude: 45.6012, Longitude: 5.6328)
        st.link_button(
            "🗺️ Ouvrir Google Maps", 
            "https://google.com"
        )
        st.link_button(
            "🚙 Ouvrir Waze", 
            "https://waze.com"
        )

    st.markdown(" ") # Petit espace vertical

    # Ligne pour Aoste (Terrains d'Aoste)
    col_aos1, col_aos2 = st.columns([1, 3])
    with col_aos1:
        st.write("**📍 Terrains d'Aoste :**")
    with col_aos2:
        # Liens profonds pour Aoste (Latitude: 45.5872, Longitude: 5.6083)
        st.link_button(
            "🗺️ Ouvrir Google Maps", 
            "https://google.com"
        )
        st.link_button(
            "🚙 Ouvrir Waze", 
            "https://waze.com"
        )
    
    # Création de la carte à partir des variables globales
    df_carte = pd.DataFrame(DONNEES_CARTE)
    st.map(df_carte, latitude="latitude", longitude="longitude", size=40)
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
