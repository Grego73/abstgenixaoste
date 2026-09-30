import streamlit as st
import pandas as pd
from modules.utils import NOM_CLUB, STATUT_CLUB, ADRESSE_SIEGE, BOULODROMES, URL_FACEBOOK, DONNEES_CARTE

def afficher_accueil():
    # On donne des proportions : 1.5 de vide à gauche, 5 pour le texte au centre, 1.5 de vide à droite
    col_marge_gauche, col_contenu, col_marge_droite = st.columns([1.5, 5, 1.5])
    
    with col_contenu:
        # Un titre propre bien proportionné
        st.title(f"🏆 {NOM_CLUB}")
        st.write(f"*{STATUT_CLUB}*")
        st.markdown("---")
        
        # On regroupe les informations dans un conteneur pour un rendu plus net
        with st.container(border=True):
            st.markdown("### 📍 Notre Implantation")
            st.write(f"**Siège social :** {ADRESSE_SIEGE}")
            st.write(f"**Lieux d'entraînement et compétitions :** {BOULODROMES}")
            
            st.markdown("### 🎯 Notre Mission")
            st.write(
                "Fondée dans un esprit de franche camaraderie, notre amicale s'attache à développer "
                "la pratique et le rayonnement du sport-boules (Boule Lyonnaise) sur les territoires de "
                "Saint-Genix-les-Villages (Savoie) et d'Aoste (Isère)."
            )
            
            # --- SECTION CENTENAIRE ---
            st.markdown("### 📜 Un Club Centenaire au Riche Passé")
            st.write(
                "L'événement marquant de notre histoire récente reste la célébration de notre **centenaire**, "
                "orchestrée avec ferveur en **juillet 2022**. C’est à cette occasion mémorable que notre association "
                "locale a soufflé ses **100 bougies**, entourée de ses membres actifs, de ses fidèles bénévoles et de ses partenaires."
            )
            st.write("Ce cap historique a mis en lumière un palmarès exceptionnel qui fait la fierté de notre territoire :")
            
            # Correction ici : Chaîne normale sans le 'r' pour décoder correctement l'émoji du drapeau
            drapeau_france = "\U0001F1EB\U0001F1F7"
            
            st.write(f"- {drapeau_france} Une **quarantaine de participations aux championnats de France**.")
            st.write("• 🏆 De multiples titres de **champions de Savoie** (à l'image des qualifications régulières de nos équipes en simple, double ou quadrette).")
            
            st.markdown(f"🔗 *Suivez l'actualité en direct sur notre [Page Facebook Officielle]({URL_FACEBOOK}).*")
                
        # Carte centrée et bien proportionnée
        st.map(pd.DataFrame(DONNEES_CARTE), latitude="latitude", longitude="longitude", size=40, height=280)

        st.markdown(" ") 
        st.markdown("#### 🚗 Configuration du GPS :")
        
        # --- ZONE SAINT-GENIX (Jeux de la Glière) ---
        st.markdown("##### 📍 Jeux de La Glière (Saint-Genix)")
        
        # Ton code parfait avec l'index [0]
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

        # --- ZONE AOSTE (Terrains d'Aoste) ---
        st.markdown("##### 📍 Terrains d'Aoste")
        
        # Ton code parfait avec l'index [1]
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
