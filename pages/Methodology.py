import streamlit as st

st.set_page_config(
    page_title="Methodology – Transformation Management Assistant",
    page_icon="🧪",
    layout="wide",
)

# Guard: respect login from main app
if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in from the main page to access this content.")
    st.stop()

st.title("🧪 Methodology & Technical Approach")
st.markdown("---")

st.subheader("1. Design Principles")
st.markdown(
    """
The Transformation Management Assistant is built around four principles:

1. **Privacy by design** – Only user-pasted text is processed in this prototype.  
2. **Low friction** – A simple, tab-based interface for different analysis types.  
3. **Explainability** – Outputs are plain-language narratives mapped to known frameworks.  
4. **Safety & guardrails** – Limited action surface (analysis-only), secure key handling, and scoped prompts.  
"""
)

st.markdown("---")

# Architecture & stack
st.subheader("2. System Architecture (High-Level)")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
**Technology Stack**

- 🐍 **Python** as the core language  
- 📊 **Streamlit** for the web UI and session management  
- 🤖 **OpenAI** Python SDK for LLM access  
- 🔑 **Streamlit Secrets** (`secrets.toml`) for `OPENAI_API_KEY`  
- 🧠 `st.session_state` for:
  - Authentication flag  
  - Logged-in username  
  - Per-session analysis history  
"""
    )

with col2:
    st.markdown(
        """
**Key Components**

- `app.py`  
  - Login and authentication  
  - Main analysis interface with four tabs  
- `pages/01_About_Us.py`  
  - Project scope, objectives, data sources, and features  
- `pages/02_Methodology.py`  
  - Data flows, implementation details, and use case flowcharts  
"""
    )

st.markdown("#### High-Level Request Flow")
st.code(
    """
[User Browser] → [Streamlit App] → [OpenAI API] → [Streamlit App] → [User Browser]
    """,
    language="text",
)

st.markdown("---")

# Prompt design
st.subheader("3. Prompt Design & Lightweight Prompt Chaining")

st.markdown(
    """
The core logic sits in a single helper function: `analyze_transformation_data(user_input, analysis_type)`.

Each **analysis type** maps to a **specialised system prompt**:

- `risk_detection` → transformation risk expert  
- `change_guidance` → change management consultant  
- `team_analysis` → team dynamics and sentiment analyst  
- `recommendations` → strategic transformation advisor  

For every user request:

1. The app selects the appropriate **system prompt** based on the active tab.  
2. The user’s text input (and optional parameters like framework or urgency) are appended.  
3. The combined prompt is sent to the **Chat Completions API** (`client.chat.completions.create`).  
4. The response is parsed and displayed, and stored in **`chat_history`** in `st.session_state`.  

This approach is a lightweight form of **prompt chaining / orchestration**: user choices (tab, framework, urgency) steer the model behaviour without exposing agents or tools.
"""
)

st.markdown("---")

# Use Case 1 – Risk Detection flowchart
st.subheader("4. Use Case 1 – Risk Detection & Early Warning (Flowchart)")

st.markdown("**Objective:** Help transformation leads detect risks ~2–3 weeks early from qualitative project updates.")

st.markdown("##### Textual Flowchart (for Slide 13–15 Style Diagrams)")

st.markdown(
    """
**Actors:**  
- 👤 *User*  
- 🖥️ *Streamlit App*  
- 🤖 *LLM (OpenAI)*  

**Step-by-step Flow:**

1. **User Login**  
   - User logs in on `app.py` using a username/password.  
   - On success, `st.session_state.authenticated = True`.

2. **Select Use Case**  
   - User clicks on the **“🔍 Risk Detection”** tab.

3. **Provide Input**  
   - User pastes project status updates, meeting summaries, or email snippets into the text area.

4. **Validation (Streamlit App)**  
   - Check that:
     - Input text is not empty  
     - `OPENAI_API_KEY` is available in `st.secrets`  

5. **Prompt Construction (Streamlit App)**  
   - Select the `risk_detection` system prompt:
     - Role: “transformation management expert specializing in risk detection”  
     - Instruction: look for risks, early warnings, and patterns  
   - Combine system prompt + user input.

6. **LLM Request (Streamlit App → OpenAI)**  
   - Call `client.chat.completions.create(model="gpt-4", ...)`.

7. **Model Processing (LLM)**  
   - The model analyses the text and returns:
     - Key risks and weak signals  
     - Possible root causes  
     - Suggested mitigation actions  

8. **Response Handling (Streamlit App)**  
   - Extract the text response.  
   - Append to `st.session_state.chat_history` with:
     - Timestamp  
     - Analysis type (“Risk Detection”)  
     - Input (truncated)  
     - Output (full).

9. **Display to User**  
   - Show under **“🎯 Risk Analysis Results”** with clear headings or bullet points.

10. **Error Handling**  
    - If rate limits / quota / invalid key issues occur, show friendly messages like:
      - “⚠️ Rate limit exceeded…”  
      - “⚠️ Insufficient API credits…”  
"""
)

st.markdown("---")

# Use Case 2 – Team Dynamics & Change Guidance flowchart
st.subheader("5. Use Case 2 – Team Dynamics & Change Guidance (Flowchart)")

tab_team, tab_change = st.tabs(["👥 Team Communication Analysis", "📋 Change Management Guidance"])

with tab_team:
    st.markdown("**Objective:** Understand team sentiment, resistance, and collaboration patterns from communications.")
    st.markdown(
        """
**Actors:**  
- 👤 *User*  
- 🖥️ *Streamlit App*  
- 🤖 *LLM (OpenAI)*  

**Flow Steps:**

1. User logs in and selects the **“👥 Team Analysis”** tab.  
2. User pastes emails, chat logs, or retrospective notes into the text area.  
3. App validates that:
   - Input is present  
   - API key is configured  

4. App selects the `team_analysis` system prompt:
   - Focus on sentiment, engagement, resistance, and collaboration.  

5. App calls the Chat Completions API with system + user messages.  
6. LLM returns analysis:
   - Overall sentiment  
   - Positive signals  
   - Areas of concern / resistance themes  
7. App displays the output as “👥 Team Dynamics Insights” and stores it in `chat_history`.  
"""
    )

with tab_change:
    st.markdown("**Objective:** Translate people challenges into practical, framework-based actions.")
    st.markdown(
        """
**Actors:**  
- 👤 *User*  
- 🖥️ *Streamlit App*  
- 🤖 *LLM (OpenAI)*  

**Flow Steps:**

1. User logs in and selects the **“📋 Change Guidance”** tab.  
2. User describes the change challenge (e.g. low adoption, resistant managers).  
3. User optionally chooses a **preferred framework**:
   - Auto-select, ADKAR, Kotter’s 8-Step, Prosci, McKinsey 7-S.  

4. App constructs the input:
   - Base system prompt: `change_guidance`.  
   - If a framework is selected, append  
     `"Preferred framework: <framework>"` to the user message.  

5. App sends the combined prompt to the LLM via the Chat Completions API.  
6. LLM returns:
   - Short diagnosis (e.g. which dimensions are weak)  
   - Actionable recommendations aligned to the chosen framework.  

7. App displays the output under **“📚 Best Practice Guidance”** and stores it in `chat_history`.  
"""
    )

st.markdown("---")

# Safeguards & prompt injection
st.subheader("6. Safeguards, Prompt Injection & Risk Management")

st.markdown(
    """
Although this is a prototype, several safeguards are already applied:

1. **Login & Access Control**  
   - Access requires username/password; credentials are s
