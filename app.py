import streamlit as st
import google.generativeai as genai
import datetime

# --- CONFIGURATION MOBILE FIRST ---
st.set_page_config(
    page_title="AlpinaAi",
    page_icon="🏔️",
    layout="centered"
)

# --- CSS (DESIGN PASTEL & CONTRASTE FORT) ---
st.markdown("""
    <style>
    /* 1. LE FOND GLOBAL (Pastel agréable) */
    .stApp {
        background-color: #F4F6F9; /* Gris-Bleu très pâle, reposant */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* 2. LE TEXTE (Force le noir/gris foncé partout) */
    h1, h2, h3, h4, h5, h6 {
        color: #003366 !important; /* Bleu Alpina pour les titres */
    }
    p, div, label, span {
        color: #1F2937 !important; /* Gris foncé pour le texte normal */
    }
    
    /* 3. LES CHAMPS DE SAISIE (Input) - Pour qu'on voie ce qu'on écrit */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important; /* Fond blanc pur */
        color: #000000 !important; /* Texte noir */
        border: 1px solid #CBD5E1; /* Bordure grise fine */
        border-radius: 8px;
    }
    
    /* 4. LES RADIOS (Choix QCM) - Pour qu'ils soient lisibles */
    div[role="radiogroup"] {
        background-color: #FFFFFF; /* Fond blanc sous les questions */
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #E5E7EB;
    }
    
    /* 5. LE BOUTON (Gros et Visible) */
    .stButton>button {
        width: 100%;
        background-color: #D32F2F; 
        color: white !important; /* Texte blanc forcé */
        font-size: 18px;
        font-weight: bold; 
        padding: 15px 0px; 
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .stButton>button:hover {background-color: #B71C1C;}
    
    /* 6. CACHER LES ÉLÉMENTS STREAMLIT INUTILES */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 7. Centrer logo et titres */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- GESTION CLÉ API ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Clé API manquante.")
    st.stop()

# --- HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", use_container_width=True) 
    except:
        st.markdown("<h1 style='text-align: center;'>🏔️ AlpinaAi</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; margin-bottom: 5px;'>Votre Potentiel. Toutes les Opportunités Suisses.</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555 !important; font-size: 14px;'>L'IA qui scanne le marché caché pour vous.</p>", unsafe_allow_html=True)

# --- SERVICES (Expanders stylés) ---
# On met un fond blanc pour que ça ressorte sur le pastel
with st.expander("📌 Voir nos Solutions & Tarifs"):
    st.markdown("""
    <div style='background-color: white; padding: 10px; border-radius: 5px;'>
    ✅ <b>Audit Flash (Gratuit)</b> : Ce que vous faites maintenant.<br>
    🚀 <b>Pack Essential (150 CHF)</b> : CV + LinkedIn + Base de Talents.<br>
    💎 <b>Pack Elite (Sur devis)</b> : Coaching + Chasseur de tête dédié.<br>
    <br>
    <small>📧 partner@alpinaai.ch</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- LE TEST ---
st.markdown("### 📝 Bilan Flash (Gratuit)")
st.write("Prenez 2 minutes. Répondez spontanément.")

with st.form("quiz_form"):
    # Champs persos
    prenom = st.text_input("Prénom")
    nom = st.text_input("Nom")
    email = st.text_input("Email Pro")
    pays = st.text_input("Pays")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Questions
    questions = {
        "Q1_Deadline": "Une deadline impossible tombe. Réaction ?",
        "Q2_Bureau": "Votre espace idéal ?",
        "Q3_Changement": "On change tous les processus. Avis ?",
        "Q4_Reunion": "Votre rôle en réunion ?",
        "Q5_Conflit": "Désaccord majeur avec un collègue ?",
        "Q6_Manager": "Le manager parfait est...",
        "Q7_Motivation": "Qu'est-ce qui vous motive le plus ?",
        "Q8_Decision": "Décider sans tout savoir ?",
        "Q9_Echec": "L'échec c'est...",
        "Q10_Structure": "Environnement préféré ?",
        "Q11_Apero": "L'afterwork commence...",
        "Q12_Reve": "Ambition ultime ?"
    }

    options = {
        "Q1_Deadline": ["Action immédiate.", "Planification détaillée.", "Mobilisation équipe.", "Négociation."],
        "Q2_Bureau": ["Créatif.", "Minimaliste.", "Organisé visuel.", "Cosy personnel."],
        "Q3_Changement": ["Enthousiaste.", "Sceptique.", "Analytique.", "Consensuel."],
        "Q4_Reunion": ["Synthèse.", "Proposition.", "Critique.", "Observation."],
        "Q5_Conflit": ["Logique/Faits.", "Compromis.", "Fermeté.", "Test A/B."],
        "Q6_Manager": ["Délégatif.", "Coach.", "Visionnaire.", "Protecteur."],
        "Q7_Motivation": ["Argent.", "Compétence.", "Sens/Mission.", "Pouvoir."],
        "Q8_Decision": ["Intuition.", "Attente données.", "Consultation.", "Scénario pire cas."],
        "Q9_Echec": ["Honte.", "Apprentissage.", "Inévitable.", "Erreur prépa."],
        "Q10_Structure": ["Multinationale.", "PME Suisse.", "Start-up.", "Indépendant."],
        "Q11_Apero": ["Réseautage.", "Poli mais bref.", "Travail d'abord.", "Organisateur."],
        "Q12_Reve": ["Expertise.", "CEO.", "Équilibre.", "Impact sociétal."]
    }

    reponses_user = {}
    
    for key, text in questions.items():
        st.write(f"**{text}**")
        reponses_user[key] = st.radio("Choix", options[key], label_visibility="collapsed", key=key)
        st.write("") 
        
    st.markdown("---")
    submitted = st.form_submit_button("🚀 ANALYSER MON PROFIL")

# --- TRAITEMENT IA ---
if submitted:
    if not prenom or not email:
        st.error("⚠️ Prénom et Email obligatoires.")
    else:
        with st.spinner("🧠 AlpinaAi réfléchit..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                user_info = f"Candidat: {prenom} {nom}, Pays: {pays}"
                prompt_content = f"{user_info}\nRéponses QCM :\n" + "\n".join([f"{k}: {v}" for k,v in reponses_user.items()])
                
                full_prompt = """
                Tu es AlpinaAi. Analyse ce profil.
                Format Markdown :
                ### 💎 [Titre Profil]
                **🧠 Analyse :** [Court et percutant]
                **🤝 Relationnel :** [Court et percutant]
                **⚠️ Vigilance :** [1 phrase]
                **🇨🇭 Secteurs Suisses :** [Liste à puces]
                ---
                **🚀 OFFRE :** Pitch court pour le Moteur de Recherche IA.
                """ + "\n" + prompt_content

                response = model.generate_content(full_prompt)
                
                st.balloons()
                
                # Boite de résultat propre (Fond blanc sur fond pastel)
                st.markdown("""<div style="background-color: #fff; padding: 25px; border-radius: 10px; border: 1px solid #ddd; border-top: 5px solid #003366; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">""", unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Erreur : {e}")

# --- FOOTER ---
st.markdown("<br><br><p style='text-align: center; color: #999 !important; font-size: 12px;'>© 2025 AlpinaAi Switzerland</p>", unsafe_allow_html=True)
