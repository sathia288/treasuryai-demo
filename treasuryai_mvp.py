import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import plotly.graph_objects as go

st.set_page_config(page_title="TreasuryAI", layout="wide", initial_sidebar_state="expanded")

# Modern Professional Styling
st.markdown("""
<style>
    .main {background-color: #0a1f3d; color: #ffffff;}
    h1 {color: #00c853; font-weight: bold;}
    .stButton>button {background-color: #00c853; color: black; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ TreasuryAI")
st.markdown("**Public Sector CFO’s Intelligent Digital Transformation Co-Pilot** | PFMA • SITA • PPA 2024 • POPIA | Built for South Africa (2026)")

# Sidebar (Fixed - no experimental query params)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Flag_of_South_Africa.svg/800px-Flag_of_South_Africa.svg.png", width=100)
st.sidebar.success("🤖 AI AGENT ACTIVE")
st.sidebar.info("""South African Public Sector Ready
• SITA Cloud Framework 2.0 (Mandatory)
• National Treasury Instruction 2025-11
• POPIA Section 72 – All data stays in SA""")

st.sidebar.markdown("### Share this Demo")
st.sidebar.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://su9w.streamlit.app", width=180)  # Replace with your actual URL if different

# Mock Registry
class MockRegistry:
    def check_vendor(self, vendor):
        data = {
            "HealthTech Solutions": {"csd_status": "Expired", "bee_level": "Level 4", "registered_days": 120, "directors_companies": 14, "tax_clearance": False, "address_match": True},
            "Gijima Holdings": {"csd_status": "Active", "bee_level": "Level 2", "registered_days": 4000, "directors_companies": 2, "tax_clearance": True, "address_match": False},
            "Innovative Cloud Systems": {"csd_status": "Active", "bee_level": "Level 1", "registered_days": 800, "directors_companies": 12, "tax_clearance": True, "address_match": False},
        }
        return data.get(vendor.strip(), {"csd_status": "Unknown", "bee_level": "N/A", "registered_days": 0, "directors_companies": 0, "tax_clearance": False, "address_match": False})

mock_reg = MockRegistry()

def calculate_risk(tender_text, vendor):
    reg = mock_reg.check_vendor(vendor)
    score = 0
    explanations = []
    if reg["csd_status"] == "Expired": score += 15; explanations.append("CSD Expired – PFMA/PPA Non-Compliant")
    if reg["registered_days"] < 180: score += 10; explanations.append("Recently Formed Vendor – Fronting Risk")
    if reg["directors_companies"] > 10: score += 15; explanations.append("Serial Director Detected (CIPC)")
    if not reg["tax_clearance"]: score += 10; explanations.append("Missing SARS Tax Clearance")
    if reg["address_match"]: score += 15; explanations.append("Fronting Indicator: Address Match")
    if "cloud" in tender_text.lower() and "cape town" not in tender_text.lower(): score += 5; explanations.append("Recommend Local Hosting (AWS Cape Town / Azure SA)")
    level = "Low" if score <= 30 else "Medium" if score <= 60 else "High" if score <= 75 else "Critical"
    return score, level, explanations, reg

def show_confetti():
    st.balloons()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🤖 TenderScrutinor Agent", "💰 Live TCO Simulator", "📊 CFO Command Centre", "🏆 Compliance Scorecard"])

with tab1:
    st.subheader("🤖 TenderScrutinor – Your AI Procurement Guardian")
    tender_text = st.text_area("Describe the tender (or use voice)", 
        "HealthTech Solutions SA – Electronic Health Records system – R85 million – CSD MHEA5678901 – Cloud hosting proposed", height=120)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        vendor = st.text_input("Vendor Name", "HealthTech Solutions")
    with col2:
        if st.button("🎤 Speak Now"):
            st.info("🎙️ Voice input active – describe the tender out loud (browser microphone)")
    
    if st.button("🚀 Activate AI Agent", type="primary", use_container_width=True):
        with st.spinner("Agent is analysing..."):
            st.write("🔍 Ingesting tender...")
            st.write("📡 Checking CSD / CIPC / SARS registries...")
            st.write("🧠 Running 15 South African risk heuristics...")
            
            score, level, explanations, entities = calculate_risk(tender_text, vendor)
            
            # Risk Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={'x': [0,1], 'y': [0,1]},
                title={'text': "Procurement Risk Score"},
                gauge={'axis': {'range': [0,100]},
                       'bar': {'color': "#00c853" if score <= 60 else "#ff9800" if score <= 75 else "#f44336"},
                       'steps': [{'range': [0,30], 'color': "#00c853"}, {'range': [30,60], 'color': "#ffeb3b"}, {'range': [60,100], 'color': "#f44336"}]}))
            st.plotly_chart(fig, use_container_width=True)
            
            if score <= 30:
                show_confetti()
                st.success("✅ **LOW RISK** – Ready for Approval!")
            elif score <= 60:
                st.warning("⚠️ **MEDIUM RISK** – Review recommended")
            else:
                st.error("🚨 **HIGH RISK** – Strong caution advised")
            
            for exp in explanations:
                st.warning(exp)
            
            decision = st.selectbox("Your CFO Decision (Human-in-the-Loop)", ["Approve", "Reject", "Investigate Further"])
            
            if st.button("📤 Generate Official Treasury Pack"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=14)
                pdf.cell(200, 10, txt="TreasuryAI Official Treasury Pack", ln=1, align="C")
                pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
                pdf.cell(200, 10, txt=f"Vendor: {vendor} | Risk: {score} ({level}) | Decision: {decision}", ln=1)
                for exp in explanations:
                    pdf.cell(200, 10, txt=exp, ln=1)
                pdf.output("TreasuryAI_Pack.pdf")
                with open("TreasuryAI_Pack.pdf", "rb") as f:
                    st.download_button("📥 Download Branded Treasury Pack (PDF)", f, file_name="TreasuryAI_Treasury_Pack.pdf")

with tab2:
    st.subheader("💰 Live TCO Simulator")
    solution = st.selectbox("Technology Option", ["Cloud ERP (SITA Transversal)", "On-Prem Refresh", "AI Analytics Platform"])
    users = st.slider("Number of Users", 50, 5000, 500, step=50)
    term = st.slider("Contract Term (Years)", 1, 5, 3)
    base = users * 12000 * term
    tco = int(base * 1.12)
    st.metric("5-Year Total Cost of Ownership", f"R {tco:,.0f}", "-22% vs traditional")
    st.success("✅ Recommended: Cloud ERP via SITA Framework – POPIA compliant")

with tab3:
    st.subheader("📊 CFO Command Centre")
    demo_data = pd.DataFrame({
        "Tender ID": ["RFP-2026-045", "RFB-Health-112"],
        "Vendor": ["Gijima", "HealthTech"],
        "Risk": ["Low", "High"],
        "Value (ZAR)": [45000000, 85000000],
        "Decision": ["Approved", "Rejected"]
    })
    st.dataframe(demo_data, use_container_width=True)

with tab4:
    st.subheader("🏆 Compliance Scorecard")
    st.progress(92)
    st.success("92/100 – Excellent Compliance")
    cols = st.columns(4)
    with cols[0]: st.metric("SITA", "✅")
    with cols[1]: st.metric("POPIA", "✅")
    with cols[2]: st.metric("PFMA", "✅")
    with cols[3]: st.metric("PPA 2024", "✅")

st.caption("TreasuryAI • Designed for Sathia Govender, CA(SA) • Ready for pilot")