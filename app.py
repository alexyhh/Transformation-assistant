import streamlit as st
from openai import OpenAI
from datetime import datetime
import json
import hashlib

# Page configuration
st.set_page_config(
    page_title="Transformation Assistant",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication credentials (in production, use environment variables or secure storage)
VALID_CREDENTIALS = {
    "admin": hashlib.sha256("transform2024".encode()).hexdigest(),
    "manager": hashlib.sha256("change2024".encode()).hexdigest()
}

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize API key from secrets (automatic, secure)
if 'openai_api_key' not in st.session_state:
    try:
        st.session_state.openai_api_key = st.secrets["OPENAI_API_KEY"]
    except:
        st.session_state.openai_api_key = None

def authenticate(username, password):
    """Authenticate user credentials"""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return VALID_CREDENTIALS.get(username) == hashed_password

def login_page():
    """Display login page"""
    st.title("🔄 Transformation Management Assistant")
    st.markdown("### Secure Access Portal")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("#### Login to Continue")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Login", use_container_width=True):
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
        
        with col_b:
            if st.button("Clear", use_container_width=True):
                st.rerun()
        
        st.markdown("---")
        st.info("**Demo Credentials:**\n\nUsername: `admin` | Password: `transform2024`\n\nUsername: `manager` | Password: `change2024`")

def get_openai_client():
    """Get OpenAI client instance"""
    if st.session_state.openai_api_key:
        try:
            return OpenAI(api_key=st.session_state.openai_api_key)
        except Exception as e:
            st.error(f"Error initializing OpenAI client: {str(e)}")
            return None
    return None

def analyze_transformation_data(user_input, analysis_type):
    """Analyze transformation data using OpenAI"""
    client = get_openai_client()
    if not client:
        return "Please configure your OpenAI API key in Streamlit Cloud secrets."
    
    system_prompts = {
        "risk_detection": """You are a transformation management expert specializing in risk detection. 
        Analyze the provided information for early warning signs of resistance, delays, or issues. 
        Identify patterns that might indicate problems 2-3 weeks ahead. Provide specific, actionable insights.""",
        
        "change_guidance": """You are a change management consultant providing practical guidance. 
        Based on the situation described, provide contextually relevant best practices from proven frameworks 
        like ADKAR, Kotter's 8-Step Process, or Prosci methodology. Be specific and actionable.""",
        
        "team_analysis": """You are analyzing team communications and sentiment. 
        Identify resistance patterns, engagement levels, and collaboration issues. 
        Highlight both positive indicators and areas of concern.""",
        
        "recommendations": """You are providing strategic recommendations for transformation success. 
        Based on the current situation, suggest targeted interventions, timeline adjustments, 
        and stakeholder management strategies."""
    }
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompts.get(analysis_type, system_prompts["risk_detection"])},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower():
            return "⚠️ Rate limit exceeded. Please wait a moment and try again."
        elif "insufficient_quota" in error_msg.lower():
            return "⚠️ Insufficient API credits. Please check your OpenAI account balance."
        elif "invalid_api_key" in error_msg.lower():
            return "⚠️ Invalid API key. Please check your OpenAI API key in Streamlit secrets."
        else:
            return f"⚠️ Error: {error_msg}\n\nPlease check your API key and ensure you have sufficient credits."

def main_app():
    """Main application interface"""
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # API Key Status Display (No manual entry needed)
        st.markdown("### 🔑 API Status")
        if st.session_state.openai_api_key:
            st.success("✅ OpenAI Connected")
            st.caption("Securely configured via secrets")
        else:
            st.error("❌ API Key Missing")
            st.caption("Configure in Streamlit Cloud secrets")
            with st.expander("ℹ️ Setup Instructions"):
                st.markdown("""
                **Streamlit Cloud:**
                1. Go to app Settings → Secrets
                2. Add: `OPENAI_API_KEY = "sk-..."`
                
                **Local Development:**
                1. Create `.streamlit/secrets.toml`
                2. Add: `OPENAI_API_KEY = "sk-..."`
                """)
        
        st.markdown("---")
        
        # User info
        st.markdown(f"**Logged in as:** {st.session_state.username}")
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        st.metric("Analysis Count", len(st.session_state.chat_history))
        st.metric("Session Duration", f"{(datetime.now().hour - 9) % 12}h")
        
        st.markdown("---")
        
        # Clear history
        if st.button("Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main content
    st.title("🔄 Transformation Management Assistant")
    st.markdown("**Real-time transformation monitoring and change management guidance**")
    st.markdown("---")
    
    # Tabs for different functions
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Risk Detection",
        "📋 Change Guidance",
        "👥 Team Analysis",
        "💡 Recommendations"
    ])
    
    with tab1:
        st.header("Risk Detection & Early Warning")
        st.markdown("Identify transformation risks 2-3 weeks early through pattern analysis")
        
        risk_input = st.text_area(
            "Describe the current project status, recent communications, or concerns:",
            height=150,
            placeholder="E.g., Team meeting notes, email summaries, project updates..."
        )
        
        if st.button("Analyze Risks", key="risk_btn"):
            if risk_input and st.session_state.openai_api_key:
                with st.spinner("Analyzing for risk patterns..."):
                    result = analyze_transformation_data(risk_input, "risk_detection")
                    st.session_state.chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "type": "Risk Detection",
                        "input": risk_input,
                        "output": result
                    })
                    st.success("Analysis Complete!")
                    st.markdown("### 🎯 Risk Analysis Results")
                    st.markdown(result)
            elif not st.session_state.openai_api_key:
                st.error("Please configure your OpenAI API key in the sidebar.")
            else:
                st.warning("Please provide input for analysis.")
    
    with tab2:
        st.header("Change Management Guidance")
        st.markdown("Get contextually relevant best practices from proven frameworks")
        
        guidance_input = st.text_area(
            "Describe the change management challenge:",
            height=150,
            placeholder="E.g., Resistance from middle management, low adoption rates, communication gaps..."
        )
        
        framework = st.selectbox(
            "Preferred Framework (optional)",
            ["Auto-select", "ADKAR", "Kotter's 8-Step", "Prosci", "McKinsey 7-S"]
        )
        
        if st.button("Get Guidance", key="guidance_btn"):
            if guidance_input and st.session_state.openai_api_key:
                full_input = f"{guidance_input}\n\nPreferred framework: {framework}" if framework != "Auto-select" else guidance_input
                with st.spinner("Generating guidance..."):
                    result = analyze_transformation_data(full_input, "change_guidance")
                    st.session_state.chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "type": "Change Guidance",
                        "input": guidance_input,
                        "output": result
                    })
                    st.success("Guidance Generated!")
                    st.markdown("### 📚 Best Practice Guidance")
                    st.markdown(result)
            elif not st.session_state.openai_api_key:
                st.error("Please configure your OpenAI API key in the sidebar.")
            else:
                st.warning("Please describe your challenge.")
    
    with tab3:
        st.header("Team Communication Analysis")
        st.markdown("Analyze team sentiment and identify resistance patterns")
        
        team_input = st.text_area(
            "Paste team communications (emails, chat logs, meeting notes):",
            height=150,
            placeholder="E.g., Recent team emails, Slack conversations, retrospective notes..."
        )
        
        if st.button("Analyze Team Dynamics", key="team_btn"):
            if team_input and st.session_state.openai_api_key:
                with st.spinner("Analyzing team communications..."):
                    result = analyze_transformation_data(team_input, "team_analysis")
                    st.session_state.chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "type": "Team Analysis",
                        "input": team_input,
                        "output": result
                    })
                    st.success("Analysis Complete!")
                    st.markdown("### 👥 Team Dynamics Insights")
                    st.markdown(result)
            elif not st.session_state.openai_api_key:
                st.error("Please configure your OpenAI API key in the sidebar.")
            else:
                st.warning("Please provide team communications to analyze.")
    
    with tab4:
        st.header("Strategic Recommendations")
        st.markdown("Get targeted interventions and action plans")
        
        situation = st.text_area(
            "Describe the current transformation situation:",
            height=150,
            placeholder="E.g., Project timeline, stakeholder status, key challenges, milestones..."
        )
        
        urgency = st.select_slider(
            "Situation Urgency",
            options=["Low", "Medium", "High", "Critical"]
        )
        
        if st.button("Generate Recommendations", key="rec_btn"):
            if situation and st.session_state.openai_api_key:
                full_input = f"{situation}\n\nUrgency level: {urgency}"
                with st.spinner("Generating recommendations..."):
                    result = analyze_transformation_data(full_input, "recommendations")
                    st.session_state.chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "type": "Recommendations",
                        "input": situation,
                        "output": result
                    })
                    st.success("Recommendations Ready!")
                    st.markdown("### 💡 Strategic Action Plan")
                    st.markdown(result)
            elif not st.session_state.openai_api_key:
                st.error("Please configure your OpenAI API key in the sidebar.")
            else:
                st.warning("Please describe the situation.")
    
    # Display history
    if st.session_state.chat_history:
        st.markdown("---")
        st.header("📜 Analysis History")
        
        for i, entry in enumerate(reversed(st.session_state.chat_history[-5:])):
            with st.expander(f"{entry['type']} - {entry['timestamp']}"):
                st.markdown("**Input:**")
                st.text(entry['input'][:200] + "..." if len(entry['input']) > 200 else entry['input'])
                st.markdown("**Analysis:**")
                st.markdown(entry['output'])

# Main application logic
if not st.session_state.authenticated:
    login_page()
else:
    main_app()
