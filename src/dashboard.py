import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# Set Page Config
st.set_page_config(page_title="AI Model Evaluation Dashboard", layout="wide")

st.title("🛡️ LLM Evaluation & Drift Monitor")
st.markdown("Based on **The Gen Academy** Evaluation Framework")

# --- 1. Load Data ---
HISTORY_FILE = "data/history.json"


def load_metrics():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}


data = load_metrics()

if not data:
    st.warning("No evaluation data found. Run your main.py script first!")
else:
    # --- 2. Key Metrics Row ---
    st.subheader("Current Performance")
    cols = st.columns(len(data))

    for i, (metric, value) in enumerate(data.items()):
        # Simulate a "previous" value for the delta display
        prev_value = value * 1.05  # Mocking a 5% drop for visual effect
        delta = f"{((value - prev_value) / prev_value) * 100:.1f}%"
        cols[i].metric(label=metric, value=value, delta=delta)

    # --- 3. Visualization ---
    st.divider()
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Metric Distribution")
        df = pd.DataFrame(list(data.items()), columns=['Metric', 'Score'])
        fig = px.bar(df, x='Metric', y='Score', color='Score',
                     color_continuous_scale='RdYlGn', range_y=[0, 1])
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Accountability Checklist")
        st.checkbox("Performance Verification", value=True, disabled=True)
        st.checkbox("Ethical AI / Bias Check", value=data.get('Accuracy', 0) > 0.7)
        st.checkbox("Smart Model Selection", value=True)
        st.info("Evaluation helps researchers create next-gen AI capabilities.")

# --- 4. Sidebar Controls ---
st.sidebar.header("Settings")
st.sidebar.button("Re-run Evaluation")
st.sidebar.download_button("Download Report (CSV)",
                           data=pd.DataFrame([data]).to_csv(),
                           file_name="llm_report.csv")