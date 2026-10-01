import streamlit as st
import pandas as pd
import os
from modules.utils import NOM_CLUB, STATUT_CLUB, ADRESSE_SIEGE, BOULODROMES, URL_FACEBOOK, DONNEES_CARTE

def afficher_accueil():
    # 1. EN-TÊTE : Gestion propre du logo (local ou racine en secours)
    path_logo = "assets/logo_club.png"
    if not os.path.exists(path_logo):
        path_logo = "logo_club.png" # Secours si mis à la racine
    
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l2: # Centre le logo
        if os.path.exists(path_logo):
            st.image(path_logo, use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center; font-size: 70px; margin: 0;'>🏆</h1>", unsafe_allow_html=True)

    # Titres et sous-titres centrés en HTML
    st.markdown(f"<h1 style='text-align: center; margin-top: 0;'>{NOM_CLUB}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-style: italic; color: gray;'>{STATUT_CLUB}</p>", unsafe_allow_html=True)
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
        
        path_photo = "assets/photo_centenaire.jpg"
        if os.path.exists(path_photo):
            st.image(path_photo, caption="Célébration du centenaire du club (Juillet 2022)", use_container_width=True)
            
        st.markdown("#### ✨ Un Palmarès d'Exception")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="Participations au Championnat de France", value="~40 🇨🇵")
        with col_m2:
            st.metric(label="Titres cumulés", value="Multiples 🏆", delta="Savoie & Région")
            
        st.info("💡 À l'image des qualifications régulières de nos équipes en simple, double ou quadrette.")

    # --- Onglet 3 : Carte Interactive & Guidage GPS ---
    with tab_acces:
        st.markdown("### 🗺️ Carte des Terrains")
        st.map(pd.DataFrame(DONNEES_CARTE), latitude="latitude", longitude="longitude", size=40, height=280)

        st.markdown("---")
        st.markdown("#### 🚗 Configuration du GPS :")
        
        # --- ZONE SAINT-GENIX (Jeux de la Glière - Index 0) ---
        st.markdown("##### 📍 Jeux de La Glière (Saint-Genix)")
        lat_sg = DONNEES_CARTE['latitude'][0]
        lon_sg = DONNEES_CARTE['longitude'][0]
        coords_texte_sg = f"{lat_sg}, {lon_sg}"
        
        col_sg1, col_sg2, col_sg3 = st.columns([1, 1, 1.5])
        with col_sg1:
            st.link_button(
                "🗺️ Google Maps", 
                f"https://google.com/maps?q={lat_sg},{lon_sg}", 
                use_container_width=True
            )
        with col_sg2:
            st.link_button(
                "🚙 Waze", 
                f"https://waze.com/fr/live-map/directions?to=ll.{lat_sg},{lon_sg}", 
                use_container_width=True
            )
        with col_sg3:
            st.text_input("Coordonnées GPS 1", value=coords_texte_sg, key="gps_sg", label_visibility="collapsed")

        st.markdown(" ") 

        # --- ZONE AOSTE (Terrains d'Aoste - Index 1) ---
        st.markdown("##### 📍 Terrains d'Aoste")
        lat_aos = DONNEES_CARTE['latitude'][1]
        lon_aos = DONNEES_CARTE['longitude'][1]
        coords_texte_aos = f"{lat_aos}, {lon_aos}"
        
        col_aos1, col_aos2, col_aos3 = st.columns([1, 1, 1.5])
        with col_aos1:
            st.link_button(
                "🗺️ Google Maps", 
                f"https://google.com/maps?q={lat_aos},{lon_aos}&dir_action=navigate", 
                use_container_width=True
            )
        with col_aos2:
            st.link_button(
                "🚙 Waze", 
                f"https://waze.com/fr/live-map/directions?to=ll.{lat_aos},{lon_aos}&navigate=yes", 
                use_container_width=True
            )
        with col_aos3:
            st.text_input("Coordonnées GPS 2", value=coords_texte_aos, key="gps_aos", label_visibility="collapsed")
