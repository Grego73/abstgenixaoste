import streamlit as st
from modules.utils import envoyer_email_brevo

def afficher_contact(db):
    st.title("✉️ Contacter le Secrétariat")
    st.markdown("---")
    
    # Tout le formulaire est strictement confiné à l'intérieur de la fonction
    with st.form("contact_form", clear_on_submit=True):
        nom = st.text_input("Votre Nom / Prénom")
        email_visiteur = st.text_input("Votre Adresse E-mail")
        message = st.text_area("Votre Message")
        
        if st.form_submit_button("Envoyer au bureau"):
            if nom and email_visiteur and message:
                # 1. Sauvegarde dans la base Firestore
                db.collection("messages").add({
                    "nom": nom, 
                    "email": email_visiteur, 
                    "message": message, 
                    "statut": "Non lu"
                })
                
                # 2. Envoi de l'alerte e-mail aux administrateurs
                try:
                    email_admin = st.secrets["brevo"]["sender_email"]
                except Exception:
                    email_admin = "bureau@amicale-boule-st-genix-aoste.fr"
                    
                sujet_alerte = f"🔔 Nouveau message reçu de {nom}"
                html_alerte = f"""
                <h2>Nouveau message sur le site internet du club</h2>
                <p><strong>Expéditeur :</strong> {nom} (<a href='mailto:{email_visiteur}'>{email_visiteur}</a>)</p>
                <p><strong>Contenu du message :</strong></p>
                <div style='background-color: #F3F4F6; padding: 15px; border-left: 4px solid #1E3A8A; border-radius: 4px;'>
                    {message.replace('\n', '<br>')}
                </div>
                <p><br>👉 Traitez ce message depuis le Panneau Administration.</p>
                """
                
                envoyer_email_brevo(email_admin, sujet_alerte, html_alerte)
                st.success("Votre message a bien été transmis ! Une alerte a été envoyée au secrétariat.")
            else:
                st.error("Veuillez remplir l'intégralité du formulaire.")
