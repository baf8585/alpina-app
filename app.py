import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="AlpinaAi - Bilan Flash",
    page_icon="🏔️",
    layout="centered"
)

# --- STYLE VISUEL (CSS PRO) ---
st.markdown("""
    <style>
    .main-header {text-align: center; color: #003366;}
    .sub-text {text-align: center; color: #666;}
    .stButton>button {width: 100%; background-color: #003366; color: white; font-weight: bold; padding: 12px; border-radius: 8px;}
    .report-box {background-color: #ffffff; padding: 25px; border-radius: 10px; border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .report-header {color: #003366; border-bottom: 2px solid #d4af37; padding-bottom: 10px; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.markdown("<h1 class='main-header'>🏔️ AlpinaAi</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Découvrez votre profil professionnel et votre potentiel sur le marché Suisse en 5 minutes.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- GESTION SÉCURISÉE DE LA CLÉ API ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Erreur technique : La clé API n'est pas configurée dans les Secrets Streamlit.")
    st.stop()

# --- SIDEBAR (Barre latérale) ---
with st.sidebar:
    st.header("À propos")
    st.info("Ce test utilise l'intelligence artificielle **Gemini 2.5** pour analyser vos Soft-Skills.")
    st.markdown("---")
    st.write("**Pour les entreprises :**")
    st.write("Trouvez les meilleurs talents de demain.")
    st.write("📧 contact@alpinaai.ch")
    st.markdown("---")
    st.caption("© 2025 AlpinaAi Switzerland")

# --- LE CERVEAU (Prompt Système) ---
SYSTEM_PROMPT = """
Tu es AlpinaAi, l'IA experte en recrutement suisse.
Analyse les réponses QCM ci-dessous pour un profil Junior (20-30 ans).

Génère une réponse structurée exactement comme suit (utilise le Markdown pour le gras et les titres) :

### 💎 [Invente ici un Titre de Profil Valorisant]

**🧠 Analyse de vos Forces :**
[Rédige un paragraphe de 3-4 lignes. Sois précis, psychologue et valorisant. Analyse comment ses choix (Deadline, Conflit, etc.) révèlent ses soft-skills.]

**⚠️ Point de vigilance :**
[Une phrase bienveillante sur un axe d'amélioration.]

**🇨🇭 Votre Potentiel sur le Marché Suisse :**
* **[Secteur 1]** : [Pourquoi ?]
* **[Secteur 2]** : [Pourquoi ?]
* **[Secteur 3]** : [Pourquoi ?]

---
**🎁 Le Conseil Alpina :**
[Un conseil carrière court et percutant. Invite-le à contacter l'équipe pour valider ce potentiel.]
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
        st.warning("Merci d'entrer votre prénom pour lancer l'analyse.")
    else:
        with st.spinner("🧠 AlpinaAi analyse vos réponses..."):
            try:
                # 1. Configurer Gemini
                genai.configure(api_key=api_key)
                
                # --- C'EST ICI QUE NOUS AVONS CORRIGÉ LE MODÈLE ---
                model = genai.GenerativeModel('gemini-2.5-flash')
                # --------------------------------------------------
                
                # 2. Préparer le message pour l'IA
                prompt_content = f"Voici les réponses du candidat nommé {user_name} :\n"
                for k, v in reponses_user.items():
                    prompt_content += f"- Question : {questions[k]} / Réponse : {v}\n"
                
                full_prompt = SYSTEM_PROMPT + "\n" + prompt_content

                # 3. Envoyer et recevoir
                response = model.generate_content(full_prompt)
                
                # 4. Afficher le résultat
                st.balloons()
                st.success("Analyse terminée avec succès !")
                
                st.markdown(f"<div class='report-box'>", unsafe_allow_html=True)
                st.markdown(f"<h2 class='report-header'>Bilan Flash : {user_name}</h2>", unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Une erreur est survenue. Détails : {e}")
