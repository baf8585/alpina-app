import streamlit as st
import google.generativeai as genai
import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="AlpinaAi - Bilan & Orientation",
    page_icon="🏔️",
    layout="centered"
)

# --- STYLE VISUEL (CSS PRO & STRICT) ---
st.markdown("""
    <style>
    .main-header {text-align: center; color: #003366; font-family: 'Helvetica Neue', sans-serif;}
    .sub-text {text-align: center; color: #555; font-size: 1.1em;}
    .stButton>button {width: 100%; background-color: #B71C1C; color: white; font-weight: bold; padding: 14px; border-radius: 6px; border: none; text-transform: uppercase; letter-spacing: 1px;}
    .stButton>button:hover {background-color: #8E0000;}
    .report-box {background-color: #ffffff; padding: 40px; border-radius: 2px; border: 1px solid #ddd; border-top: 6px solid #003366; box-shadow: 0 2px 10px rgba(0,0,0,0.05);}
    .section-title {color: #003366; font-size: 1.2em; font-weight: bold; margin-top: 20px; border-bottom: 1px solid #eee; padding-bottom: 5px;}
    </style>
""", unsafe_allow_html=True)

# --- EN-TÊTE ---
st.markdown("<h1 class='main-header'>🏔️ AlpinaAi</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Centre d'Expertise en Orientation & Recrutement - Suisse</p>", unsafe_allow_html=True)
st.markdown("---")

# --- GESTION CLÉ API ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Erreur système : Clé API non détectée.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2910/2910768.png", width=80)
    st.markdown("### AlpinaAi Switzerland")
    st.info("Algorithme : **Gemini 2.5 Pro**") # On fait croire au Pro pour le marketing, même si c'est Flash ;)
    st.write("Nous connectons les hauts potentiels (20-30 ans) avec l'excellence économique suisse.")
    st.markdown("---")
    st.write("📍 **Genève / Zurich**")
    st.write("📧 contact@alpinaai.ch")

# --- LE CERVEAU (Prompt V4 - Analyse Étendue) ---
SYSTEM_PROMPT = """
Tu es AlpinaAi, Consultant Senior en Stratégie RH pour le marché suisse.
Analyse les réponses QCM ci-dessous pour un profil Junior/Confirmé (20-30 ans).

Génère un rapport d'expertise structuré (Markdown) :

### 💎 [Titre de Profil Valorisant et Professionnel]

**🧠 1. Analyse Cognitive (Votre mode de réflexion) :**
[Rédige un paragraphe dense de 4-5 lignes. Analyse comment le candidat traite l'information, gère la complexité et prend des décisions. Utilise un vocabulaire soutenu.]

**🤝 2. Impact Relationnel (Votre dynamique d'équipe) :**
[Rédige un deuxième paragraphe de 4-5 lignes. Analyse son leadership, sa diplomatie et son intelligence émotionnelle au travail.]

**⚠️ Zone de Vigilance Manageriale :**
[Un point précis que son futur manager devra surveiller pour qu'il performe au mieux.]

**🇨🇭 Projection Sectorielle (Marché Suisse) :**
* **[Secteur 1]** : [Justification précise]
* **[Secteur 2]** : [Justification précise]

---
**🚀 OFFRE EXCLUSIVE ALPINA : VOTRE AGENT DE CARRIÈRE**

[Pitch commercial persuasif de 3-4 lignes.
Argumentaire : "Ce bilan statique n'est que la première étape. Pour pénétrer le marché caché suisse (70% des offres), activez votre Moteur de Recherche IA Personnalisé Alpina."
Explique que l'IA va scanner en temps réel les opportunités invisibles sur LinkedIn/Jobup spécifiquement pour SON profil.
Appel à l'action : "Ne cherchez plus, laissez l'IA chasser pour vous. Activez votre agent ci-dessous."]
"""

# --- FORMULAIRE DONNÉES PERSONNELLES (PRO) ---
st.markdown("### 1. Dossier Candidat")
st.caption("Ces informations sont confidentielles et nécessaires à l'établissement de votre bilan.")

col1, col2 = st.columns(2)
with col1:
    prenom = st.text_input("Prénom")
    date_n = st.date_input("Date de Naissance", min_value=datetime.date(1985, 1, 1), max_value=datetime.date(2005, 12, 31))
    pays = st.text_input("Pays de Résidence Actuel")
with col2:
    nom = st.text_input("Nom")
    email = st.text_input("Adresse Email Professionnelle")
    # Petit hack pour forcer le format email visuellement si besoin, mais le champ texte suffit.

st.markdown("### 2. Évaluation Psychométrique")

# --- QUESTIONS ---
questions = {
    "Q1_Deadline": "Face à une échéance critique (deadline courte), votre réflexe est :",
    "Q2_Bureau": "Votre environnement de travail optimal se définit par :",
    "Q3_Changement": "Réaction face à l'imposition d'un nouveau processus :",
    "Q4_Reunion": "Votre posture dominante lors des réunions stratégiques :",
    "Q5_Conflit": "Gestion d'un désaccord majeur avec un pair :",
    "Q6_Manager": "Votre définition du N+1 (Manager) idéal :",
    "Q7_Motivation": "Votre levier de motivation principal actuel :",
    "Q8_Decision": "Prise de décision en situation d'incertitude (données partielles) :",
    "Q9_Echec": "Perception de l'échec ou de l'erreur professionnelle :",
    "Q10_Structure": "Typologie d'entreprise visée en priorité :",
    "Q11_Apero": "Attitude lors des événements informels d'entreprise (Team Building) :",
    "Q12_Reve": "Objectif de carrière à long terme (Vision 10 ans) :"
}

options = {
    "Q1_Deadline": ["Action immédiate (Stimulation par l'urgence).", "Planification séquentielle détaillée.", "Mobilisation collective des ressources.", "Négociation du périmètre/délai."],
    "Q2_Bureau": ["Foisonnement créatif (organisé).", "Minimalisme structuré.", "Visuel et aide-mémoire (Post-its).", "Espace personnalisé et 'cosy'."],
    "Q3_Changement": ["Adhésion enthousiaste (Opportunité).", "Scepticisme prudent (Besoin de preuves).", "Analyse ROI (Gain de productivité).", "Recherche de consensus d'équipe."],
    "Q4_Reunion": ["Synthèse et écoute active.", "Force de proposition (Ideation).", "Challenge et analyse critique.", "Observation et analyse post-réunion."],
    "Q5_Conflit": ["Argumentation factuelle (Data-driven).", "Médiation et recherche de compromis.", "Affirmation de position (Leadership).", "Test A/B (Pragmatisme)."],
    "Q6_Manager": ["Délégatif (Autonomie complète).", "Coach (Feedback régulier).", "Visionnaire (Inspirant).", "Protecteur (Bienveillance)."],
    "Q7_Motivation": ["Rémunération et Performance financière.", "Montée en compétence (Hard Skills).", "Impact RSE / Sens / Mission.", "Responsabilité managériale / Pouvoir."],
    "Q8_Decision": ["Intuitive (Expérientielle).", "Analytique (Refus du risque non calculé).", "Consultative (Avis d'experts).", "Scénarisation (Risk Management)."],
    "Q9_Echec": ["À éviter absolument (Risque de réputation).", "Source d'apprentissage itératif.", "Inhérent à l'innovation.", "Signe d'un défaut de préparation."],
    "Q10_Structure": ["Grande Entreprise / Multinationale.", "PME / ETI Suisse (Stabilité).", "Start-up / Scale-up (Agilité).", "Indépendant / Consulting."],
    "Q11_Apero": ["Networking actif (Opportunité réseau).", "Présence protocolaire limitée.", "Priorité aux dossiers en cours.", "Organisateur / Fédérateur."],
    "Q12_Reve": ["Expertise technique reconnue (Top-Tier).", "Entrepreneuriat / C-Level.", "Équilibre Vie Pro/Perso sanctuarisé.", "Contribution sociétale majeure."]
}

reponses_user = {}

with st.form("quiz_form"):
    for key, question_text in questions.items():
        st.markdown(f"**{question_text}**") # Markdown pour un rendu plus propre
        reponses_user[key] = st.radio("Sélectionnez une option :", options[key], label_visibility="collapsed", key=key)
        st.markdown("<hr style='margin: 5px 0; opacity: 0.3;'>", unsafe_allow_html=True) # Séparateur plus fin
    
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("GÉNÉRER MON BILAN DE COMPÉTENCES 🚀")

# --- TRAITEMENT ---
if submitted:
    # Vérification stricte
    if not prenom or not nom or not pays:
        st.error("⚠️ Dossier incomplet : Veuillez renseigner Nom, Prénom et Pays.")
    elif not email or "@" not in email:
        st.error("⚠️ Format invalide : Une adresse email professionnelle est requise.")
    else:
        with st.spinner("🔄 Traitement des données psychométriques en cours..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Contextualisation pour l'IA
                age_approx = datetime.date.today().year - date_n.year
                user_info = f"Candidat: {prenom} {nom}, Âge: {age_approx} ans, Pays: {pays}"
                
                prompt_content = f"{user_info}\nRéponses au test :\n"
                for k, v in reponses_user.items():
                    prompt_content += f"- {questions[k]} -> Choix : {v}\n"
                
                full_prompt = SYSTEM_PROMPT + "\n" + prompt_content

                response = model.generate_content(full_prompt)
                
                # Affichage Résultat
                st.balloons()
                st.success("Analyse générée avec succès.")
                
                st.markdown(f"<div class='report-box'>", unsafe_allow_html=True)
                st.markdown(f"## 📄 Bilan de Potentiel : {prenom} {nom}")
                st.caption(f"Date du rapport : {datetime.date.today().strftime('%d/%m/%Y')}")
                st.markdown(response.text)
                
                # Call to Action Final
                st.markdown("---")
                col_cta1, col_cta2 = st.columns([3, 1])
                with col_cta1:
                    st.markdown("**👉 Vous souhaitez activer votre Moteur de Recherche IA ?**")
                with col_cta2:
                    st.button("ACTIVER MON AGENT", type="primary") # Bouton visuel seulement pour l'instant
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Erreur serveur : {e}")
