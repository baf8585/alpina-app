import streamlit as st
import google.generativeai as genai
import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AlpinaAi",
    page_icon="🏔️",
    layout="centered"
)

# --- CSS PREMIUM (LUXE & ÉPURÉ) ---
st.markdown("""
    <style>
    /* 1. FOND GLOBAL & TYPO */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h1, h2, h3 { color: #003366 !important; font-weight: 700 !important; }
    p, div, label, span { color: #2C3E50 !important; }

    /* 2. HEADER & CARTES SERVICES */
    .hero-title { text-align: center; margin-bottom: 10px; }
    .hero-subtitle { text-align: center; color: #666 !important; font-size: 1.1rem; margin-bottom: 30px; }
    
    .services-container {
        display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-bottom: 30px;
    }
    .service-card {
        background: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04); border: 1px solid #EAECEF;
        flex: 1; min-width: 200px; text-align: center;
        transition: transform 0.2s;
    }
    .service-card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
    .card-icon { font-size: 24px; margin-bottom: 10px; }
    .card-title { color: #003366; font-weight: bold; margin-bottom: 5px; }
    .card-price { color: #D32F2F; font-weight: bold; font-size: 0.9em; }

    /* 3. CHAMPS DE SAISIE */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB; border-radius: 8px; padding: 10px;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
    }
    .stTextInput>div>div>input:focus { border-color: #003366; }

    /* 4. QCM ÉPURÉ */
    .stRadio > label { font-weight: 600; font-size: 1.05em; margin-bottom: 10px; display: block; }
    div[role="radiogroup"] { background: transparent; padding: 5px; }
    hr { margin: 25px 0; border-color: #EAECEF; opacity: 0.6; }

    /* 5. BOUTON D'ACTION */
    .stButton>button {
        width: 100%; background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%);
        color: white !important; font-size: 18px; font-weight: bold;
        padding: 16px 0px; border-radius: 12px; border: none;
        box-shadow: 0 4px 10px rgba(211, 47, 47, 0.3); margin-top: 25px;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .stButton>button:hover { box-shadow: 0 6px 15px rgba(211, 47, 47, 0.4); transform: scale(1.01); }

    /* HIDE STREAMLIT UI */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 1rem; padding-bottom: 5rem; max-width: 800px; }
    </style>
""", unsafe_allow_html=True)

# --- GESTION CLÉ API ---
try: api_key = st.secrets["GOOGLE_API_KEY"]
except: st.stop()

# ================= HEADER =================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try: st.image("logo.png", use_container_width=True)
    except: st.markdown("<h1 style='text-align: center;'>🏔️ AlpinaAi</h1>", unsafe_allow_html=True)

st.markdown("<h3 class='hero-title'>Votre Potentiel. Toutes les Opportunités Suisses.</h3>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>L'Intelligence Artificielle qui scanne le marché caché pour vous.</p>", unsafe_allow_html=True)

# --- SERVICES ---
st.markdown("""
<div class="services-container">
    <div class="service-card">
        <div class="card-icon">✅</div>
        <div class="card-title">Audit Flash</div>
        <div>Bilan de compétences IA instantané.</div>
        <div class="card-price">Gratuit (Ci-dessous)</div>
    </div>
    <div class="service-card">
        <div class="card-icon">🚀</div>
        <div class="card-title">Pack Essential</div>
        <div>CV + LinkedIn + Base de Talents.</div>
        <div class="card-price">Dès 150 CHF</div>
    </div>
    <div class="service-card">
        <div class="card-icon">💎</div>
        <div class="card-title">Pack Elite</div>
        <div>Coaching + Chasseur dédié.</div>
        <div class="card-price">Sur Devis</div>
    </div>
</div>
<div style="text-align: center; font-size: 0.9em; color: #666; margin-bottom: 40px;">
    Entreprises : <a href="mailto:partner@alpinaai.ch" style="color: #003366; font-weight: bold; text-decoration: none;">partner@alpinaai.ch</a>
</div>
""", unsafe_allow_html=True)


# ================= LE TEST =================
st.markdown("### 📝 Commencez votre Bilan Flash (Gratuit)")
st.write("Prenez 2 minutes. Répondez spontanément pour une analyse précise.")
st.markdown("<br>", unsafe_allow_html=True)

with st.form("quiz_form"):
    prenom = st.text_input("Prénom")
    nom = st.text_input("Nom")
    email = st.text_input("Email Professionnel")
    pays = st.text_input("Pays de résidence actuel")
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    questions = {
        "Q1_Deadline": "Une deadline impossible tombe. Réaction ?",
        "Q2_Bureau": "Votre espace de travail idéal ?",
        "Q3_Changement": "On change tous les processus. Votre avis ?",
        "Q4_Reunion": "Votre rôle dominant en réunion ?",
        "Q5_Conflit": "Désaccord majeur avec un collègue ?",
        "Q6_Manager": "Le manager parfait est...",
        "Q7_Motivation": "Votre moteur principal actuel ?",
        "Q8_Decision": "Décider sans avoir toutes les infos ?",
        "Q9_Echec": "Votre définition de l'échec ?",
        "Q10_Structure": "Environnement d'entreprise préféré ?",
        "Q11_Apero": "L'afterwork commence...",
        "Q12_Reve": "Ambition ultime de carrière ?"
    }

    options = {
        "Q1_Deadline": ["Action immédiate (Positif).", "Planification détaillée d'abord.", "Mobilisation de l'équipe.", "Négociation du délai/périmètre."],
        "Q2_Bureau": ["Créatif et foisonnant.", "Minimaliste et ultra-rangé.", "Organisé avec supports visuels.", "Cosy et personnalisé."],
        "Q3_Changement": ["Enthousiaste (Opportunité).", "Sceptique (Besoin de preuves).", "Analytique (Calcul du ROI).", "Consensuel (Suivre l'équipe)."],
        "Q4_Reunion": ["Synthèse et écoute.", "Force de proposition.", "Challenge et critique.", "Observation et analyse."],
        "Q5_Conflit": ["Basé sur la logique/faits.", "Recherche du compromis.", "Fermeté sur ma position.", "Test A/B (Pragmatisme)."],
        "Q6_Manager": ["Délégatif (Laissez-moi faire).", "Coach (Feedback constant).", "Visionnaire (Inspirant).", "Protecteur (Bienveillant)."],
        "Q7_Motivation": ["Rémunération / Argent.", "Montée en compétence technique.", "Sens / Mission sociétale.", "Pouvoir / Management."],
        "Q8_Decision": ["Je tranche à l'intuition.", "J'attends plus de données.", "Je consulte des experts.", "Je fais un scénario 'Pire Cas'."],
        "Q9_Echec": ["Une honte à éviter.", "Une opportunité d'apprentissage.", "Inévitable pour innover.", "Un défaut de préparation."],
        "Q10_Structure": ["Grande Multinationale.", "PME Suisse stable.", "Start-up agile.", "Indépendant / Freelance."],
        "Q11_Apero": ["Réseautage actif.", "Poli mais départ rapide.", "Priorité au travail d'abord.", "C'est moi l'organisateur !"],
        "Q12_Reve": ["Expertise technique reconnue.", "CEO / Entrepreneur.", "Équilibre Vie Pro/Perso parfait.", "Impact sociétal majeur."]
    }

    reponses_user = {}
    
    for key, text in questions.items():
        st.write(f"**{text}**")
        reponses_user[key] = st.radio("Choix", options[key], label_visibility="collapsed", key=key)
        st.markdown("<hr>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("GÉNÉRER MON PROFIL IA 🚀")

# --- TRAITEMENT IA ---
if submitted:
    if not prenom or not email:
        st.warning("⚠️ Veuillez remplir au minimum votre Prénom et votre Email pour recevoir l'analyse.")
    else:
        with st.spinner("🧠 Connexion aux neurones d'AlpinaAi... Analyse en cours..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                user_info = f"Candidat: {prenom} {nom}, Pays: {pays}"
                prompt_content = f"{user_info}\nRéponses QCM :\n" + "\n".join([f"{k}: {v}" for k,v in reponses_user.items()])
                
                full_prompt = """
                Tu es AlpinaAi, consultant expert carrière suisse. Analyse ce profil avec précision et bienveillance.
                Format Markdown strict :
                ### 💎 [Titre de Profil Valorisant]
                **🧠 Analyse Cognitive & Soft-Skills :** [Paragraphe dense et expert]
                **🤝 Dynamique Relationnelle :** [Paragraphe dense et expert]
                **⚠️ Point de Vigilance :** [Une phrase constructive]
                **🇨🇭 Potentiel Marché Suisse :** [Liste à puces de 3 secteurs/métiers justifiés]
                ---
                **🚀 OFFRE EXCLUSIVE :** Pitch commercial court et percutant (3 lignes max) incitant à activer le Moteur de Recherche IA Personnalisé Alpina pour accéder au marché caché.
                """ + "\n" + prompt_content

                response = model.generate_content(full_prompt)
                
                st.balloons()
                st.success("Analyse terminée avec succès.")
                
                st.markdown("""<div style="background-color: #fff; padding: 40px; border-radius: 12px; border: 1px solid #EAECEF; border-top: 6px solid #003366; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">""", unsafe_allow_html=True)
                st.markdown(f"## Bilan de Potentiel : {prenom}")
                st.caption(f"Généré par l'IA Alpina le {datetime.date.today().strftime('%d/%m/%Y')}")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Une erreur technique est survenue : {e}")

# --- FOOTER ---
st.markdown("<br><br><p style='text-align: center; color: #aaa !important; font-size: 11px; letter-spacing: 1px;'>© 2025 ALPINAAI SWITZERLAND | HIGH-END TALENT INTELLIGENCE</p>", unsafe_allow_html=True)
