import streamlit as st
import plotly.express as px
import pandas as pd
import io

st.set_page_config(page_title="Telecom PMO RAG Dashboard", layout="wide")
st.title("🛰️ Telecom PMO Project Analytics Portal")

# --- SIDEBAR: USER INPUTS ---
st.sidebar.header("🛠️ Scenario & RAG Controls")

# Document Ingestion Input
uploaded_files = st.sidebar.file_uploader(
    "Upload Project Documents (PDF/CSV)", 
    accept_multiple_files=True
)

# Text Query Input for Gemini RAG
user_query = st.sidebar.text_area(
    "Ask Gemini PMO Assistant:", 
    placeholder="e.g., What are the SLA penalty exposures for Zone B fiber delays?"
)
submit_query = st.sidebar.button("Run RAG Analysis")

# Parametric Scenario Inputs
st.sidebar.subheader("📈 Project Parameter Tuning")
material_variance_pct = st.sidebar.slider("Material Cost Variance (%)", 0.0, 30.0, 8.4)
fiber_crews = st.sidebar.number_input("Active Fiber Crews", min_value=1, max_value=50, value=14)

# --- MAIN DASHBOARD INTERFACE ---
st.markdown("### 📊 Active Operational Thresholds")
col1, col2, col3 = st.columns(3)
col1.metric("SLA Targets Met", "99.99%", "0.02%")
col2.metric("Active Fiber Crews", f"{fiber_crews} Crews", f"{fiber_crews - 16}")

# Dynamic status rendering based on user inputs
if material_variance_pct >= 10.0:
    col3.metric("Financial Variance", f"+{material_variance_pct}%", "⚠️ CRITICAL EXPOSURE", delta_color="inverse")
else:
    col3.metric("Financial Variance", f"+{material_variance_pct}%", "✓ Within Safe Threshold")

st.markdown("---")

# Mock processing data to demonstrate download actions
st.markdown("### 📋 Risk Register Context Tracking")
mock_data = pd.DataFrame({
    "Project ID": ["TEL-FIB-001", "TEL-FIB-002", "TEL-TOW-004"],
    "Task Module": ["Trenching", "Splicing", "Structural Foundation"],
    "Current SLA Status": ["On Track", "Delayed (2 Days)", "On Track"],
    "Material Cost Variance": ["+2.1%", f"+{material_variance_pct}%", "-0.5%"]
})
st.dataframe(mock_data, use_container_width=True)

# --- REPORT DOWNLOAD OPTIONS ---
st.markdown("### 📥 Export Project Analytics")

# Convert dataframe to CSV in memory for download trigger
csv_buffer = io.StringIO()
mock_data.to_csv(csv_buffer, index=False)
csv_bytes = csv_buffer.getvalue().encode('utf-8')

st.download_button(
    label="📥 Download Risk Register Summary (CSV)",
    data=csv_bytes,
    file_name="telecom_pmo_risk_report.csv",
    mime="text/csv"
)

# Handle interactive RAG response block
if submit_query and user_query:
    st.info(f"🔍 Initializing semantic lookup for query: '{user_query}'")
    st.success("🤖 Gemini Response: [RAG module execution layer connecting next...]")
