import streamlit as st
import random
import pandas as pd
from modules.utils import hash_password

def afficher_espace_membres(db):
    # Initialisation des variables de session indispensables
    if "reset_pseudo" not in st.session_state:
        st.session_state["reset_pseudo"] = None
    if "reset_code" not in st.session_state:
        st.session_state["reset_code"] = None
    if "reset_step" not in st.session_state:
        st.session_state["reset_step"] = 1
    if "is_admin" not in st.session_state:
        st.session_state["is_admin"] = False

    # --- CAS 1 : UTILISATEUR CONNECTÉ ---
    if st.session_state["logged_in"]:
        user_pseudo = st.session_state["user_pseudo"]
        
        # Récupération dynamique des données fraîches depuis Firestore
        user_ref = db.collection("users").document(user_pseudo).get()
        if not user_ref.exists:
            st.error("Erreur de session. Veuillez vous reconnecter.")
            st.session_state["logged_in"] = False
            st.rerun()
            
        user_data = user_ref.to_dict()
        
        # Liste des champs facultatifs à vérifier
        champs_facultatifs = ["nom", "prenom", "num_licence", "telephone", "club"]
        profil_incomplet = any(not str(user_data.get(champ, "")).strip() for champ in champs_facultatifs)

        # ÉTAPE INTERMÉDIAIRE : Première connexion avec profil incomplet
        if user_data.get("premiere_connexion", True) and profil_incomplet:
            st.title("👋 Bienvenue sur votre espace !")
            st.subheader("Complétez votre profil (Facultatif)")
            st.info("Prenez un instant pour enrichir votre fiche de membre. Ces informations aident les bénévoles à gérer le club.")
            
            # Formulaire de mise à jour rapide
            up_nom = st.text_input("Nom", value=user_data.get("nom", ""))
            up_prenom = st.text_input("Prénom", value=user_data.get("prenom", ""))
            up_licence = st.text_input("N° de Licence", value=user_data.get("num_licence", ""))
            up_telephone = st.text_input("N° de Téléphone", value=user_data.get("telephone", ""))
            
            # Sélecteur de club dynamique identique
            liste_clubs = ["Aucun club", "Amicale Boule Saint-Genix Aoste"]
            try:
                utilisateurs = db.collection("users").stream()
                for u in utilisateurs:
                    c_existant = u.to_dict().get("club")
                    if c_existant and c_existant not in ["Aucun club", ""] and c_existant not in liste_clubs:
                        liste_clubs.append(c_existant)
            except Exception:
                pass
            
            clubs_tries = sorted([c for c in liste_clubs if c != "Aucun club"])
            liste_clubs = ["Aucun club"] + clubs_tries + ["➕ Autre..."]
            
            club_actuel = user_data.get("club", "")
            index_club = liste_clubs.index(club_actuel) if club_actuel in liste_clubs else 0
            
            club_selectionne = st.selectbox("Votre Club / Société", liste_clubs, index=index_club)
            if club_selectionne == "➕ Autre...":
                up_club = st.text_input("Saisissez le nom de votre club")
            else:
                up_club = "" if club_selectionne == "Aucun club" else club_selectionne

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enregistrer mes informations", type="primary"):
                    db.collection("users").document(user_pseudo).update({
                        "nom": up_nom.strip(),
                        "prenom": up_prenom.strip(),
                        "num_licence": up_licence.strip(),
                        "telephone": up_telephone.strip(),
                        "club": up_club.strip(),
                        "premiere_connexion": False  # On marque l'étape comme passée
                    })
                    st.success("Profil mis à jour !")
                    st.rerun()
            with col2:
                if st.button("Continuer sans rien ajouter"):
                    db.collection("users").document(user_pseudo).update({
                        "premiere_connexion": False  # Étape validée même sans saisie
                    })
                    st.rerun()
            return  # On bloque le reste de la page tant qu'il n'a pas cliqué sur l'un des deux boutons

        # ÉTAPE NORMALE : Le profil est vu, on affiche l'Espace Membre Standard
        st.title(f"👋 Espace de {st.session_state['user_pseudo']}")
        
        tab_accueil, tab_mon_profil = st.tabs(["🏠 Tableau de bord", "👤 Mon Profil / Mettre à jour"])
        
        with tab_accueil:
            st.success("Vous êtes connecté à l'espace membre de l'Amicale Boule.")
            st.write("Retrouvez ici vos documents et vos accès privilégiés.")
            if st.session_state.get("is_admin", False):
                st.info("🛡️ Mode Administrateur activé.")
                
            if st.button("Se déconnecter", key="btn_logout"):
                st.session_state["logged_in"] = False
                st.session_state["user_pseudo"] = ""
                st.session_state["is_admin"] = False
                st.rerun()
                
        with tab_mon_profil:
            st.subheader("Gestion de vos informations personnelles")
            st.write("Modifiez vos données à tout moment ci-dessous :")
            
            prof_nom = st.text_input("Nom", value=user_data.get("nom", ""), key="p_nom")
            prof_prenom = st.text_input("Prénom", value=user_data.get("prenom", ""), key="p_prenom")
            prof_licence = st.text_input("N° de Licence", value=user_data.get("num_licence", ""), key="p_lic")
            prof_telephone = st.text_input("N° de Téléphone", value=user_data.get("telephone", ""), key="p_tel")
            prof_club = st.text_input("Club / Société actuel", value=user_data.get("club", ""), key="p_club")
            
            if st.button("Enregistrer les modifications", key="btn_save_profile"):
                db.collection("users").document(user_pseudo).update({
                    "nom": prof_nom.strip(),
                    "prenom": prof_prenom.strip(),
                    "num_licence": prof_licence.strip(),
                    "telephone": prof_telephone.strip(),
                    "club": prof_club.strip()
                })
                st.success("Modifications enregistrées avec succès !")
                st.rerun()

    # --- CAS 2 : VÉRIFICATION DE L'EMAIL (INSCRIPTION) ---
    elif st.session_state["verifying_email"]:
        st.title("✉️ Vérification E-mail")
        st.info(f"👉 Code de test généré : {st.session_state['verification_code']}")
        
        code_saisi = st.text_input("Entrez le code reçu", max_chars=6)
        if st.button("Valider mon compte"):
            if code_saisi == st.session_state["verification_code"]:
                db.collection("users").document(st.session_state["verifying_email"]).update({
                    "email_verifie": True
                })
                st.success("Compte validé ! Vous pouvez maintenant vous connecter.")
                st.session_state["verifying_email"] = None
                st.rerun()
            else:
                st.error("Code incorrect.")

    # --- CAS 3 : FORMULAIRES DE CONNEXION / INSCRIPTION ---
    else:
        tab_connexion, tab_inscription, tab_oublie = st.tabs([
            "Connexion", "Créer un compte", "Mot de passe oublié"
        ])
        
        with tab_connexion:
            st.subheader("Connexion")
            login_pseudo = st.text_input("Pseudo", key="login_p")
            login_password = st.text_input("Mot de passe", type="password", key="login_pwd")
            if st.button("Se connecter"):
                user_ref = db.collection("users").document(login_pseudo).get()
                if user_ref.exists and user_ref.to_dict().get("password") == hash_password(login_password):
                    user_data = user_ref.to_dict()
                    if not user_data.get("email_verifie", False):
                        st.error("E-mail non vérifié.")
                    else:
                        st.session_state["logged_in"] = True
                        st.session_state["user_pseudo"] = login_pseudo
                        st.session_state["is_admin"] = user_data.get("role") == "admin"
                        st.rerun()
                else:
                    st.error("Identifiants incorrects.")

        with tab_inscription:
            st.subheader("Inscription")
            reg_pseudo = st.text_input("Pseudo choisi")
            reg_email = st.text_input("Adresse e-mail")
            reg_password = st.text_input("Mot de passe", type="password", key="reg_pwd")
            
            opt_nom = st.text_input("Nom (Facultatif)")
            opt_prenom = st.text_input("Prénom (Facultatif)")
            opt_licence = st.text_input("N° de Licence (Facultatif)")
            opt_telephone = st.text_input("N° de Téléphone (Facultatif)")
            
            # Liste dynamique facultative des clubs
            liste_clubs = ["Aucun club", "Amicale Boule Saint-Genix Aoste"]
            try:
                utilisateurs = db.collection("users").stream()
                for u in utilisateurs:
                    c_existant = u.to_dict().get("club")
                    if c_existant and c_existant not in ["Aucun club", ""] and c_existant not in liste_clubs:
                        liste_clubs.append(c_existant)
            except Exception:
                pass
                
            clubs_tries = sorted([c for c in liste_clubs if c != "Aucun club"])
            liste_clubs = ["Aucun club"] + clubs_tries + ["➕ Autre (Ajouter un nouveau club...)"]
            
            club_selectionne = st.selectbox("Sélectionnez votre Club ou Société", liste_clubs)
            opt_club = ""
            if club_selectionne == "➕ Autre (Ajouter un nouveau club...)":
                opt_club = st.text_input("Saisissez le nom de votre Club / Société (Facultatif)")
            elif club_selectionne != "Aucun club":
                opt_club = club_selectionne
            
            if st.button("Créer mon compte"):
                if reg_pseudo and reg_email and reg_password:
                    if db.collection("users").document(reg_pseudo).get().exists:
                        st.error("Pseudo déjà pris.")
                    else:
                        # Génération du code de validation à 6 chiffres
                        code_valid = str(random.randint(100000, 999999))
                        st.session_state["verification_code"] = code_valid
                        st.session_state["verifying_email"] = reg_pseudo
                        
                        # Enregistrement complet dans Firebase Firestore
                        db.collection("users").document(reg_pseudo).set({
                            "pseudo": reg_pseudo,
                            "email": reg_email,
                            "password": hash_password(reg_password),
                            "email_verifie": False,
                            "nom": opt_nom.strip(),
                            "prenom": opt_prenom.strip(),
                            "num_licence": opt_licence.strip(),
                            "telephone": opt_telephone.strip(),
                            "club": opt_club.strip(),
                            "role": "membre",
                            "premiere_connexion": True  # Permet le contrôle au premier accès
                        })
                        st.success("Compte créé ! Veuillez valider votre e-mail.")
                        st.rerun()
                else:
                    st.error("Veuillez remplir les champs obligatoires (Pseudo, E-mail, Mot de passe).")
