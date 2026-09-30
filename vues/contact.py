import streamlit as st

def afficher_contact(db):
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
