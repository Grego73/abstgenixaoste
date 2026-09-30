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
    # On donne des proportions : 1.5 de vide à gauche, 5 pour le texte au centre, 1.5 de vide à droite
    col_marge_gauche, col_contenu, col_marge_droite = st.columns([1.5, 5, 1.5])
    
    with col_contenu:
        # Un titre propre sur une seule ligne ou bien proportionné
        st.title(f"🏆 {NOM_CLUB}")
        st.write(f"*{STATUT_CLUB}*")
        st.markdown("---")
        
        # On regroupe les informations dans un conteneur pour un rendu plus net
        with st.container(border=True):
            st.markdown(f"### 📍 Notre Implantation")
            st.write(f"**Siège social :** {ADRESSE_SIEGE}")
            st.write(f"**Lieux d'entraînement et compétitions :** {BOULODROMES}")
            
            st.markdown("### 🎯 Notre Mission")
            st.write(
                "Fondée dans un esprit de franche camaraderie, notre amicale s'attache à développer "
                "la pratique et le rayonnement du sport-boules (Boule Lyonnaise) sur les territoires de "
                "Saint-Genix-les-Villages (Savoie) et d'Aoste (Isère)."
            )
            st.markdown(f"🔗 *Suivez l'actualité en direct sur notre [Page Facebook Officielle]({URL_FACEBOOK}).*")
        
        # --- SECTION PLAN D'ACCÈS INTERACTIF ---
        st.markdown(" ")
        st.markdown("### 🗺️ Plan d'accès aux terrains")
        st.write("Cliquez pour lancer votre application ou copiez les coordonnées pour votre GPS :")
        
        # Carte centrée et bien proportionnée
        st.map(pd.DataFrame(DONNEES_CARTE), latitude="latitude", longitude="longitude", size=40, height=280)

        st.markdown(" ") 
        st.markdown("#### 🚗 Configuration du GPS :")
        
        # --- ZONE SAINT-GENIX (Jeux de la Glière) ---
        st.markdown("##### 📍 Jeux de La Glière (Saint-Genix)")
        
        # On extrait proprement la latitude et la longitude de Saint-Genix (Index 0)
        lat_sg = DONNEES_CARTE['latitude'][0]
        lon_sg = DONNEES_CARTE['longitude'][0]
        coords_texte_sg = f"{lat_sg}, {lon_sg}"
        
        col_sg1, col_sg2, col_sg3 = st.columns([1, 1, 1.5])
        with col_sg1:
            # Lien corrigé avec le slash / obligatoire après le .com/maps/dir/
            st.link_button(
                "🗺️ Google Maps", 
                f"https://google.com/maps?q={lat_sg},{lon_sg}", 
                use_container_width=True
            )
        with col_sg2:
            st.link_button(
                "🚙 Waze", 
                f"https://waze.com{lat_sg},{lon_sg}&navigate=yes", 
                use_container_width=True
            )
        with col_sg3:
            st.text_input("Coordonnées GPS 1", value=coords_texte_sg, key="gps_sg", label_visibility="collapsed")

        st.markdown(" ") 

        # --- ZONE AOSTE (Terrains d'Aoste) ---
        st.markdown("##### 📍 Terrains d'Aoste")
        
        # On extrait proprement la latitude et la longitude d'Aoste (Index 1)
        lat_aos = DONNEES_CARTE['latitude'][1]
        lon_aos = DONNEES_CARTE['longitude'][1]
        coords_texte_aos = f"{lat_aos}, {lon_aos}"
        
        col_aos1, col_aos2, col_aos3 = st.columns([1, 1, 1.5])
        with col_aos1:
            # Lien corrigé avec le slash / obligatoire après le .com/maps/dir/
            st.link_button(
                "🗺️ Google Maps", 
                f"https://google.com/maps?q={lat_aos},{lon_aos}&dir_action=navigate", 
                use_container_width=True
            )
        with col_aos2:
            st.link_button(
                "🚙 Waze", 
                f"https://waze.com{lat_aos},{lon_aos}&navigate=yes", 
                use_container_width=True
            )
        with col_aos3:
            st.text_input("Coordonnées GPS 2", value=coords_texte_aos, key="gps_aos", label_visibility="collapsed")
       
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
