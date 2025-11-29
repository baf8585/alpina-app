import streamlit as st
import google.generativeai as genai
import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="AlpinaAi | Recrutement & IA Suisse",
    page_icon="🏔️",
    layout="wide"
)

# --- CSS (DESIGN DU SITE) ---
st.markdown("""
    <style>
    /* Titres */
    h1 {color: #003366; font-family: 'Helvetica', sans-serif;}
    h2, h3 {color: #00509E;}
    
    /* Bouton Principal */
    .stButton>button {
        background-color: #D32F2F; color: white; border-radius: 5px; 
        font-weight: bold; border: none; padding: 10px 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {background-color: #B71C1C;}
    
    /* Boites d'info */
    .service-box {
        background-color: #F8F9FA; padding: 20px; border-radius: 10px;
        border-left: 5px solid #003366; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- GESTION CLÉ API ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Clé API manquante dans les secrets.")
    st.stop()

# --- SIDEBAR (NAVIGATION & SERVICES) ---
with st.sidebar:
    # GESTION DU LOGO
    # Le code va chercher 'logo.png' sur GitHub.
    try:
        st.image("logo.png", width=220) 
    except:
        # Si le logo ne s'affiche pas, on met le texte par sécurité
        st.title("🏔️ AlpinaAi")
        st.caption("Image logo.png introuvable")

    st.caption("Suisse | Innovation | Carrière")
    
    st.markdown("---")
    st.header("📌 Nos Solutions")
    
    with st.expander("🔍 Audit de Profil (Gratuit)", expanded=True):
        st.write("Le bilan IA flash pour connaître vos forces en 5 min.")
    
    with st.expander("🚀 Pack 'Essential'"):
        st.write("**Pour démarrer fort.**")
        st.write("- Revue CV par Expert + IA")
        st.write("- Optimisation LinkedIn")
        st.write("- Accès Base Talents")
        st.caption("Dès 150 CHF")
        
    with st.expander("💎 Pack 'Elite Career'"):
        st.write("**L'accompagnement total.**")
        st.write("- Coaching Interview 1-to-1")
        st.write("- Chasseur de tête dédié")
        st.write("- Négociation salariale")
        st.caption("Sur devis")

    st.markdown("---")
    st.info("📞 **Contact Entreprises**\n\nVous cherchez des talents ?\npartner@alpinaai.ch")

# --- CORPS DU SITE (MAIN) ---

# 1. HERO SECTION (L'ACCUEIL)
col_logo, col_text = st.columns([1, 3])
with col_text:
    st.title("Votre Potentiel. Toutes les Opportunités Suisses.")
    st.markdown("### Ne cherchez plus un emploi. Laissez l'IA trouver votre carrière.")
    st.markdown("""
    AlpinaAi n'est pas une agence classique. Nous utilisons **l'Intelligence Artificielle de pointe** pour décoder vos compétences et vous connecter instantanément aux entreprises suisses qui vous cherchent.
    
    ✅ **100% Gratuit pour les candidats** ✅ **Analyse psychométrique incluse** ✅ **Ouvert à tous les secteurs (Banque, Tech, Industrie, Services)**
    """)

st.markdown("---")

# 2. LE TEST (L'APPEL À L'ACTION)
st.subheader("📝 Commencez par votre Bilan de Compétences Flash")
st.write("Répondez honnêtement. Notre IA analyse votre profil en temps réel.")

# --- FORMULAIRE ET LOGIQUE ---

with st.container():
    col_form1, col_form2 = st.columns(2)
    with col_form1:
        prenom = st.text_input("Prénom")
        pays = st.text_input("Pays")
    with col_form2:
        nom = st.text_input("Nom")
        email = st.text_input("Email Pro")

    # --- QUESTIONS QCM ---
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
    
    with st.form("quiz_form"):
        # Affichage en grille
        cols = st.columns(2)
        i = 0
        for key, text in questions.items():
            with cols[i % 2]:
                st.write(f"**{text}**")
                reponses_user[key] = st.radio("Choix", options[key], label_visibility="collapsed", key=key)
                st.write("")
            i += 1
        
        st.markdown("---")
        submitted = st.form_submit_button("🚀 GÉNÉRER MON PROFIL IA")

# --- TRAITEMENT IA ---
if submitted:
    if not prenom or not email:
        st.error("Merci de remplir votre Prénom et Email pour recevoir l'analyse.")
    else:
        with st.spinner("🤖 AlpinaAi analyse vos réponses..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                user_info = f"Candidat: {prenom} {nom}, Pays: {pays}"
                prompt_content = f"{user_info}\nRéponses QCM :\n" + "\n".join([f"{k}: {v}" for k,v in reponses_user.items()])
                
                # Prompt système
                full_prompt = """
                Tu es AlpinaAi, expert carrière suisse. Analyse ce profil junior/confirmé.
                Structure ta réponse en Markdown :
                ### 💎 [Titre Profil]
                **🧠 Analyse Cognitive :** [Texte riche]
                **🤝 Impact Relationnel :** [Texte riche]
                **⚠️ Vigilance :** [Texte]
                **🇨🇭 Potentiel Suisse :** [3 secteurs justifiés]
                ---
                **🚀 OFFRE SPECIALE :** Pitch commercial court pour activer le Moteur de Recherche IA Personnalisé.
                """ + "\n" + prompt_content

                response = model.generate_content(full_prompt)
                
                st.balloons()
                st.success("Analyse terminée.")
                
                # Affichage propre du rapport
                st.markdown("""<div style="background-color: #fff; padding: 30px; border-radius: 10px; border-top: 5px solid #003366; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">""", unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Erreur : {e}")

# --- PIED DE PAGE ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <small>© 2025 AlpinaAi Switzerland. Tous droits réservés. | <a href='#'>Mentions Légales</a></small>
</div>
""", unsafe_allow_html=True)
