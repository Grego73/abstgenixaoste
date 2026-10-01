import streamlit as st
import pandas as pd
import os
from modules.utils import NOM_CLUB, STATUT_CLUB, ADRESSE_SIEGE, BOULODROMES, URL_FACEBOOK, DONNEES_CARTE

def afficher_accueil():
    # 1. EN-TÊTE : Gestion propre du logo (local ou distant en secours)
    path_logo = "assets/logo_club.png"
    
    col_l1, col_l2, col_l3 = st.columns([2, 2, 2])
    with col_l2: # Centre le logo
        if os.path.exists(path_logo):
            st.image(path_logo, use_container_width=True)
        else:
            # Emoji géant si l'image n'est pas encore téléversée dans le dossier assets
            st.markdown("<h1 style='text-align: center; font-size: 70px;'>🏆</h1>", unsafe_content_type=True)

    # Titres et sous-titres centrés
    st.markdown(f"<h1 style='text-align: center;'>{NOM_CLUB}</h1>", unsafe_content_type=True)
    st.markdown(f"<p style='text-align: center; font-style: italic; color: gray;'>{STATUT_CLUB}</p>", unsafe_content_type=True)
    st.markdown("---")

    # 2. SÉPARATION EN ONGLETS POUR ALLÉGER LA PAGE
    tab_presentation, tab_histoire, tab_acces = st.tabs([
        "📍 Présentation & Infos", "📜 Notre Histoire", "🚗 Accès & GPS"
    ])

    # --- Onglet 1 : Informations Générales ---
    with tab_presentation:
        with st.container(border=True):
            st.markdown("### 🎯 Notre Mission")
            st.write(
                "Fondée dans un esprit de franche camaraderie, notre amicale s'attache à développer "
                "la pratique et le rayonnement du sport-boules (Boule Lyonnaise) sur les territoires de "
                "Saint-Genix-les-Villages (Savoie) et d'Aoste (Isère)."
            )
            
            st.markdown("### 🏠 Coordonnées")
            st.write(f"**Siège social :** {ADRESSE_SIEGE}")
            st.write(f"**Lieux d'entraînement et compétitions :** {BOULODROMES}")
            
            st.markdown(f"🔗 *Suivez notre actualité en direct sur notre [Page Facebook Officielle]({URL_FACEBOOK}).*")

    # --- Onglet 2 : Histoire & Palmarès ---
    with tab_histoire:
        st.markdown("### 📜 Un Club Centenaire au Riche Passé")
        st.write(
            "L'événement marquant de notre histoire récente reste la célébration de notre **centenaire**, "
            "orchestrée avec ferveur en **juillet 2022**. C’est à cette occasion mémorable que notre association "
            "locale a soufflé ses **100 bougies**, entourée de ses membres actifs, de ses fidèles bénévoles et de ses partenaires."
        )
        
        # Optionnel : Affichage de la photo souvenir si elle existe
        path_photo = "assets/photo_centenaire.jpg"
        if os.path.exists(path_photo):
            st.image(path_photo, caption="Célébration du centenaire du club (Juillet 2022)", use_container_width=True)
            
        st.markdown("#### ✨ Un Palmarès d'Exception")
        
        # Utilisation de colonnes de métriques pour un design professionnel
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="Participations au Championnat de France", value="~40 🇨🇵")
        with col_m2:
            st.metric(label="Titres cumulés", value="Multiples 🏆", delta="Savoie & Région")
            
        st.info("💡 À l'image des qualifications régulières de nos équipes en simple, double ou quadrette.")

    # --- Onglet 3 : Carte Interactive & Guidage GPS ---
    with tab_acces:
        st.markdown("### 🗺️ Carte des Terrains")
        st.map(pd.DataFrame(DONNEES_CARTE), latitude="latitude", longitude="longitude", size=40, height=300)

        st.markdown("---")
        st.markdown("#### 🚗 Lancer le Guidage GPS")
        
        # --- ZONE SAINT-GENIX ---
        st.markdown("##### 📍 Jeux de La Glière (Saint-Genix)")
        lat_sg, lon_sg = DONNEES_CARTE['latitude'][0], DONNEES_CARTE['longitude'][0]
        
        col_sg1, col_sg2, col_sg3 = st.columns([1, 1, 1.5])
        with col_sg1:
            st.link_button("🗺️ Google Maps", f"https://google.com{lat_sg},{lon_sg}", use_container_width=True)
        with col_sg2:
            st.link_button("🚙 Waze", f"https://waze.com.{lat_sg},{lon_sg}", use_container_width=True)
        with col_sg3:
            st.text_input("Coordonnées GPS 1", value=f"{lat_sg}, {lon_sg}", key="gps_sg", label_visibility="collapsed")

        st.markdown(" ") 

        # --- ZONE AOSTE ---
        st.markdown("##### 📍 Terrains d'Aoste")
        lat_aos, lon_aos = DONNEES_CARTE['latitude'][1], DONNEES_CARTE['longitude'][1]
        
        col_aos1, col_aos2, col_aos3 = st.columns([1, 1, 1.5])
        with col_aos1:
            st.link_button("🗺️ Google Maps", f"https://google.com{lat_aos},{lon_aos}&dir_action=navigate", use_container_width=True)
        with col_aos2:
            st.link_button("🚙 Waze", f"https://waze.com.{lat_aos},{lon_aos}&navigate=yes", use_container_width=True)
        with col_aos3:
            st.text_input("Coordonnées GPS 2", value=f"{lat_aos}, {lon_aos}", key="gps_aos", label_visibility="collapsed")
