import streamlit as st

# Require login
if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in from the main page to access this content.")
    st.stop()

st.title("🧪 Methodology & Technical Implementation")
st.markdown("---")

st.subheader("1. Design Principles")
st.markdown("""
1. **Privacy by design** — all data is pasted manually and stays local to the session  
2. **Explainability** — outputs focus on clarity, actionability, and frameworks  
3. **Safety** — restricted system prompts, no tool execution, no system access  
4. **Simplicity** — clean UI with four core analysis modules  
""")

st.subheader("2. System Architecture")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
### Application Stack
- Streamlit (UI)
- Python
- OpenAI API (LLM)
- `st.session_state` for temporary state
""")

with col2:
    st.markdown("""
### Application Structure
- `app.py` → Login + main 4-tab interface  
- `pages/About_Us.py` → Scope & goals  
- `pages/Methodology.py` → Architecture & methodology  
- `pages/Usage_Analytics.py` → Query history visualisation  
""")

st.subheader("3. Core Mechanism: Analysis Function")
st.markdown("""
The function `analyze_transformation_data(user_input, analysis_type)` handles:
- Selecting the correct **system prompt**
- Combining system + user messages  
- Sending the request to the OpenAI Chat API  
- Returning the model output  
""")

st.subheader("4. Use Case Flowcharts (Textual Representation)")

st.markdown("### Use Case 1 — Risk Detection")
st.markdown("""
1. User logs in  
2. Opens **Risk Detection** tab  
3. Inputs project updates  
4. App selects `risk_detection` system prompt  
5. Sends request to OpenAI  
6. Receives risk insights + early warning signals  
7. Displays results and logs them to session history  
""")

st.markdown("### Use Case 2 — Change Guidance")
st.markdown("""
1. User provides a transformation challenge  
2. Selects optional framework (ADKAR, Kotter, Prosci)  
3. App builds an enriched input prompt  
4. LLM returns structured best practices  
""")

st.markdown("### Use Case 3 — Team Sentiment Analysis")
st.markdown("""
1. User pastes emails or chat logs  
2. App uses `team_analysis` system prompt  
3. LLM identifies sentiment, resistance patterns, positive signals  
""")

st.markdown("### Use Case 4 — Strategic Recommendations")
st.markdown("""
1. User describes a situation  
2. User selects urgency level  
3. App appends urgency metadata  
4. LLM produces actionable strategic recommendations  
""")

st.subheader("5. Safeguards & Security")
st.markdown("""
- Login system with SHA-256 hashed passwords  
- OpenAI API key stored in Streamlit Secrets  
- No data stored on disk or external systems  
- No tool execution, file access, or code execution in prompts  
- Basic error handling for API failures, rate limits, quota issues  
""")

st.caption("This page fulfils the 'Methodology' documentation requirement.")
