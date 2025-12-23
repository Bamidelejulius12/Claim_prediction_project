from overview import customer_overview
from predictions import FNOL_prediction
import streamlit as st
from visualizations import Customer_Visual
import retrain_dashboard as retrain_ui
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="FNOL Insurance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("FNOL_Data/Full_claims_data.csv")

claims_data = load_data()

# Sidebar navigation
st.sidebar.title("📊 FNOL Dashboard")
st.sidebar.markdown("---")

# Clean navigation without radio buttons
st.sidebar.subheader("Navigation")

# Navigation options as selectable items
if st.sidebar.button("🏠 Customer Claim Overview", use_container_width=True):
    st.session_state.current_page = "overview"
    
if st.sidebar.button("📈 Visualizations", use_container_width=True):
    st.session_state.current_page = "visualizations"
    
if st.sidebar.button("🔮 Prediction", use_container_width=True):
    st.session_state.current_page = "prediction"

if st.sidebar.button("⚡ Retraining", use_container_width=True):
    st.session_state.current_page = "retraining"

st.sidebar.markdown("---")
st.sidebar.info("**FNOL Insurance Analytics**  \nFirst Notice of Loss Dashboard")

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "overview"

# Main content area
if st.session_state.current_page == "overview":
    customer_overview(claims_data)
elif st.session_state.current_page == "visualizations":
    Customer_Visual(claims_data)
elif st.session_state.current_page == "prediction":
    FNOL_prediction(claims_data)
elif st.session_state.current_page == "retraining":
    retrain_ui.show_retraining_ui()  # display retraining dashboard
