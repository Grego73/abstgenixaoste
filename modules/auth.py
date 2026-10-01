import streamlit as st
import random
import hashlib

# 1. FONCTION TECHNIQUE DE SÉCURITÉ
def hash_password(password):
    """Hache le mot de passe pour ne jamais le stocker en clair."""
    return hashlib.sha256(password.encode()).hexdigest()


# 2. INTERFACE UTILISATEUR (CONNEXION / INSCRIPTION / RÉCUPÉRATION)
def afficher_espace_membres(db):
    # Initialisation des variables de session pour la sécurité
    if "reset_pseudo" not in st.session_state:
        st.session_state["reset_pseudo"] = None
    if "reset_code" not in st.session_state:
        st.session_state["reset_code"] = None
    if "reset_step" not in st.session_state:
        st.session_state["reset_step"] = 1

    # --- CAS 1 : UTILISATEUR CONNECTÉ ---
    if st.session_state["logged_in"]:
        user_pseudo = st.session_state["user_pseudo"]
        user_ref = db.collection("users").document(user_pseudo).get()
        
        if not user_ref.exists:
            st.error("Erreur de session.")
            st.session_state["logged_in"] = False
            st.rerun()
            
        user_data = user_ref.to_dict()

        # Écran intermédiaire : profil incomplet lors de la première connexion
        champs_facultatifs = ["nom", "prenom", "num_licence", "telephone", "club"]
        profil_incomplet = any(not str(user_data.get(champ, "")).strip() for champ in champs_facultatifs)

        if user_data.get("premiere_connexion", True) and profil_incomplet:
            st.title("👋 Bienvenue sur votre espace !")
            st.subheader("Complétez votre profil (Facultatif)")
            
            up_nom = st.text_input("Nom", value=user_data.get("nom", ""))
            up_prenom = st.text_input("Prénom", value=user_data.get("prenom", ""))
            up_licence = st.text_input("N° de Licence", value=user_data.get("num_licence", ""))
            up_telephone = st.text_input("N° de Téléphone", value=user_data.get("telephone", ""))
            
            # --- LISTE DES CLUBS SÉCURISÉE ---
            liste_clubs = ["Aucun club", "Amicale Boule Saint-Genix Aoste"]
            
            try:
                utilisateurs = db.collection("users").stream()
                for u in utilisateurs:
                    u_data = u.to_dict()
                    if u_data:
                        c_existant = u_data.get("club")
                        if c_existant and c_existant not in ["Aucun club", ""] and c_existant not in liste_clubs:
                            liste_clubs.append(c_existant)
            except Exception:
                pass
                
            clubs_tries = sorted([c for c in liste_clubs if c != "Aucun club"])
            
            # Nettoyage de la liste pour la selectbox
            club_selectionne = st.selectbox("Votre Club / Société", ["Aucun club"] + clubs_tries + ["➕ Autre..."])
            up_club = st.text_input("Saisissez le nom du club") if club_selectionne == "➕ Autre..." else ("" if club_selectionne == "Aucun club" else club_selectionne)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Enregistrer mes informations", type="primary"):
                    db.collection("users").document(user_pseudo).update({
                        "nom": up_nom.strip(), "prenom": up_prenom.strip(),
                        "num_licence": up_licence.strip(), "telephone": up_telephone.strip(),
                        "club": up_club.strip(), "premiere_connexion": False
                    })
                    st.rerun()
            with col2:
                if st.button("Continuer sans rien ajouter"):
                    db.collection("users").document(user_pseudo).update({"premiere_connexion": False})
                    st.rerun()
            return

        # Interface standard de l'espace membre connecté
        st.title(f"👋 Espace de {st.session_state['user_pseudo']}")
        tab_accueil, tab_mon_profil = st.tabs(["🏠 Tableau de bord", "👤 Mon Profil / Mettre à jour"])
        
        with tab_accueil:
            st.success("Vous êtes connecté à l'espace membre.")
            if st.button("Se déconnecter"):
                st.session_state["logged_in"] = False
                st.session_state["user_pseudo"] = ""
                st.session_state["is_admin"] = False
                
                variables_profil = ["premiere_connexion", "user_club", "user_nom", "user_prenom", "user_licence", "user_telephone"]
                for var in variables_profil:
                    if var in st.session_state:
                        del st.session_state[var]
                        
                st.rerun()
                
        with tab_mon_profil:
            st.subheader("Modifier vos données personnelles")
            prof_nom = st.text_input("Nom", value=user_data.get("nom", ""), key="p_nom")
            prof_prenom = st.text_input("Prénom", value=user_data.get("prenom", ""), key="p_prenom")
            prof_licence = st.text_input("N° de Licence", value=user_data.get("num_licence", ""), key="p_lic")
            prof_telephone = st.text_input("N° de Téléphone", value=user_data.get("telephone", ""), key="p_tel")
            prof_club = st.text_input("Club / Société actuel", value=user_data.get("club", ""), key="p_club")
            
            if st.button("Enregistrer les modifications"):
                db.collection("users").document(user_pseudo).update({
                    "nom": prof_nom.strip(), "prenom": prof_prenom.strip(),
                    "num_licence": prof_licence.strip(), "telephone": prof_telephone.strip(), "club": prof_club.strip()
                })
                st.success("Modifications enregistrées !")
                st.rerun()

    # --- CAS 2 : VÉRIFICATION CODE EMAIL ---
    elif st.session_state["verifying_email"]:
        st.title("✉️ Vérification E-mail")
        st.info(f"👉 Code généré : {st.session_state['verification_code']}")
        code_saisi = st.text_input("Entrez le code reçu", max_chars=6)
        if st.button("Valider mon compte"):
            if code_saisi == st.session_state["verification_code"]:
                db.collection("users").document(st.session_state["verifying_email"]).update({"email_verifie": True})
                st.success("Compte validé !")
                st.session_state["verifying_email"] = None
                st.rerun()
            else:
                st.error("Code incorrect.")

    # --- CAS 3 : FORMULAIRES DE SÉCURITÉ NON CONNECTÉ ---
    else:
        tab_connexion, tab_inscription, tab_oublie = st.tabs(["Connexion", "Créer un compte", "Mot de passe oublié"])
        
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
            
            liste_clubs = ["Aucun club", "Amicale Boule Saint-Genix Aoste"]
            try:
                utilisateurs = db.collection("users").stream()
                for u in utilisateurs:
                    c_existant = u.to_dict().get("club")
                    if c_existant and c_existant not in ["Aucun club", ""] and c_existant not in liste_clubs:
                        liste_clubs.append(c_existant)
            except Exception:
                pass
            
            club_selectionne = st.selectbox("Sélectionnez votre Club", ["Aucun club"] + sorted([c for c in liste_clubs if c != "Aucun club"]) + ["➕ Autre..."])
            opt_club = st.text_input("Nom du club") if club_selectionne == "➕ Autre..." else ("" if club_selectionne == "Aucun club" else club_selectionne)
            
            if st.button("Créer mon compte"):
                if reg_pseudo and reg_email and reg_password:
                    if db.collection("users").document(reg_pseudo).get().exists:
                        st.error("Pseudo déjà pris.")
                    else:
                        st.session_state["verification_code"] = str(random.randint(100000, 999999))
                        st.session_state["verifying_email"] = reg_pseudo
                        db.collection("users").document(reg_pseudo).set({
                            "pseudo": reg_pseudo, "email": reg_email, "password": hash_password(reg_password),
                            "email_verifie": False, "nom": opt_nom.strip(), "prenom": opt_prenom.strip(),
                            "num_licence": opt_licence.strip(), "telephone": opt_telephone.strip(),
                            "club": opt_club.strip(), "role": "membre", "premiere_connexion": True
                        })
                        st.rerun()
                else:
                    st.error("Veuillez remplir les champs obligatoires.")

        # --- ONGLET 3 : MOT DE PASSE OUBLIÉ ---
        with tab_oublie:
            st.subheader("Mot de passe oublié")
            if st.session_state["reset_step"] == 1:
                forgot_pseudo = st.text_input("Entrez votre Pseudo", key="forgot_p")
                if st.button("Générer un code de récupération"):
                    if db.collection("users").document(forgot_pseudo).get().exists:
                        # Génération du code à 6 chiffres pour la réinitialisation
                        st.session_state["reset_code"] = str(random.randint(100000, 999999))
                        st.session_state["reset_pseudo"] = forgot_pseudo
                        st.session_state["reset_step"] = 2
                        st.success("Code de récupération généré !")
                        st.rerun()
                    else:
                        st.error("Ce pseudo n'existe pas dans notre base de données.")
                        
            # ÉTAPE 2 : Saisie du code reçu et du nouveau mot de passe
            elif st.session_state["reset_step"] == 2:
                st.info(f"👉 Code de récupération (simulation e-mail) : {st.session_state['reset_code']}")
                code_saisi = st.text_input("Entrez le code reçu", max_chars=6, key="forgot_code_input")
                new_password = st.text_input("Nouveau mot de passe", type="password", key="forgot_pwd")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("Mettre à jour mon mot de passe"):
                        if code_saisi == st.session_state["reset_code"] and new_password:
                            db.collection("users").document(st.session_state["reset_pseudo"]).update({
                                "password": hash_password(new_password)
                            })
                            st.success("Mot de passe modifié avec succès !")
                            # Réinitialisation des états pour la prochaine utilisation
                            st.session_state["reset_step"] = 1
                            st.session_state["reset_pseudo"] = None
                            st.session_state["reset_code"] = None
                            st.rerun()
                        else:
                            st.error("Le code est incorrect ou le mot de passe est vide.")
                with col_btn2:
                    if st.button("Annuler"):
                        st.session_state["reset_step"] = 1
                        st.session_state["reset_pseudo"] = None
                        st.session_state["reset_code"] = None
                        st.rerun()

