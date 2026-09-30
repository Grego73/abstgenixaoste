import streamlit as st

def afficher_actualites(db):
    st.title("🏆 Résultats & Compétitions")
    st.markdown("---")
    
    st.subheader("✨ Les grands moments du club")
    col1, col2 = st.columns(2)
    with col1:
        st.success("📈 **Performance Historique !**")
        st.write("Le club a enregistré une performance inédite en qualifiant simultanément **6 équipes aux Championnats de France**.")
    with col2:
        st.success("🥇 **Championnat Individuel**")
        st.write("**Régine Robin** s'est illustrée avec brio en décrochant le titre de **Championne de Savoie en simple F4**.")
        
    st.markdown("---")
    st.subheader("📅 Prochains Concours Officiels")
    
    try:
        concours_ref = db.collection("concours")
        docs = concours_ref.stream()
        events_found = False
        for doc in docs:
            events_found = True
            data = doc.to_dict()
            st.markdown(f"🔹 **{data.get('nom')}**")
            st.caption(f"Lieu : {data.get('lieu')} | Date : {data.get('date')}")
            st.write(data.get('description'))
            st.divider()
        if not events_found:
            st.info("Aucun événement encodé dans la base de données. Utilisez l'espace membre pour ajouter un concours.")
    except Exception:
        st.caption("Base de données en attente d'éléments.")
