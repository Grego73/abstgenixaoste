import streamlit as st
import random
# On importe la fonction partagée depuis notre nouveau fichier utils
from modules.utils import hash_password

def afficher_espace_membres(db):
    if st.session_state["logged_in"]:
        st.title(f"👋 Bienvenue, {st.session_state['user_pseudo']} !")
        st.success("Vous êtes connecté à l'espace membre.")
        
        if st.button("Se déconnecter"):
            st.session_state["logged_in"] = False
            st.session_state["user_pseudo"] = ""
            st.rerun()
            
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
    else:
        # CORRECTION ICI : Dépaquetage correct des onglets Streamlit
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
                    if not user_ref.to_dict().get("email_verifie", False):
                        st.error("E-mail non vérifié.")
                    else:
                        st.session_state["logged_in"] = True
                        st.session_state["user_pseudo"] = login_pseudo
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
                            "telephone": opt_telephone
                        })
                        st.rerun()
                else:
                    st.error("Veuillez remplir les champs obligatoires (Pseudo, E-mail, Mot de passe).")

        with tab_oublie:
            st.subheader("Mot de passe oublié")
            st.warning("⚠️ Pour des raisons de sécurité, veuillez contacter un administrateur du club pour réinitialiser votre mot de passe.")
            # Optionnel : Tu pourrais ajouter un formulaire qui envoie un message dans db.collection("messages") 
            # demandant une réinitialisation de mot de passe au secrétariat.

