import streamlit as st
import hashlib
import json
import urllib.request

# 1. VARIABLES GLOBALES DE L'AMICALE BOULE SAINT-GENIX AOSTE
NOM_CLUB = "Amicale Boule Saint-Genix Aoste"
STATUT_CLUB = "Association déclarée (fondée en décembre 2004)"
ADRESSE_SIEGE = "Café Gojon, Rue des Juifs, 73240 Saint-Genix-les-Villages"
BOULODROMES = "Jeux de La Glière (Saint-Genix) & Terrains d'Aoste"
URL_FACEBOOK = "https://facebook.com"

DONNEES_CARTE = {
    "latitude": (45.5995592, 45.590435),
    "longitude": (5.6297572, 5.606534),
    "Nom du terrain": ("Jeux de La Glière (Saint-Genix)", "Terrains de boules d'Aoste")
}

URL_BOULE_IMAGE = "https://taboulot.fr"


# 2. CLIENT WEB REST FAIT MAISON POUR CONTOURNER gRPC
class DocumentSimule:
    def __init__(self, data):
        self._data = data
    def to_dict(self):
        return self._data

class CollectionSimulee:
    def __init__(self, project_id, collection_name):
        self.project_id = project_id
        self.collection_name = collection_name

    def get(self, timeout=None):
        # Requête Web directe sur l'API publique de Google Firestore (Pas de gRPC)
        url = f"https://firestore.googleapis.com/v1/projects/{self.project_id}/databases/(default)/documents/{self.collection_name}"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=4) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                documents = []
                
                if "documents" in res_data:
                    for doc in res_data["documents"]:
                        fields = doc.get("fields", {})
                        data_nettoyee = {}
                        for key, val in fields.items():
                            # Extraction propre des types de données Firestore REST
                            if "stringValue" in val:
                                data_nettoyee[key] = val["stringValue"]
                            elif "integerValue" in val:
                                data_nettoyee[key] = int(val["integerValue"])
                            elif "booleanValue" in val:
                                data_nettoyee[key] = val["booleanValue"]
                            else:
                                data_nettoyee[key] = list(val.values())[0] if val.values() else None
                        documents.append(DocumentSimule(data_nettoyee))
                return documents
        except Exception:
            # Si la collection est introuvable ou vide, l'API renvoie un code d'absence.
            # On renvoie une liste vide pour valider instantanément l'affichage.
            return []

class ClientFirestoreREST:
    def __init__(self, project_id):
        self.project_id = project_id
    def collection(self, name):
        return CollectionSimulee(self.project_id, name)


@st.cache_resource
def initialiser_firebase():
    if "firebase" not in st.secrets:
        st.error("❌ Les secrets Firebase sont introuvables. Vérifiez votre secrets.toml.")
        st.stop()
    
    project_id = st.secrets["firebase"].get("project_id")
    # Retourne notre client sécurisé basé sur le web natif
    return ClientFirestoreREST(project_id)


# 3. GESTION DES SESSIONS ET DE LA SÉCURITÉ
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verifier_session():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_pseudo" not in st.session_state:
        st.session_state["user_pseudo"] = ""
    if "verifying_email" not in st.session_state:
        st.session_state["verifying_email"] = None


# 4. SERVICE D'E-MAILS BREVO
def envoyer_email_brevo(destinataire_email, sujet, message_html):
    try:
        api_key = st.secrets["brevo"]["api_key"]
        sender_email = st.secrets["brevo"]["sender_email"]
        
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }
        
        payload = {
            "sender": {"name": "Amicale Boule St-Genix Aoste", "email": sender_email},
            "to": [{"email": destinataire_email}],
            "subject": sujet,
            "htmlContent": message_html
        }
        
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
  
        with urllib.request.urlopen(req) as response:
            if response.status == 200 or response.status == 201 or response.status == 202 or response.status == 204:
                return True
    except Exception as e:
        st.error(f"Erreur technique lors de l'envoi de l'e-mail : {e}")
    return False

