import streamlit as st
from datetime import datetime

def afficher_actualites(db):
    st.title("🏆 Résultats & Vie du Club")
    st.markdown("---")
    
    # --- CALCUL DYNAMIQUE DE L'ÂGE DU CLUB ---
    annee_actuelle = datetime.now().year
    annee_fondation = 1922
    age_club = annee_actuelle - annee_fondation
    
    # Intégration de la variable dynamique dans le titre de l'onglet
    tab_palmares, tab_histoire, tab_concours = st.tabs([
        "✨ Palmarès & Exploits", 
        f"📜 Notre Histoire ({age_club} ans)", 
        "📅 Concours du Club"
    ])
    
    # --- ONGLET 1 : PALMARÈS DYNAMIQUE DES JOUEURS (DEPUIS FIREBASE) ---
    with tab_palmares:
        st.subheader("🚀 Les performances de nos licenciés")
        
        try:
            palmares_ref = db.collection("palmares")
            docs = palmares_ref.stream()
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
                st.info("Aucun palmarès moderne n'a encore été encodé par le secrétariat. Les performances apparaîtront très bientôt !")
                
        except Exception:
            st.caption("Base de données des palmarès en attente d'éléments.")

    # --- ONGLET 2 : LA LÉGENDE DU CLUB (IMMUABLE AVEC VARIABLES COMPORTEMENTALES) ---
    with tab_histoire:
        st.subheader("🌍 L'Âge d'Or Mondial : La Quadrette Roissard / Pioz")
        st.write(
            f"Fondée originellement en **{annee_fondation}**, l'association célèbre aujourd'hui ses **{age_club} ans** "
            f"d'histoire sportive ininterrompue. Ancrée dans le berceau de la boule lyonnaise, elle reste la fierté "
            f"de notre territoire."
        )
        
        with st.container(border=True):
            st.markdown("#### 🥇 Joseph Pioz - La Légende Absolue")
            st.write("• 🌍 **4 fois Champion du Monde** de Sport-Boules (Quadrettes de 1950 à 1952).")
            st.write("• 🇫🇷 **Multiple Champion de France Excellence** (1949 à Nîmes, 1950, 1951, 1953).")
            st.write("• 🎖️ En hommage, le boulodrome couvert régional porte aujourd'hui son nom (*Boulodrome Joseph Pioz*).")
            
        st.info("📊 **Bilan Global :** Le club comptabilise plus de 40 participations officielles aux phases finales des Championnats de France en un siècle.")

    # --- ONGLET 3 : LECTURE DYNAMIQUE DES CONCOURS FIRESTORE ---
    with tab_concours:
        st.subheader("📅 Événements Officiels")
        
        with st.expander("🏆 Concours Annuels Traditionnels de l'Amicale"):
            st.write("• **Challenge de la Ville d'Aoste** : Grand rendez-vous annuel par poules attirant plus de 60 équipes.")
            st.write("• **Challenge Thierry Bedot** : Organisé chaque été aux jeux de La Glière.")
            st.write("• **Concours de la Vogue (Saint-Genix)** : Tournoi estival traditionnel.")
            
        st.markdown("#### ➕ Événements programmés :")
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
                st.info("Aucun concours supplémentaire encodé pour le moment.")
        except Exception:
            st.caption("Base de données en attente d'éléments.")
