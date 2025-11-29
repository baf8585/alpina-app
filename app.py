import streamlit as st
import google.generativeai as genai
import os

st.title("🛠️ Radar à Modèles AlpinaAi")

# 1. Récupération de la clé
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.success("✅ Clé API trouvée.")
except:
    st.error("❌ Pas de clé configurée.")
    st.stop()

# 2. Le Scan
if st.button("SCANNER LES MODÈLES DISPONIBLES"):
    try:
        genai.configure(api_key=api_key)
        
        st.write("📡 Interrogation de Google en cours...")
        
        # On récupère la liste brute
        models_list = []
        for m in genai.list_models():
            # On cherche uniquement les modèles qui savent générer du texte
            if 'generateContent' in m.supported_generation_methods:
                models_list.append(m.name)
        
        st.write("📋 Voici la liste EXACTE des modèles disponibles pour ta clé :")
        st.code(models_list)
        
        st.info("Copie-colle cette liste à ton consultant AlpinaAi (Moi).")
        
    except Exception as e:
        st.error(f"❌ Erreur critique : {e}")
