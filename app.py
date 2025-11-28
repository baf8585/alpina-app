import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="AlpinaAi - Bilan Flash",
    page_icon="🏔️",
    layout="centered"
)

# --- STYLE VISUEL (CSS) ---
st.markdown("""
    <style>
    .main-header {text-align: center; color: #003366;}
    .sub-text {text-align: center; color: #666;}
    .stButton>button {width: 100%; background-color: #003366; color: white; font-weight: bold; padding: 10px;}
    .report-box {background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #003366;}
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.markdown("<h1 class='main-header'>🏔️ AlpinaAi</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Découvrez votre profil professionnel et votre potentiel sur le marché Suisse en 5 minutes.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- GESTION DE LA CLÉ API (VIA SECRETS) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Erreur de configuration : La clé API est manquante dans les Secrets Streamlit.")
    st.stop()

# --- SIDEBAR (Contact uniquement) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2910/2910768.png", width=100) # Petite montagne
    st.header("À propos")
    st.write("AlpinaAi utilise l'intelligence artificielle pour révéler les talents de la nouvelle génération.")
    st.markdown("---")
    st.write("**Contact Pro**")
    st.write("contact@alpinaai.ch")

# --- LE CERVEAU (Prompt Système) ---
SYSTEM_PROMPT = """
Tu es AlpinaAi, expert en recrutement suisse. Analyse les réponses QCM ci-dessous pour un profil Junior (20-30 ans).
Génère une réponse structurée ainsi, avec une mise en forme Markdown propre :

### 💎 Signature Professionnelle : [Un Titre Valorisant]

**🧠 Analyse des Forces :**
[Un paragraphe dense et expert de 3-4 lignes sur les soft-skills et le fonctionnement psychologique.]

**⚠️ Zone de Vigilance :**
[Une phrase bienveillante sur un point à surveiller.]

**🇨🇭 Potentiel Marché Suisse :**
* **[Secteur 1]** : [Pourquoi ?]
* **[Secteur 2]** : [Pourquoi ?]
* **[Secteur 3]** : [Pourquoi ?]

---
**🎁 Conseil Alpina :**
[Conclusion encourageante et invitation à contacter l'équipe pour le placement.]
"""

# --- LES QUESTIONS ---
questions = {
    "Q1_Deadline": "Un projet important tombe avec une deadline très courte. Réaction ?",
    "Q2_Bureau": "Votre espace de travail idéal ressemble à quoi ?",
    "Q3_Changement": "On vous impose une nouvelle méthode de travail. Votre avis ?",
    "Q4_Reunion": "En réunion, quel est votre comportement ?",
    "Q5_Conflit": "Un désaccord total avec un collègue. Que faites-vous ?",
    "Q6_Manager": "Pour vous, un bon manager c'est...",
    "Q7_Motivation": "Qu'est-ce qui vous ferait changer de job demain ?",
    "Q8_Decision": "Il manque 30% des infos pour décider. On fait quoi ?",
    "Q9_Echec": "Votre définition de l'échec professionnel ?",
    "Q10_Structure": "Dans quel type d'entreprise vous sentez-vous le mieux ?",
    "Q11_Apero": "Vendredi 17h, apéro d'équipe. Vous êtes où ?",
    "Q12_Reve": "Votre rêve ultime de carrière ?"
}

options = {
    "Q1_Deadline": ["Je fonce ! L'adrénaline m'aide.", "Je planifie tout minute par minute.", "Je réunis l'équipe, impossible seul.", "Je négocie le délai pour la qualité."],
    "Q2_Bureau": ["Chaos créatif, mais je m'y retrouve.", "Minimaliste et ultra-rangé.", "Des post-its partout.", "Propre avec ma touche perso."],
    "Q3_Changement": ["Super ! J'adore la nouveauté.", "Sceptique. Pourquoi changer ?", "J'analyse d'abord les gains.", "Je demande l'avis des autres."],
    "Q4_Reunion": ["J'écoute et je synthétise.", "Je lance plein d'idées.", "Je pose les questions difficiles.", "J'observe et je note."],
    "Q5_Conflit": ["Je sors les faits et les chiffres.", "Je cherche le compromis.", "Je maintiens ma position fermement.", "On teste les deux solutions."],
    "Q6_Manager": ["Quelqu'un qui me laisse libre.", "Un coach présent au quotidien.", "Un visionnaire inspirant.", "Un protecteur bienveillant."],
    "Q7_Motivation": ["L'argent et les bonus.", "Apprendre une tech de pointe.", "Une mission sociale/écologique.", "Le pouvoir et le management."],
    "Q8_Decision": ["Je décide à l'instinct.", "Je refuse sans toutes les données.", "Je consulte des experts.", "Je fais un scénario 'Pire Cas'."],
    "Q9_Echec": ["Une honte à éviter.", "Une opportunité d'apprendre.", "Inévitable pour innover.", "Un manque de préparation."],
    "Q10_Structure": ["Grande structure prestigieuse (Banque/Pharma).", "PME familiale suisse.", "Start-up chaos & croissance.", "Indépendant / Freelance."],
    "Q11_Apero": ["Premier au bar pour le réseau !", "30min par politesse.", "Je finis mes dossiers.", "C'est moi l'organisateur !"],
    "Q12_Reve": ["Expert mondial reconnu.", "CEO de ma propre boîte.", "Équilibre parfait Vie Pro/Perso.", "Impact positif sur la société."]
}

# --- AFFICHAGE DU FORMULAIRE ---
user_name = st.text_input("Votre Prénom", placeholder="Ex: Thomas")

reponses_user = {}

with st.form("quiz_form"):
    for key, question_text in questions.items():
        st.write(f"**{question_text}**")
        reponses_user[key] = st.radio(f"Choix pour {key}", options[key], label_visibility="collapsed")
        st.write("---")
    
    submitted = st.form_submit_button("ANALYSER MON PROFIL 🚀")

# --- LOGIQUE D'ANALYSE ---
if submitted:
    if not user_name:
        st.warning("Veuillez entrer votre prénom pour personnaliser l'analyse.")
    else:
        with st.spinner("🧠 AlpinaAi connecte ses neurones... Analyse en cours..."):
            try:
                # 1. Configurer Gemini avec la clé secrète
                genai.configure(api_key=api_key)
                
                # CHANGEMENT ICI : Utilisation du modèle Flash (plus récent)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 2. Préparer le message pour l'IA
                prompt_content = f"Voici les réponses du candidat nommé {user_name} :\n"
                for k, v in reponses_user.items():
                    prompt_content += f"- Question : {questions[k]} / Réponse : {v}\n"
                
                full_prompt = SYSTEM_PROMPT + "\n" + prompt_content

                # 3. Envoyer et recevoir
                response = model.generate_content(full_prompt)
                
                # 4. Afficher le résultat
                st.balloons() # Petite animation festive
                st.success("Analyse terminée !")
                
                st.markdown(f"<div class='report-box'>", unsafe_allow_html=True)
                st.markdown(f"## Bilan Flash pour {user_name}")
                st.markdown(response.text)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Oups, une erreur technique est survenue. Vérifiez la clé API ou réessayez. Détail: {e}")
