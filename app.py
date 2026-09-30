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

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

st.set_page_config(page_title=NOM_CLUB, page_icon="🏆", layout="centered")

# Barre de navigation
liste_pages = ["Accueil", "La Vie du Club & Concours", "Contact", "🔑 Espace Membres"]
if st.session_state.get("is_admin", False):
    liste_pages.append("🛡️ Panneau Administration")

page = st.sidebar.radio("Navigation", liste_pages)

# --- VERROU DE SÉCURITÉ : PREMIÈRE CONNEXION COMPLÈTE ---
if st.session_state.get("logged_in", False):
    try:
        # Récupération en temps réel du profil de l'utilisateur dans Firestore
        check_user = db.collection("users").document(st.session_state["user_pseudo"]).get()
        
        if check_user.exists:
            u_data = check_user.to_dict()
            
            # Vérification de la présence de champs vides parmi les informations facultatives
            champs_a_verifier = ["nom", "prenom", "num_licence", "telephone", "club"]
            a_des_champs_vides = any(not str(u_data.get(c, "")).strip() for c in champs_a_verifier)
            
            # Si c'est sa première connexion, qu'il reste des champs vides et qu'il tente de naviguer ailleurs
            if u_data.get("premiere_connexion", True) and a_des_champs_vides and page != "🔑 Espace Membres":
                st.sidebar.warning("⚠️ Action requise : Profil incomplet")
                
                # Message d'accueil bloquant bienveillant
                st.warning("### ⚙️ Finalisation de votre inscription requise")
                st.write(
                    "Pour accéder aux différentes pages du site de l'Amicale Boule, "
                    "veuillez valider ou compléter votre profil une première fois."
                )
                st.info("👉 Rendez-vous dès maintenant sur l'onglet **🔑 Espace Membres** dans le menu de gauche.")
                
                # Interruption immédiate du chargement du reste de la page (Accueil, Contact, etc.)
                st.stop()
                
    except Exception as e:
        # Sécurité en cas de coupure temporaire avec la base de données Firestore
        st.sidebar.error("⏳ Erreur de synchronisation avec le profil.")


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
            
            # --- AJOUT SECTION CENTENAIRE ---
            st.markdown("### 📜 Un Club Centenaire au Riche Passé")
            st.write(
                "L'événement marquant de notre histoire récente reste la célébration de notre **centenaire**, "
                "orchestrée avec ferveur en **juillet 2022**. C’est à cette occasion mémorable que notre association "
                "locale a soufflé ses **100 bougies**, entourée de ses membres actifs, de ses fidèles bénévoles et de ses partenaires."
            )
            drapeau_france = "\U0001F1EB\U0001F1F7"
            st.write("Ce cap historique a mis en lumière un palmarès exceptionnel qui fait la fierté de notre territoire :")
            st.markdown(f"- {drapeau_france} Une **quarantaine de participations aux championnats de France**.")
            st.markdown("- 🏆 De multiples titres de **champions de Savoie** (à l'image des qualifications régulières de nos équipes en simple, double ou quadrette).")
            # ---------------------------------
            
            st.markdown(f"🔗 *Suivez l'actualité en direct sur notre [Page Facebook Officielle]({URL_FACEBOOK}).*")
                
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
                f"https://waze.com/fr/live-map/directions?to=ll.{lat_sg},{lon_sg}", 
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
                f"https://waze.com/fr/live-map/directions?to=ll.{lat_aos},{lon_aos}&navigate=yes", 
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

# --- PAGE ADMINISTRATION ---
elif page == "🛡️ Panneau Administration":
    # Double sécurité au cas où l'URL ou l'état changerait frauduleusement
    if not st.session_state.get("is_admin", False):
        st.error("Accès refusé. Vous devez être administrateur.")
        st.stop()
        
    st.title("🛡️ Espace Gestionnaires & Administrateurs")
    st.markdown("---")
    
    admin_tab1, admin_tab2, admin_tab3 = st.tabs([
        "📅 Ajouter un Concours", "📋 Gestion des Licences", "✉️ Messages Reçus"
    ])
    
    # Onglet 1 : Ajouter un Concours
    with admin_tab1:
        st.subheader("Créer un nouvel événement officiel")
        with st.form("add_event_form", clear_on_submit=True):
            c_nom = st.text_input("Nom du Concours (ex: Grand Prix d'Aoste)")
            c_lieu = st.selectbox("Lieu de la compétition", [
                "Jeux de La Glière (Saint-Genix)", 
                "Terrains d'Aoste", 
                "Autre / Extérieur"
            ])
            c_date = st.text_input("Date et heure (ex: Samedi 15 Octobre à 14h)")
            c_desc = st.text_area("Description et système de jeu (ex: 16 Quadrettes TD)")
            
            if st.form_submit_button("Publier le concours"):
                if c_nom and c_date and c_desc:
                    db.collection("concours").add({
                        "nom": c_nom,
                        "lieu": c_lieu,
                        "date": c_date,
                        "description": c_desc
                    })
                    st.success(f"Le concours '{c_nom}' a été publié avec succès !")
                else:
                    st.error("Veuillez remplir tous les champs obligatoires.")
                    
    # Onglet 2 : Gestion des Membres & Licences
    with admin_tab2:
        st.subheader("Validation et consultation des fiches membres")
        try:
            users_docs = db.collection("users").stream()
            liste_users = [d.to_dict() for d in users_docs]
            
            if liste_users:
                df_users = pd.DataFrame(liste_users)
                # On réorganise l'affichage pour le gestionnaire
                colonnes_visibles = ["pseudo", "nom", "prenom", "email", "num_licence", "club", "telephone", "role", "email_verifie"]
                # On filtre uniquement sur les colonnes existantes dans le dataframe
                colonnes_visibles = [c for c in colonnes_visibles if c in df_users.columns]
                
                st.dataframe(df_users[colonnes_visibles], use_container_width=True)
            else:
                st.info("Aucun membre inscrit pour le moment.")
        except Exception as e:
            st.error(f"Impossible de charger les utilisateurs : {e}")
            
    # Onglet 3 : Messages du Secrétariat
    with admin_tab3:
        st.subheader("Messages reçus depuis le formulaire de contact")
        try:
            messages_docs = db.collection("messages").where("statut", "==", "Non lu").stream()
            msg_found = False
            for doc in messages_docs:
                msg_found = True
                m_data = doc.to_dict()
                doc_id = doc.id
                
                with st.expander(f"📥 Message de {m_data.get('nom')} ({m_data.get('email')})"):
                    st.write(m_data.get("message"))
                    if st.button("Marquer comme lu", key=f"read_{doc_id}"):
                        db.collection("messages").document(doc_id).update({"statut": "Lu"})
                        st.success("Message archivé.")
                        st.rerun()
            if not msg_found:
                st.success("🎉 Aucun nouveau message non lu ! Tout est à jour.")
        except Exception as e:
            st.caption("Aucun message à traiter dans la base de données.")

