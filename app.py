import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="AlpinaAi - Bilan & Orientation",
    page_icon="🏔️",
    layout="centered"
)

# --- STYLE VISUEL (CSS PRO) ---
st.markdown("""
    <style>
    .main-header {text-align: center; color: #003366;}
    .sub-text {text-align: center; color: #666; font-size: 1.1em;}
    .stButton>button {width: 100%; background-color: #D32F2F; color: white; font-weight: bold; padding: 12px; border-radius: 8px; border: none;}
    .stButton>button:hover {background-color: #B71C1C;}
    .report-box {background-color: #ffffff; padding: 30px; border-radius: 10px; border: 1px solid #e0e0e0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);}
    .sales-pitch {background-color: #e3f2fd; padding: 20px; border-radius: 8px; border-left: 5px solid #2196F3; margin-top: 25px;}
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.markdown("<h1 class='main-header'>🏔️ AlpinaAi</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Révélez votre potentiel professionnel en Suisse grâce à l'IA.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- GESTION CLÉ API ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Erreur technique : Clé API manquante.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("À propos")
    st.info("Test propulsé par **Gemini 2.5 Flash**.")
    st.write("Nous connectons les talents de 20-30 ans avec les meilleures opportunités suisses.")
    st.markdown("---")
    st.write("📧 contact@alpinaai.ch")

# --- LE CERVEAU (Prompt Système Vente) ---
SYSTEM_PROMPT = """
Tu es AlpinaAi, expert en carrière suisse.
Analyse les réponses QCM ci-dessous pour un profil Junior (20-30 ans).

Génère une réponse structurée exactement comme suit (Markdown) :

### 💎 [Invente un Titre de Profil Valorisant]

**🧠 Analyse de vos Forces :**
[Paragraphe précis de 3-4 lignes sur les soft-skills révélés par ses choix.]

**⚠️ Point de vigilance :**
[Une phrase bienveillante sur un axe d'amélioration.]

**🇨🇭 Votre Potentiel sur le Marché Suisse :**
* **[Secteur 1]** : [Pourquoi ?]
* **[Secteur 2]** : [Pourquoi ?]

---
**🚀 PASSEZ À LA VITESSE SUPÉRIEURE**

[Ici, tu dois rédiger un pitch commercial très persuasif de 3 lignes.
Le but : Convaincre le candidat de souscrire au "Pack Carrière Alpina".
L'argument clé : Dis-lui que ce bilan n'est que le début. Propose-lui de configurer pour lui un **"Moteur de Recherche IA Personnalisé"**.
Explique que cet agent IA va scanner le marché caché et les sites de recrutement (LinkedIn, Jobup) spécifiquement pour SON profil, afin de lui trouver des opportunités invisibles sans qu'il ait à chercher.
Termine par une phrase engageante du type : "Ne laissez pas le hasard décider de votre carrière, activez votre agent maintenant."]
"""

# --- FORMULAIRE DONNÉES PERSONNELLES ---
st.markdown("### 1. Vos Informations")
col1, col2 = st.columns(2)
with col1:
    prenom = st.text_input("Prénom")
    pays = st.text_input("Pays de résidence")
with col2:
    nom = st.text_input("Nom")
    email = st.text_input("Email Professionnel (Obligatoire)")

st.markdown("### 2. Le Test de Personnalité")

# --- QUESTIONS ---
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
    "Q1_Deadline": ["Je fonce ! L'adrénaline m'aide.", "Je planifie tout minute par minute.", "Je réunis l'équipe.", "Je négocie le délai."],
    "Q2_Bureau": ["Chaos créatif.", "Minimaliste et ultra-rangé.", "Des post-its partout.", "Propre avec ma touche perso."],
    "Q3_Changement": ["Super ! J'adore la nouveauté.", "Sceptique. Pourquoi changer ?", "J'analyse d'abord les gains.", "Je demande l'avis des autres."],
    "Q4_Reunion": ["J'écoute et je synthétise.", "Je lance plein d'idées.", "Je pose les questions difficiles.", "J'observe et je note."],
    "Q5_Conflit": ["Je sors les faits et les chiffres.", "Je cherche le compromis.", "Je maintiens ma position.", "On teste les deux solutions."],
    "Q6_Manager": ["Quelqu'un qui me laisse libre.", "Un coach présent au quotidien.", "Un visionnaire inspirant.", "Un protecteur bienveillant."],
    "Q7_Motivation": ["L'argent et les bonus.", "Apprendre une tech de pointe.", "Une mission sociale.", "Le pouvoir et le management."],
    "Q8_Decision": ["Je décide à l'instinct.", "Je refuse sans toutes les données.", "Je consulte des experts.", "Je fais un scénario 'Pire Cas'."],
    "Q9_Echec": ["Une honte à éviter.", "Une opportunité d'apprendre.", "Inévitable pour innover.", "Un manque de préparation."],
    "Q10_Structure": ["Grande Banque / Pharma.", "PME familiale suisse.", "Start-up / Scale-up.", "Indépendant / Freelance."],
    "Q11_Apero": ["Premier au bar (Réseau !).", "30min par politesse.", "Je finis mes dossiers.", "C'est moi l'organisateur !"],
    "Q12_Reve": ["Expert mondial reconnu.", "CEO de ma propre boîte.", "Équilibre Vie Pro/Perso.", "Impact positif sur la société."]
}

reponses_user = {}

# --- AFFICHAGE QCM ---
with st.form("quiz_form"):
    for key, question_text in questions.items():
        st.write(f"**{question_text}**")
        reponses_user[key] = st.radio(f"Choix", options[key], label_visibility="collapsed", key=key)
        st.write("---")
    
    submitted = st.form_submit_button("OBTENIR MON ANALYSE & MON OFFRE 🚀")

# --- LOGIQUE ---
if submitted:
    # 1. Vérification des champs obligatoires
    if not prenom or not nom or not pays:
        st.error("⚠️ Merci de remplir votre Nom, Prénom et Pays.")
    elif not email or "@" not in email:
        st.error("⚠️ Merci d'entrer une adresse Email valide pour recevoir vos résultats.")
    else:
        with st.spinner("🧠 Configuration de votre profil IA en cours..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash') # Modèle rapide
                
                # Préparation des données pour l'IA
                user_info = f"Candidat: {prenom} {nom}, Pays: {pays}"
                prompt_content = f"{user_info}\nRéponses QCM :\n"
                for k, v in reponses_user.items():
                    prompt_content += f"- {questions[k]} : {v}\n"
                
                full_prompt = SYSTEM_PROMPT + "\n" + prompt_content

                # Appel API
                response = model.generate_content(full_prompt)
                
                # Affichage Résultat
                st.balloons()
                st.success(f"Analyse terminée pour {prenom} !")
                
                st.markdown(f"<div class='report-box'>", unsafe_allow_html=True)
                st.markdown(response.text)
                
                # Bouton de vente fictif (pour l'instant)
                st.markdown("---")
                st.button("👉 ACTIVER MON MOTEUR DE RECHERCHE IA (En savoir plus)")
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Erreur : {e}")
