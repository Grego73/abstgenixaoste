import streamlit as st
import random
from modules.utils import hash_password

def afficher_espace_membres(db):
    # Initialisation des variables de session nécessaires pour le mot de passe oublié
    if "reset_pseudo" not in st.session_state:
        st.session_state["reset_pseudo"] = None
    if "reset_code" not in st.session_state:
        st.session_state["reset_code"] = None
    if "reset_step" not in st.session_state:
        st.session_state["reset_step"] = 1  # Étape 1 : Demande, Étape 2 : Vérification & Saisie

    # --- CAS 1 : UTILISATEUR CONNECTÉ ---
    if st.session_state["logged_in"]:
        st.title(f"👋 Bienvenue, {st.session_state['user_pseudo']} !")
        st.success("Vous êtes connecté à l'espace membre.")
        
        if st.session_state.get("is_admin", False):
            st.info("🛡️ Vous disposez des droits Administrateur pour cette session.")

        if st.button("Se déconnecter"):
            st.session_state["logged_in"] = False
            st.session_state["user_pseudo"] = ""
            st.session_state["is_admin"] = False
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
                
    # --- CAS 3 : FORMULAIRES DE CONNEXION / INSCRIPTION / RÉCUPÉRATION ---
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
                        # Vérification du rôle admin (à configurer manuellement dans Firestore pour les profils gestionnaires)
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
            
            if st.button("Créer mon compte"):
                if reg_pseudo and reg_email and reg_password:
                    if db.collection("users").document(reg_pseudo).get().exists:
                        st.error("Pseudo déjà pris.")
                    else:
                        code_valid = str(random.randint(100000, 999999))
                        st.session_state["verification_code"] = code_valid
                        st.session_state["verifying_email"] = reg_pseudo
                        
                        db.collection("users").document(reg_pseudo).set({
                            "pseudo": reg_pseudo,
                            "email": reg_email,
                            "password": hash_password(reg_password),
                            "email_verifie": False,
                            "nom": opt_nom,
                            "prenom": opt_prenom,
                            "num_licence": opt_licence,
                            "telephone": opt_telephone,
                            "role": "membre"  # Rôle par défaut
                        })
                        st.rerun()
                else:
                    st.error("Veuillez remplir les champs obligatoires (Pseudo, E-mail, Mot de passe).")

        with tab_oublie:
            st.subheader("Récupération de mot de passe")
            
            if st.session_state["reset_step"] == 1:
                forgot_pseudo = st.text_input("Entrez votre Pseudo", key="forgot_p")
                if st.button("Générer un code de récupération"):
                    user_ref = db.collection("users").document(forgot_pseudo).get()
                    if user_ref.exists:
                        code_recup = str(random.randint(100000, 999999))
                        st.session_state["reset_code"] = code_recup
                        st.session_state["reset_pseudo"] = forgot_pseudo
                        st.session_state["reset_step"] = 2
                        st.rerun()
                    else:
                        st.error("Ce pseudo n'existe pas dans notre base de données.")
                        
            elif st.session_state["reset_step"] == 2:
                st.info(f"👉 Code de récupération généré (simulation e-mail) : {st.session_state['reset_code']}")
                code_saisi = st.text_input("Entrez le code de récupération", max_chars=6, key="forgot_code_input")
                new_password = st.text_input("Nouveau mot de passe", type="password", key="forgot_pwd")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("Mettre à jour mon mot de passe"):
                        if code_saisi == st.session_state["reset_code"]:
                            if new_password:
                                db.collection("users").document(st.session_state["reset_pseudo"]).update({
                                    "password": hash_password(new_password)
                                })
                                st.success("Mot de passe modifié avec succès !")
                                # Réinitialisation de l'état
                                st.session_state["reset_step"] = 1
                                st.session_state["reset_pseudo"] = None
                                st.session_state["reset_code"] = None
                                st.rerun()
                            else:
                                st.error("Le nouveau mot de passe ne peut pas être vide.")
                        else:
                            st.error("Code de récupération incorrect.")
                with col_btn2:
                    if st.button("Annuler"):
                        st.session_state["reset_step"] = 1
                        st.session_state["reset_pseudo"] = None
                        st.session_state["reset_code"] = None
                        st.rerun()
