import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="TreasuryAI",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛡️"
)

# South African professional styling
st.markdown("""
<style>
    .main {background-color: #0a1f3d; color: #e0e0e0;}
    h1 {color: #00c853; font-weight: 700; font-size: 2.8rem;}
    .stButton>button {background-color: #00c853; color: #0a1f3d; font-weight: bold; border-radius: 8px;}
    .agent-card {background-color: #112233; padding: 18px; border-radius: 12px; border-left: 6px solid #00c853; margin-bottom: 10px;}
    .warning-box {background-color: #3d2b1f; padding: 12px; border-radius: 8px; border-left: 5px solid #ff9800;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ TreasuryAI")
st.markdown("**Public Sector CFO’s Multi-Agent Intelligent Digital Transformation Co-Pilot** | PFMA • SITA • PPA 2024 • POPIA | Proudly Built for South Africa (2026)")

# Sidebar with South African branding
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Flag_of_South_Africa.svg/800px-Flag_of_South_Africa.svg.png", width=130)
st.sidebar.success("🤖 MULTI-AGENT CO-PILOT ACTIVE")
st.sidebar.info("""South African Public Sector Ready
• SITA Cloud Framework 2.0 (Mandatory)
• National Treasury Instruction 2025-11
• POPIA Section 72 – Data stays in South Africa""")

st.sidebar.markdown("### Share this Demo")
st.sidebar.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://su9w.streamlit.app", width=180)

# Mock Registry (fully fixed)
class MockRegistry:
    def check_vendor(self, vendor):
        data = {
            "HealthTech Solutions": {"csd_status": "Expired", "bee_level": "Level 4", "registered_days": 120, "directors_companies": 14, "tax_clearance": False, "address_match": True},
            "Gijima Holdings": {"csd_status": "Active", "bee_level": "Level 2", "registered_days": 4000, "directors_companies": 2, "tax_clearance": True, "address_match": False},
            "Innovative Cloud Systems": {"csd_status": "Active", "bee_level": "Level 1", "registered_days": 800, "directors_companies": 12, "tax_clearance": True, "address_match": False},
        }
        return data.get(vendor.strip(), {
            "csd_status": "Unknown", 
            "bee_level": "N/A", 
            "registered_days": 0, 
            "directors_companies": 0, 
            "tax_clearance": False, 
            "address_match": False
        })

mock_reg = MockRegistry()

def calculate_risk(tender_text, vendor):
    reg = mock_reg.check_vendor(vendor)
    score = 0
    explanations = []
    if reg["csd_status"] == "Expired":
        score += 15
        explanations.append("CSD registration expired – PFMA & PPA 2024 non-compliance risk")
    if reg["registered_days"] < 180:
        score += 10
        explanations.append("Recently formed vendor (<6 months) – High fronting risk")
    if reg["directors_companies"] > 10:
        score += 15
        explanations.append("Serial director detected (CIPC data) – Potential related-party concern")
    if not reg["tax_clearance"]:
        score += 10
        explanations.append("Missing valid SARS tax clearance certificate")
    if reg["address_match"]:
        score += 15
        explanations.append("Vendor address matches director personal address – Classic fronting indicator")
    if "cloud" in tender_text.lower() and not any(x in tender_text.lower() for x in ["cape town", "johannesburg", "durban"]):
        score += 8
        explanations.append("POPIA Section 72 alert: Prefer local hosting (AWS Cape Town or Azure South Africa)")
    
    level = "Low" if score <= 30 else "Medium" if score <= 60 else "High" if score <= 75 else "Critical"
    return score, level, explanations, reg

def show_confetti():
    st.balloons()

# ====================== MULTI-AGENT TEAM ======================
st.subheader("🤖 Your Multi-Agent CFO Co-Pilot Team")
st.caption("Four specialised agents working together with full human oversight")

agent_tabs = st.tabs(["🔍 TenderScrutinor", "💰 CostOracle", "📜 Regulator", "🛡️ AuditShield"])

with agent_tabs[0]:
    st.markdown('<div class="agent-card">Analysing fraud, fronting, compliance & regulatory risks</div>', unsafe_allow_html=True)
    tender_text = st.text_area("Paste tender description", 
        "HealthTech Solutions SA bidding for Electronic Health Records system R85 million CSD MHEA5678901 Cloud hosting proposed", height=110)
    vendor = st.text_input("Vendor Name", "HealthTech Solutions")
    
    if st.button("🚀 Run TenderScrutinor Agent", type="primary"):
        with st.spinner("Agent team analysing..."):
            score, level, explanations, entities = calculate_risk(tender_text, vendor)
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={'x': [0,1], 'y': [0,1]},
                title={'text': "Risk Score"},
                gauge={'axis': {'range': [0,100]},
                       'bar': {'color': "#00c853" if score <= 60 else "#ff9800" if score <= 75 else "#f44336"},
                       'steps': [{'range': [0,30], 'color': "#00c853"}, {'range': [30,60], 'color': "#ffeb3b"}, {'range': [60,100], 'color': "#f44336"}]}))
            st.plotly_chart(fig, use_container_width=True)
            
            if score <= 30:
                show_confetti()
                st.success("✅ LOW RISK – Ready for approval")
            elif score <= 60:
                st.warning("⚠️ MEDIUM RISK – Review recommended")
            else:
                st.error("🚨 HIGH RISK – Caution advised")
            
            for exp in explanations:
                st.markdown(f"<div class='warning-box'>{exp}</div>", unsafe_allow_html=True)

with agent_tabs[1]:
    st.markdown('<div class="agent-card">Forecasting costs, TCO and MTEF alignment</div>', unsafe_allow_html=True)
    users = st.slider("Number of Users", 50, 5000, 800)
    term = st.slider("Contract Term (Years)", 1, 5, 3)
    tco = int(users * 14500 * term * 1.08)
    st.metric("5-Year TCO", f"R {tco:,.0f}", delta="-18% vs traditional")
    st.success("Recommended: SITA Transversal Contract with local cloud hosting")

with agent_tabs[2]:
    st.markdown('<div class="agent-card">Answering regulatory questions with citations</div>', unsafe_allow_html=True)
    query = st.text_input("Ask the Regulator", "Can we accept a donated AI platform?")
    if st.button("Ask Regulator"):
        st.info("✅ Possible under PFMA gift provisions, but requires Section 11 approval and full declaration. Source: PFMA & Treasury Regulations.")

with agent_tabs[3]:
    st.markdown('<div class="agent-card">Predicting audit findings and risk mitigation</div>', unsafe_allow_html=True)
    st.success("Predicted AGSA Audit Risk: 14% (based on similar provincial health tenders)")

# ====================== GENERATIVE TENDER BUILDER ======================
st.subheader("✨ Generative Compliant Tender Builder")
st.caption("Describe your need in plain English – AI generates compliant documents")
need = st.text_area("What digital solution do you need?", 
    "We need a cloud ERP system for 800 users across Gauteng Health facilities with strong analytics and local data hosting", height=100)

if st.button("🚀 Generate Compliant Tender Documents", type="primary"):
    with st.spinner("Building SITA/PPA 2024 compliant specification..."):
        st.success("✅ Generated successfully!")
        st.write("**Title:** Cloud ERP Solution for Gauteng Provincial Health – SITA Transversal Route")
        st.write("**Key Features Generated:** Local hosting (AWS Cape Town), B-BBEE Level 2 preference points, POPIA-compliant architecture")
        st.download_button("📥 Download Full RFQ + SBD Forms", "Demo content – ready for your pilot", file_name="Generated_RFQ.pdf")

# Provincial Risk Heatmap
st.subheader("🗺️ Provincial Procurement Risk Heatmap")
provinces = ["Gauteng", "Western Cape", "KwaZulu-Natal", "Limpopo", "Eastern Cape"]
risk_scores = [28, 15, 42, 68, 55]
fig = px.choropleth(locations=provinces, locationmode="country names", color=risk_scores, 
                    color_continuous_scale="RdYlGn_r", title="Procurement Risk by Province (Demo Data)")
st.plotly_chart(fig, use_container_width=True)

st.caption("TreasuryAI – Multi-Agent Co-Pilot + Generative Tender Builder • Designed for Sathia Govender, CA(SA), Johannesburg • Ready for your first pilot")
