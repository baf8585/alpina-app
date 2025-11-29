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
        background-color: #F8F9FA; /* Gris-blanc très lumineux, plus premium */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h1, h2, h3 { color: #003366 !important; font-weight: 700 !important; }
    p, div, label, span { color: #2C3E50 !important; } /* Gris anthracite profond */

    /* 2. HEADER & CARTES SERVICES (Nouveau design !) */
    .hero-title { text-align: center; margin-bottom: 10px; }
    .hero-subtitle { text-align: center; color: #666 !important; font-size: 1.1rem; margin-bottom: 30px; }
    
    /* Le conteneur des 3 cartes */
    .services-container {
        display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-bottom: 30px;
    }
    /* Le design d'une carte individuelle */
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
    .card-contact { font-size: 0.8em; color: #888; margin-top: 10px; }

    /* 3. CHAMPS DE SAISIE (Plus modernes) */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        border: 1px solid #D
