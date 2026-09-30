import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialisation sécurisée de Firebase
if not firebase_admin._apps:
    try:
        # 1. Récupération des secrets
        fb_secrets = dict(st.secrets["firebase"])
        
        # 2. Nettoyage chirurgical de la clé privée
        if "private_key" in fb_secrets:
            pk = fb_secrets["private_key"]
            # On enlève les balises temporairement pour nettoyer le cœur de la clé
            pk_clean = pk.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "")
            # On supprime TOUS les espaces, retours à la ligne et anti-slash n cachés
            pk_clean = pk_clean.replace("\n", "").replace("\\n", "").replace(" ", "").strip()
            
            # On découpe proprement le cœur de la clé par blocs exacts de 64 caractères
            lines = [pk_clean[i:i+64] for i in range(0, len(pk_clean), 64)]
            
            # On remet l'en-tête et le pied de page officiels
            pk_final = "-----BEGIN PRIVATE KEY-----\n" + "\n".join(lines) + "\n-----END PRIVATE KEY-----\n"
            fb_secrets["private_key"] = pk_final
            
        cred = credentials.Certificate(fb_secrets)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Erreur de configuration Firebase : {e}")
        st.stop()

# Connexion à la base de données Firestore
db = firestore.client()


# Configuration de la page internet
st.set_page_config(page_title="Club Boule Lyonnaise", page_icon="🥎", layout="wide")

# Menu de navigation de la barre latérale
page = st.sidebar.radio("Navigation", ["Accueil", "Infos Pratiques", "Actualités & Concours", "Contact"])

# --- PAGE 1 : ACCUEIL ---
if page == "Accueil":
    st.title("🥎 Bienvenue au Club de Boule Lyonnaise")
    st.markdown("---")
    st.write("Suivez toute la vie de notre club, nos entraînements et nos compétitions officielles ici !")
    
    st.info(
        "Bienvenue sur le site officiel de notre club de Sport-Boules ! "
        "Passionnés, compétiteurs ou simples amateurs, notre club vous accueille "
        "tout au long de l'année dans une ambiance conviviale."
    )

# --- PAGE 2 : INFOS PRATIQUES ---
elif page == "Infos Pratiques":
    st.title("📅 Infos Pratiques")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⏰ Horaires d'entraînements")
        st.write("- **Mardi** : 17h00 - 20h00")
        st.write("- **Samedi** : 09h00 - 12h00")
    with col2:
        st.subheader("💳 Tarifs Licences")
        st.write("- **Adultes** : 60 € / an")
        st.write("- **Jeunes (-18 ans)** : Gratuit")

# --- PAGE 3 : ACTUALITÉS & CONCOURS (Lecture depuis Firebase) ---
elif page == "Actualités & Concours":
    st.title("🏆 Actualités & Prochains Concours")
    st.markdown("---")
    
    try:
        # Lecture des concours dans la collection "concours" de Firebase
        concours_ref = db.collection("concours")
        docs = concours_ref.stream()
        
        events_found = False
        for doc in docs:
            events_found = True
            data = doc.to_dict()
            st.subheader(f"🔹 {data.get('nom', 'Concours sans nom')}")
            st.caption(f"Date : {data.get('date', 'Non définie')} | Lieu : {data.get('lieu', 'Non défini')}")
            st.write(data.get('description', 'Aucune description disponible.'))
            st.divider()
            
        if not events_found:
            st.info("Aucun concours planifié pour le moment. Revenez bientôt !")
            
    except Exception as e:
        st.error("Impossible de charger les concours.")
        st.caption(f"Détail technique : {e}")

# --- PAGE 4 : CONTACT (Écriture vers Firebase) ---
elif page == "Contact":
    st.title("✉️ Nous Contacter")
    st.markdown("---")
    
    with st.form("contact_form", clear_on_submit=True):
        nom = st.text_input("Votre Nom et Prénom")
        email = st.text_input("Votre Adresse E-mail")
        message = st.text_area("Votre Message")
        submit = st.form_submit_button("Envoyer le message")
        
        if submit:
            if nom and email and message:
                try:
                    # Envoi des données dans la collection "messages" de Firebase
                    db.collection("messages").add({
                        "nom": nom,
                        "email": email,
                        "message": message,
                        "statut": "Non lu"
                    })
                    st.success("Votre message a bien été envoyé au secrétariat du club !")
                except Exception as e:
                    st.error("Une erreur est survenue lors de l'envoi du message.")
                    st.caption(f"Détail technique : {e}")
            else:
                st.error("Veuillez remplir tous les champs du formulaire.")
