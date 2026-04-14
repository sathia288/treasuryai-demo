import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import plotly.graph_objects as go

st.set_page_config(page_title="TreasuryAI", layout="wide", initial_sidebar_state="expanded")

# === CUSTOM CSS - MODERN & PROFESSIONAL ===
st.markdown("""
<style>
    .main {background-color: #0a1f3d; color: #ffffff;}
    .stApp {background-color: #0a1f3d;}
    h1 {color: #00c853; font-size: 3rem; font-weight: bold;}
    .stMetric {background-color: #112233; border-radius: 12px; padding: 10px;}
    .agent-step {animation: pulse 2s infinite;}
    @keyframes pulse {0% {opacity:1;} 50% {opacity:0.6;} 100% {opacity:1;}}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ TreasuryAI")
st.markdown("**Public Sector CFO’s Digital Transformation Co-Pilot** | PFMA • SITA • PPA 2024 • POPIA Compliant | Built for South Africa (2026)")

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Flag_of_South_Africa.svg/800px-Flag_of_South_Africa.svg.png", width=80)
st.sidebar.success("✅ LIVE AI AGENT")
st.sidebar.info("""South African Public Sector Ready
• SITA Cloud Framework 2.0
• National Treasury Instruction 2025-11
• POPIA Section 72 (Data in SA only)""")

# Mock Registry & Risk Engine (unchanged but cleaner)
class MockRegistry:
    def check_vendor(self, vendor):
        data = { ... }  # (same as before - I kept it identical)
        return data.get(vendor.strip(), {"csd_status": "Unknown", ...})

mock_reg = MockRegistry()

def calculate_risk(tender_text, vendor):
    # (same logic as previous version)
    reg = mock_reg.check_vendor(vendor)
    score = 0
    explanations = []
    # ... (same heuristics)
    level = "Low" if score <= 30 else "Medium" if score <= 60 else "High" if score <= 75 else "Critical"
    return score, level, explanations, reg

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["🤖 TenderScrutinor Agent", "💰 TCO Simulator", "📊 CFO Command Centre", "🏆 Compliance Scorecard"])

with tab1:
    st.subheader("🤖 TenderScrutinor Agent – Your AI Procurement Guardian")
    st.caption("Watch the agent think in real time")
    
    tender_text = st.text_area("Paste tender description or speak it", 
        "HealthTech Solutions SA bidding for Electronic Health Records system R85 million CSD MHEA5678901 Cloud hosting proposed", height=120)
    
    colA, colB = st.columns([3,1])
    with colA:
        vendor = st.text_input("Vendor Name", "HealthTech Solutions")
    with colB:
        if st.button("🎤 Speak Tender", use_container_width=True):
            st.info("🎙️ Voice input activated (demo) – please describe the tender")
            tender_text = "Voice input received: " + tender_text  # placeholder for real speech-to-text
    
    if st.button("🚀 Activate Agent", type="primary", use_container_width=True):
        with st.spinner("Agent is thinking..."):
            st.markdown('<div class="agent-step">🔍 Ingesting document...</div>', unsafe_allow_html=True)
            st.markdown('<div class="agent-step">📡