import streamlit as st
import google.generativeai as genai
import datetime

# --- CONFIGURATION MOBILE FIRST ---
st.set_page_config(
    page_title="AlpinaAi",
    page_icon="🏔️",
    layout="centered" # On passe en CENTRÉ pour l'effet "App Mobile"
)

# --- CSS (DESIGN MOBILE & PROPRE) ---
st.markdown("""
    <style>
    /* Force le fond blanc et texte sombre si le config.toml n'est pas fait */
    .stApp {
        background-color: white;
        color: #003366;
    }
    
    /* Centrer le Logo et Titres */
    .css-1kyxreq, .css-1rs6os {
        justify-content: center;
        text-align: center;
    }
    
    /* Gros Bouton "Tapable" pour mobile */
    .stButton>button {
        width: 100%;
        background-color: #D32F2F; 
        color: white; 
        font-size: 18px;
        font-weight: bold; 
        padding: 15px 0px; 
        border-radius: 12px; /* Bords arrondis comme une app */
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .stButton>button:hover {background-color: #B71C1C;}
    
    /* Style des inputs pour être lisibles sur mobile */
    .stTextInput>div>div>input {
        background-color: #F8F9FA;
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    
    /* Cacher le menu hamburger par défaut de Streamlit pour faire plus "App" */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;} /* Cache la barre colorée en haut */
    
    </style>
""", unsafe_allow_html=True)

# --- GESTION CLÉ API ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Clé API manquante.")
    st.stop()

# --- HEADER (LOGO & ACCROCHE) ---
# On utilise des colonnes pour centrer l'image parfaitement
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    try:
        # Affiche le logo en grand au centre
        st.image("logo.png", use_container_width=True) 
    except:
        st.markdown("<h1 style='text-align: center;'>🏔️ AlpinaAi</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #003366;'>Votre Potentiel. Toutes les Opportunités Suisses.</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>L'IA qui scanne le marché caché pour vous.</p>", unsafe_allow_html=True)

# --- LES SERVICES (SOUS FORME D'ACCORDÉON DISCRET) ---
# On les met ici pour rassurer, mais fermés pour ne pas gêner le scroll vers le test
with st.expander("📌 Voir nos Solutions & Tarifs"):
    st.write("✅ **Audit Flash (Gratuit)** : Ce que vous faites maintenant.")
    st.write("🚀 **Pack Essential (150 CHF)** : CV + LinkedIn + Base de Talents.")
    st.write("💎 **Pack Elite (Sur devis)** : Coaching + Chasseur de tête dédié.")
    st.info("Pour les entreprises : partner@alpinaai.ch")

st.markdown("---")

# --- LE TEST (CORPS PRINCIPAL) ---
st.markdown("### 📝 Bilan Flash (Gratuit)")
st.caption("Prenez 2 minutes. Répondez spontanément.")

with st.form("quiz_form"):
    # Champs persos
    prenom = st.text_input("Prénom")
    nom = st.text_input("Nom")
    email = st.text_input("Email Pro")
    pays = st.text_input("Pays")
    
    st.markdown("---")
    
    # Questions (Format vertical pour mobile)
    # Sur mobile, on évite les colonnes pour les questions, on empile tout.
    
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
        st.write("") # Petit espace
        
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
                
                # Boite de résultat propre
                st.markdown("""<div style="background-color: #fff; padding: 20px; border-radius: 10px; border: 1px solid #ddd; border-top: 5px solid #003366;">""", unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Erreur : {e}")

# --- FOOTER ---
st.markdown("<br><br><p style='text-align: center; color: #ccc; font-size: 12px;'>© 2025 AlpinaAi Switzerland</p>", unsafe_allow_html=True)
