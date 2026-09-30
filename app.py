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

# --- VERROU DE SÉCURITÉ OPTIMISÉ (PLUS DE BOUCLE INFINIE) ---
if st.session_state.get("logged_in", False):
    # On initialise la variable dans la session pour éviter les lectures Firestore répétitives
    if "premiere_connexion" not in st.session_state:
        try:
            check_user = db.collection("users").document(st.session_state["user_pseudo"]).get()
            if check_user.exists:
                u_data = check_user.to_dict()
                st.session_state["premiere_connexion"] = u_data.get("premiere_connexion", True)
                st.session_state["user_club"] = u_data.get("club", "")
                st.session_state["user_nom"] = u_data.get("nom", "")
                st.session_state["user_prenom"] = u_data.get("prenom", "")
                st.session_state["user_licence"] = u_data.get("num_licence", "")
                st.session_state["user_telephone"] = u_data.get("telephone", "")
            else:
                st.session_state["premiere_connexion"] = False
        except Exception:
            st.session_state["premiere_connexion"] = False

    # Vérification locale ultra-rapide des champs vides (sans appel Firebase externe)
    champs_profil = [
        st.session_state.get("user_nom", ""),
        st.session_state.get("user_prenom", ""),
        st.session_state.get("user_licence", ""),
        st.session_state.get("user_telephone", ""),
        st.session_state.get("user_club", "")
    ]
    a_des_champs_vides = any(not str(c).strip() for c in champs_profil)

    # Blocage uniquement si c'est requis
    if st.session_state.get("premiere_connexion", True) and a_des_champs_vides and page != "🔑 Espace Membres":
        st.sidebar.warning("⚠️ Action requise : Profil incomplet")
        st.warning("### ⚙️ Finalisation de votre inscription requise")
        st.write("Pour accéder aux différentes pages, veuillez valider ou compléter votre profil une première fois.")
        st.info("👉 Rendez-vous sur l'onglet **🔑 Espace Membres** dans le menu de gauche pour débloquer le site.")
        st.stop()


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
