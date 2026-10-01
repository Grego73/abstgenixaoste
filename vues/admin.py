import streamlit as st
import pandas as pd

def afficher_administration(db):
    if not st.session_state.get("is_admin", False):
        st.error("Accès refusé. Vous devez être administrateur.")
        st.stop()
        
    st.title("🛡️ Espace Gestionnaires & Administrateurs")
    st.markdown("---")
    
    admin_tab1, admin_tab2, admin_tab3 = st.tabs([
        "📅 Ajouter un Concours", "📋 Gestion des Licences", "✉️ Messages Reçus"
    ])
    
    # --- ONGLET 1 : AJOUTER UN CONCOURS ---
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
                    
    # --- ONGLET 2 : GESTION DES LICENCES & EXPORT ---
    with admin_tab2:
        st.subheader("Validation et consultation des fiches membres")
        try:
            users_docs = db.collection("users").stream()
            liste_users = [d.to_dict() for d in users_docs]
            
            if liste_users:
                df_users = pd.DataFrame(liste_users)
                colonnes_visibles = ["pseudo", "nom", "prenom", "email", "num_licence", "club", "telephone", "role", "email_verifie"]
                colonnes_visibles = [c for c in colonnes_visibles if c in df_users.columns]
                
                df_filtre = df_users[colonnes_visibles]
                st.dataframe(df_filtre, use_container_width=True)
                
                # 📥 AJOUT DE L'EXPORT CSV (Fonctionnalité 2 du programme)
                st.markdown("#### 📂 Extraction des données")
                csv_data = df_filtre.to_csv(index=False, encoding="utf-8-sig")
                st.download_button(
                    label="📥 Télécharger la liste des membres (CSV)",
                    data=csv_data,
                    file_name="membres_amicale_boule.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("Aucun membre inscrit pour le moment.")
        except Exception as e:
            st.error(f"Impossible de charger les utilisateurs : {e}")
            
    # --- ONGLET 3 : MESSAGES DU SECRÉTARIAT ---
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
        except Exception:
            st.caption("Aucun message à traiter dans la base de données.")
