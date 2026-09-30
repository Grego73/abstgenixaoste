import streamlit as st
from modules.utils import initialiser_firebase, verifier_session, NOM_CLUB

# 🔐 Import du module technique d'authentification
from modules.auth import afficher_espace_membres

# 📄 Imports depuis le tout nouveau dossier 'pages'
from pages.accueil import afficher_accueil
from pages.actualites import afficher_actualites
from pages.contact import afficher_contact
from pages.admin import afficher_administration

# Lancement des configurations et de la base de données
db = initialiser_firebase()
verifier_session()

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

st.set_page_config(page_title=NOM_CLUB, page_icon="🏆", layout="centered")

# Construction dynamique de la barre de navigation
liste_pages = ["Accueil", "La Vie du Club & Concours", "Contact", "🔑 Espace Membres"]
if st.session_state.get("is_admin", False):
    liste_pages.append("🛡️ Panneau Administration")

page = st.sidebar.radio("Navigation", liste_pages)

# --- VERROU DE SÉCURITÉ : PREMIÈRE CONNEXION COMPLÈTE ---
if st.session_state.get("logged_in", False):
    try:
        check_user = db.collection("users").document(st.session_state["user_pseudo"]).get()
        if check_user.exists:
            u_data = check_user.to_dict()
            champs_a_verifier = ["nom", "prenom", "num_licence", "telephone", "club"]
            a_des_champs_vides = any(not str(u_data.get(c, "")).strip() for c in champs_a_verifier)
            
            if u_data.get("premiere_connexion", True) and a_des_champs_vides and page != "🔑 Espace Membres":
                st.sidebar.warning("⚠️ Action requise : Profil incomplet")
                st.warning("### ⚙️ Finalisation de votre inscription requise")
                st.write("Pour accéder aux différentes pages du site de l'Amicale Boule, veuillez valider ou compléter votre profil une première fois.")
                st.info("👉 Rendez-vous dès maintenant sur l'onglet **🔑 Espace Membres** dans le menu de gauche.")
                st.stop()
    except Exception:
        st.sidebar.error("⏳ Erreur de synchronisation avec le profil.")

# --- ROUTAGE DES PAGES ---
if page == "Accueil":
    afficher_accueil()

elif page == "La Vie du Club & Concours":
    afficher_actualites(db)

elif page == "Contact":
    afficher_contact(db)

elif page == "🔑 Espace Membres":
    afficher_espace_membres(db)

elif page == "🛡️ Panneau Administration":
    afficher_administration(db)
