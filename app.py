import streamlit as st
import plotly.express as px
import pandas as pd
from pydantic import BaseModel, Field
from typing import List
import io

st.set_page_config(page_title="Telecom PMO RAG Dashboard", layout="wide")
st.title("🛰️ Telecom PMO Project Analytics Portal")

# --- DATA STRUCTURE FOR ACADEMIC EVALUATION (Pydantic Model) ---
class RiskItem(BaseModel):
    risk_id: str = Field(description="Unique code like TEL-RSK-XXX")
    risk_source: str = Field(description="The core cause from the scenario")
    impact_area: str = Field(description="SLA Delay, Material Cost, or Operational Capacity")
    severity: str = Field(description="Low, Medium, High, or Critical")
    mitigation_strategy: str = Field(description="Actionable PMO recommendation")

class RiskRegister(BaseModel):
    risks: List[RiskItem]

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🛠️ Scenario & RAG Controls")

uploaded_files = st.sidebar.file_uploader(
    "Upload Project Documents (PDF/CSV/BoQ)", 
    accept_multiple_files=True
)

st.sidebar.subheader("🔮 Run Predictive Scenarios")
scenario_text = st.sidebar.text_area(
    "Describe a project incident / scenario:", 
    placeholder="e.g., Extreme monsoons in the Western Province are halting fiber trenching for 14 days, causing crew availability to drop.",
    height=120
)
generate_risk = st.sidebar.button("⚡ Generate Risk Registry Table")

# Baseline Parameter Sliders
st.sidebar.subheader("📈 Manual KPI Tuning")
material_variance_pct = st.sidebar.slider("Material Cost Variance (%)", 0.0, 30.0, 8.4)
fiber_crews = st.sidebar.number_input("Active Fiber Crews", min_value=1, max_value=50, value=14)

# --- MAIN DASHBOARD INTERFACE ---
st.markdown("### 📊 Active Operational Thresholds")
col1, col2, col3 = st.columns(3)
col1.metric("SLA Targets Met", "99.99%", "0.02%")
col2.metric("Active Fiber Crews", f"{fiber_crews} Crews", f"{fiber_crews - 16}")
col3.metric("Financial Variance", f"+{material_variance_pct}%", "Critical Threshold < 10%" if material_variance_pct < 10 else "⚠️ CRITICAL EXPOSURE")

st.markdown("---")

# Initialize persistent session state for the generated risk registry
if "dynamic_risks" not in st.session_state:
    st.session_state.dynamic_risks = pd.DataFrame([
        {"Risk ID": "TEL-RSK-001", "Risk Source": "Baseline tracking operational data", "Impact Area": "SLA Delay", "Severity": "Low", "Mitigation Strategy": "Monitor weekly progress updates."}
    ])

# --- SCENARIO TO RISK REGISTRY ENGINE ---
if generate_risk and scenario_text:
    st.info("🤖 Processing scenario text via structured JSON generation layers...")
    
    # Simulating the structured output model mapping returned by Gemini
    # In the next step we connect the live google-genai client parsing this exact scheme
    mock_gemini_structured_output = [
        {
            "Risk ID": "TEL-RSK-102",
            "Risk Source": "Weather disruptions (Monsoons)",
            "Impact Area": "SLA Delay",
            "Severity": "High",
            "Mitigation Strategy": "Activate secondary contract window extensions under Force Majeure clause."
        },
        {
            "Risk ID": "TEL-RSK-103",
            "Risk Source": "Crew capacity constraints",
            "Impact Area": "Operational Capacity",
            "Severity": "Medium",
            "Mitigation Strategy": "Reallocate fiber splicing crews from Zone C to minimize project timeline slippage."
        }
    ]
    
    # Append generated data back into runtime presentation layer
    st.session_state.dynamic_risks = pd.DataFrame(mock_gemini_structured_output)
    st.success("✅ Dynamic Risk Registry updated from scenario context!")

st.markdown("### 📋 Dynamic Risk Register Tracking Matrix")
st.dataframe(st.session_state.dynamic_risks, use_container_width=True)

# --- REPORT DOWNLOAD OPTIONS ---
csv_buffer = io.StringIO()
st.session_state.dynamic_risks.to_csv(csv_buffer, index=False)
csv_bytes = csv_buffer.getvalue().encode('utf-8')

st.download_button(
    label="📥 Export Generated Risk Report (CSV)",
    data=csv_bytes,
    file_name="telecom_dynamic_pmo_report.csv",
    mime="text/csv"
)
