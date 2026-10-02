import streamlit as st
from datetime import datetime

def afficher_actualites(db):
    st.title("🏆 Résultats & Vie du Club")
    st.markdown("---")
    
    annee_actuelle = datetime.now().year
    annee_fondation = 1922
    age_club = annee_actuelle - annee_fondation
    
    # Définition des onglets
    tab_palmares, tab_histoire, tab_concours = st.tabs([
        "✨ Palmarès & Exploits", 
        f"📜 Notre Histoire ({age_club} ans)", 
        "📅 Concours du Club"
    ])
    
    # --- ONGLET 1 : PALMARÈS DYNAMIQUE ---
    with tab_palmares:
        st.subheader("🚀 Les performances de nos licenciés")
        
        try:
            st.info("🔍 Étape 1 : Tentative de ciblage de la collection 'palmares'...")
            palmares_ref = db.collection("palmares")
            
            st.info("🔍 Étape 2 : Récupération immédiate du bloc de données...")
            # 🔄 CORRECTION : .get() télécharge tout d'un coup instantanément sans flux continu
            docs = palmares_ref.get() 
            
            st.info("🔍 Étape 3 : Affichage des résultats...")
            palmares_trouve = False
            
            for doc in docs:
                palmares_trouve = True
                data = doc.to_dict()
                
                with st.container(border=True):
                    st.markdown(f"##### {data.get('titre')}")
                    st.write(f"**Joueur(s) / Équipe :** {data.get('joueurs')}")
                    st.write(data.get('description'))
                    if data.get('categorie'):
                        st.caption(f"Division / Catégorie : {data.get('categorie')}")
                        
            if not palmares_trouve:
                st.info("Aucun palmarès moderne n'a encore été encodé par le secrétariat.")
                
        except Exception as e:
            st.error(f"⚠️ Erreur technique lors du chargement des palmarès : {e}")

    # --- ONGLET 2 : HISTOIRE ---
    with tab_histoire:
        st.subheader("🌍 L'Âge d'Or Mondial : La Quadrette Roissard / Pioz")
        st.write(
            f"Fondée originellement en **{annee_fondation}**, l'association célèbre aujourd'hui ses **{age_club} ans** "
            f"d'histoire sportive ininterrompue."
        )
        with st.container(border=True):
            st.markdown("#### 🥇 Joseph Pioz - La Légende Absolue")
            st.write("• 🌍 **4 fois Champion du Monde** de Sport-Boules (Quadrettes de 1950 à 1952).")
            st.write("• 🇫🇷 **Multiple Champion de France Excellence** (1949 à Nîmes, 1950, 1951, 1953).")
            
        st.info("📊 Le club comptabilise plus de 40 participations officielles aux phases finales des Championnats de France.")

    # --- ONGLET 3 : CONCOURS ---
    with tab_concours:
        st.subheader("📅 Événements Officiels")
        
        with st.expander("🏆 Concours Annuels Traditionnels de l'Amicale"):
            st.write("• **Challenge de la Ville d'Aoste** : Grand rendez-vous annuel par poules.")
            st.write("• **Challenge Thierry Bedot** : Organisé chaque été aux jeux de La Glière.")
            
        st.markdown("#### ➕ Événements programmés :")
        try:
            concours_ref = db.collection("concours")
            # 🔄 CORRECTION ICI AUSSI : On repasse sur un .get() propre
            docs = concours_ref.get()
            events_found = False
            for doc in docs:
                events_found = True
                data = doc.to_dict()
                st.markdown(f"🔹 **{data.get('nom')}**")
                st.caption(f"Lieu : {data.get('lieu')} | Date : {data.get('date')}")
                st.write(data.get('description'))
                st.divider()
            if not events_found:
                st.info("Aucun concours supplémentaire encodé pour le moment.")
        except Exception as e:
            st.error(f"⚠️ Erreur technique lors du chargement des concours : {e}")
