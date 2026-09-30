import streamlit as st
import hashlib
import random

# Hachage sécurisé du mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def afficher_espace_membres(db):
    if st.session_state["logged_in"]:
        st.title(f"👋 Bienvenue dans votre espace, {st.session_state['user_pseudo']} !")
        st.success("Vous êtes connecté au site de votre club.")
        
        st.subheader("Informations internes du club")
        st.write("Prochaines réunions du bureau, documents internes du club, etc.")
        
        if st.button("Se déconnecter"):
            st.session_state["logged_in"] = False
            st.session_state["user_pseudo"] = ""
            st.rerun()
            
    elif st.session_state["verifying_email"]:
        st.title("✉️ Vérification de votre adresse E-mail")
        st.warning("Un code de vérification à 6 chiffres a été généré pour votre compte.")
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

    else:
        auth_action = st.tabs(["Connexion", "Créer un compte", "Mot de passe oublié"])
        
        # 1. CONNEXION
        with auth_action:
            st.subheader("Connectez-vous à votre espace club")
            login_pseudo = st.text_input("Pseudo / Identifiant", key="login_p")
            login_password = st.text_input("Mot de passe", type="password", key="login_pwd")
            
            if st.button("Se connecter"):
                user_ref = db.collection("users").document(login_pseudo).get()
                if user_ref.exists:
                    user_data = user_ref.to_dict()
                    if user_data.get("password") == hash_password(login_password):
                        if not user_data.get("email_verifie", False):
                            st.error("Votre adresse e-mail n'a pas encore été vérifiée.")
                        else:
                            st.session_state["logged_in"] = True
                            st.session_state["user_pseudo"] = login_pseudo
                            st.success("Connexion réussie !")
                            st.rerun()
                    else:
                        st.error("Mot de passe incorrect.")
                else:
                    st.error("Ce pseudo n'existe pas.")

        # 2. INSCRIPTION
        with auth_action:
            st.subheader("Formulaire d'inscription")
            st.markdown("**Champs obligatoires**")
            reg_pseudo = st.text_input("Pseudo choisi")
            reg_email = st.text_input("Adresse e-mail")
            reg_password = st.text_input("Mot de passe", type="password", key="reg_pwd")
            
            st.markdown("---")
            st.markdown("**Informations facultatives**")
            opt_nom = st.text_input("Nom (Facultatif)")
            opt_prenom = st.text_input("Prénom (Facultatif)")
            opt_licence = st.text_input("N° de Licence (Facultatif)")
            opt_telephone = st.text_input("N° de Téléphone (Facultatif)")
            
            if st.button("Créer mon compte"):
                if not reg_pseudo or not reg_email or not reg_password:
                    st.error("Veuillez remplir tous les champs obligatoires.")
                else:
                    check_user = db.collection("users").document(reg_pseudo).get()
                    if check_user.exists:
                        st.error("Ce pseudo est déjà pris.")
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
                            "telephone": opt_telephone
                        })
                        st.warning("Compte créé ! Validez votre e-mail à l'étape suivante.")
                        st.rerun()

        # 3. MOT DE PASSE OUBLIÉ
        with auth_action:
            st.subheader("Réinitialiser votre mot de passe")
            forgot_pseudo = st.text_input("Entrez votre Pseudo", key="forgot_p")
            new_password = st.text_input("Entrez votre NOUVEAU mot de passe", type="password", key="forgot_pwd")
            
            if st.button("Mettre à jour le mot de passe"):
                user_doc = db.collection("users").document(forgot_pseudo).get()
                if user_doc.exists:
                    db.collection("users").document(forgot_pseudo).update({
                        "password": hash_password(new_password)
                    })
                    st.success("Mot de passe modifié avec succès !")
                else:
                    st.error("Ce pseudo n'existe pas.")
