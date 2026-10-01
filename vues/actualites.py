import streamlit as st

def afficher_actualites(db):
    st.title("🏆 Histoire & Palmarès de l'Amicale")
    st.markdown("---")
    
    # 1. SÉPARATION PAR ÉPOQUES VIA DES ONGLETS
    tab_exploits_modernes, tab_legende_centenaire, tab_concours_locaux = st.tabs([
        "✨ Exploits Récents", "📜 Les Légendes (120 ans)", "🎯 Concours du Club"
    ])
    
    # --- ONGLET 1 : LES PERFORMANCE MODERNES ---
    with tab_exploits_modernes:
        st.subheader("🚀 Une Époque Moderne Historique")
        st.success(
            "🥇 **Performance Inédite (Juillet 2025) !** L'Amicale Boule Saint-Genix Aoste a marqué l'histoire "
            "moderne en qualifiant simultanément **6 équipes aux Championnats de France**, "
            "un exploit unique en un siècle d'existence."
        )
        
        st.markdown("#### 👩 Palmarès Féminin National & Régional")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            with st.container(border=True):
                st.markdown("##### 🥈 Nadège Benedetti (Féminines F3/F4)")
                st.write("• **L'exploit national de Bellecour** : Sacrée **vice-championne (sous-championne)** de l'emblématique Tournoi de Bellecour à Lyon (Pentecôte). Atteindre la finale de ce monument historique mondial est l'une des plus belles lignes du palmarès du club.")
                st.write("• **Trophée Émile Terrier 2025** : Sélectionnée sur le grand plateau national F3/F4 avec ses redoutables coéquipières : **Christine Barriez, Aline Metsue et Marie-Christine Nicod**.")
                st.write("• **Trophée Émile Terrier 2023** : Déjà illustrée sur ces jeux nationaux en doublette aux côtés de Sylvie Barlet (Entente St-Genix/Lucey).")
                st.caption("Pilier essentiel des catégories féminines, elle brille également lors des interclubs de secteur (ex: Meyrieu-les-Étangs).")
        
        with col_f2:
            with st.container(border=True):
                st.markdown("##### 🥇 Sophie Pettegola (Féminines F2/F3)")
                st.write("• **Vainqueur à Saint-Chef** : A remporté de haute lutte le prestigieux concours de Saint-Chef dès sa première année d'intégration au club après son transfert de Romagnieu.")
                st.write("• **Actrice du record de 2025** : Joueuse clé ayant activement propulsé le club vers sa qualification historique de 6 équipes aux Championnats de France.")
                st.write("• **Grands Prix** : S'aligne régulièrement parmi les doublettes de tête sur les concours nationaux (Mémorial Jean-Pierre Allemand au Clos de Ruy).")
                st.caption("Ancienne Secrétaire générale du club de Romagnieu avant de rejoindre Saint-Genix Aoste.")

        # Rappel des autres podiums féminins en dessous
        with st.container(border=True):
            st.write("• **Régine Robin** : Championne de Savoie en Simple Féminin F4 et qualifiée pour le Championnat de France à Dardilly.")
            st.write("• **Nadège Bénédetti** : Finaliste départementale F4, s'inclinant d'un rien (8-7) en finale face à Ruy-Montceau.")

        st.markdown("#### 👨 Palmarès Masculin & Qualifications Nationales (Saison 2026)")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            with st.container(border=True):
                st.markdown("##### 👥 Quadrette M4 (Qualifiés à Chalamont)")
                st.write("- **Philippe Revel** (Président actuel)")
                st.write("- **Daniel Courand** (Vainqueur du Challenge Rostaing-Némo 2023)")
                st.write("- **Jean Collonge**")
                st.write("- **Philippe Girerd**")
                st.write("- **Christian Berthet**")
                st.caption("🏆 Vainqueurs du Challenge National M4 après les phases de ligue en Savoie.")
        
        with col_m2:
            with st.container(border=True):
                st.markdown("##### 👥 Double National M2 (Qualifiés à Valence)")
                st.write("- **Florian Dupraz**")
                st.write("- **Cédric Mehr**")
                st.write("- **Nicolas Poulet**")
                st.caption("⚡ Qualifiés pour défendre les couleurs de l'Amicale au plus haut niveau national.")

        st.markdown("#### 🥈 Podiums Régionaux Masculins Additionnels")
        st.write("• **Martine Aubert & Daniel Courand** : Vice-champions de Savoie en Doublelette Mixte à Chambéry.")
        st.write("• **Daniel Courand** : Finaliste du tournoi régional de La Motte-Servolex (associé à T. Bedot, S. Collomb, L. Hugonnier).")

    # --- ONGLET 2 : LA LÉGENDE DU CLUB (120 ANS D'HISTOIRE) ---
    with tab_legende_centenaire:
        st.subheader("🌍 L'Âge d'Or Mondial : La Quadrette Roissard / Pioz")
        st.write(
            "Fondée originellement en **1922**, l'association a fêté son centenaire en 2022. "
            "Le repère absolu de l'histoire du club reste l'enfant du pays né en 1923 : **Joseph Pioz**."
        )
        
        with st.container(border=True):
            st.markdown("#### 🥇 Joseph Pioz - La Légende Absolue")
            st.write("• 🌍 **4 fois Champion du Monde** de Sport-Boules (Quadrettes de 1950 à 1952).")
            st.write("• 🇫🇷 **Multiple Champion de France Excellence** (1949 à Nîmes, 1950, 1951, 1953).")
            st.write("• 🎖️ En hommage, le boulodrome couvert régional porte aujourd'hui son nom (*Boulodrome Joseph Pioz*).")
            st.caption("La formation mythique mondiale était composée de : H. Roissard, A. Million, R. Reffet et Joseph Pioz.")
            
        st.info("📊 **Bilan Global :** Le club comptabilise plus de 40 participations officielles aux phases finales des Championnats de France en un siècle.")

    # --- ONGLET 3 : LECTURE DYNAMIQUE DES CONCOURS FIRESTORE ---
    with tab_concours_locaux:
        st.subheader("📅 Prochains Concours & Événements Officiels")
        
        with st.expander("🏆 Concours Annuels Traditionnels de l'Amicale"):
            st.write("• **Challenge de la Ville d'Aoste** : Grand rendez-vous annuel par poules attirant plus de 60 équipes.")
            st.write("• **Challenge Thierry Bedot** : Organisé chaque été aux jeux de La Glière (28 doublettes toutes divisions).")
            st.write("• **Concours de la Vogue (Saint-Genix)** : Tournoi estival traditionnel (Dernier vainqueur : Équipe Christolhomme).")
            st.write("• **Finales Nationales D3/D4** : Qualificatif pour le prestigieux Concours Émile Terrier (Vainqueurs : Guillot-Parigi en D3, Villiot-Guillet en D4).")
            
        st.markdown("#### ➕ Événements ajoutés par le bureau :")
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
                st.info("Aucun événement supplémentaire encodé pour le moment.")
        except Exception:
            st.caption("Base de données en attente d'éléments.")
