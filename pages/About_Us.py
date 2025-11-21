import streamlit as st

# Require login
if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in from the main page to access this content.")
    st.stop()

st.title("ℹ️ About the Transformation Management Assistant")
st.markdown("---")

st.subheader("1. Project Overview")
st.markdown("""
The **Transformation Management Assistant** is an AI-powered prototype designed to help
public-sector transformation teams detect risks early, understand team sentiment, and
apply proven change management frameworks during ongoing transformation programmes.
""")

st.subheader("2. Problem Statement & Motivation")
st.markdown("""
Many transformation efforts face:
- Important signals buried within emails or meeting notes  
- Inconsistent use of change management frameworks, leading to delayed detection of risks and resistance  
- Difficulty synthesising qualitative insights due to volume of work  

This tool provides structure, early warning signals, and actionable change management insights.
""")

st.subheader("3. Objectives")
st.markdown("""
- Identify weak signals and potential risks **2–3 weeks early**  
- Analyse team sentiment and communication patterns 
- Help transformation leads make faster, grounded decisions  
- Demonstrate a safe LLM-supported application aligned to WOG requirements  
""")

st.subheader("4. Target Users")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
**Primary Users**
- Transformation leads  
- PMO / project managers  
- HR / change management partners  
- Innovation teams  
""")

with col2:
    st.markdown("""
**Key Features**
- 🔍 Risk Detection  
- 📋 Change Management Guidance  
- 👥 Team Analysis  
- 💡 Strategic Recommendations  
- 📜 Per-Session History  
""")

st.subheader("5. Data Sources & Privacy")
st.markdown("""
**Data used:**
- User-pasted project updates  
- Meeting notes  
- Emails or chat excerpts  
- Descriptions of challenges  

**Not used:**
- No agency databases  
- No ERP/HR systems  
- No personal data scraping  
- No permanent storage  

All data lives only inside the current **Streamlit session memory**.
""")

st.caption("This page fulfils the 'About Us' documentation requirement.")

