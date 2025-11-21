import streamlit as st

# Require login
if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in from the main page.")
    st.stop()

st.title("ℹ️ About Us")
st.write("This is the About Us page.")

st.set_page_config(
    page_title="About Us – Transformation Management Assistant",
    page_icon="ℹ️",
    layout="wide",
)

# Simple guard to respect your existing login flow in app.py
if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in from the main page to access this content.")
    st.stop()

st.title("ℹ️ About the Transformation Management Assistant")
st.markdown("---")

# Intro / overview
st.subheader("1. Overview")
st.markdown(
    """
The **Transformation Management Assistant** is an AI-powered prototype designed to help 
**transformation leads and change managers** monitor ongoing initiatives more effectively.

It acts as a **co-pilot for transformation and change**, focusing on:

- 🔍 Early detection of risks and weak signals  
- 👥 Understanding team sentiment and resistance patterns  
- 📋 Applying proven change management frameworks to real situations  
- 💡 Generating targeted, actionable recommendations  
"""
)

with st.expander("🎯 How this ties to the WOG Ideathon problem statements"):
    st.markdown(
        """
This prototype is aligned to Whole-of-Government (WOG) needs around:

- Making sense of **fragmented qualitative data** (emails, meeting notes, chat logs)  
- Giving non-experts access to **embedded change management expertise** on demand  
- Demonstrating a **safe, contained use of LLMs** in a government context  
"""
    )

st.markdown("---")

# Problem statement & scope
st.subheader("2. Problem Statement & Project Scope")
left, right = st.columns(2)

with left:
    st.markdown(
        """
**Common challenges in transformation programmes:**

- Risks and resistance are often surfaced **too late**  
- Insights are buried in long **email threads and meeting notes**  
- Change frameworks (ADKAR, Kotter, Prosci) are **not consistently applied**  
- Managers need **practical, context-aware advice**, not theory
"""
    )

with right:
    st.markdown(
        """
**Prototype scope (this version):**

- Focuses on **text-based i**

