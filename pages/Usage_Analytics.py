import streamlit as st
import pandas as pd
from collections import Counter

if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in from the main page.")
    st.stop()

st.title("📊 Usage & Query Analytics")
st.write("Visualisation will go here.")

st.set_page_config(
    page_title="Usage & Query Analytics",
    page_icon="📊",
    layout="wide",
)

# Respect your existing login
if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in from the main page to access this content.")
    st.stop()

st.title("📊 Usage & Query Analytics")
st.markdown(
    """
This page gives an overview of how the **Transformation Management Assistant** 
is being used in the current session.
"""
)
st.markdown("---")

chat_history = st.session_state.get("chat_history", [])

if not chat_history:
    st.info("No analyses have been run in this session yet. Try running a few queries first.")
    st.stop()

# Turn history into a DataFrame
df = pd.DataFrame(chat_history)

# Ensure columns exist
expected_cols = ["timestamp", "type", "input", "output"]
for col in expected_cols:
    if col not in df.columns:
        df[col] = None

# Filters
st.subheader("1. Filters")
col1, col2 = st.columns(2)

with col1:
    types_available = sorted(df["type"].dropna().unique())
    selected_types = st.multiselect(
        "Filter by analysis type",
        options=types_available,
        default=types_available,
    )

with col2:
    search_term = st.text_input(
        "Search within input text (optional)",
        placeholder="e.g. resistance, finance, stakeholder"
    )

# Apply filters
filtered_df = df[df["type"].isin(selected_types)]

if search_term:
    search_term_lower = search_term.lower()
    filtered_df = filtered_df[
        filtered_df["input"].astype(str).str.lower().str.contains(search_term_lower)
        | filtered_df["output"].astype(str).str.lower().str.contains(search_term_lower)
    ]

st.markdown("---")

# Summary stats
st.subheader("2. Summary Statistics")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Analyses (Session)", len(df))

with c2:
    st.metric("Analyses (After Filters)", len(filtered_df))

with c3:
    type_counts = Counter(df["type"])
    most_common_type, most_common_count = type_counts.most_common(1)[0]
    st.metric("Most Used Analysis Type", f"{most_common_type} ({most_common_count})")

st.markdown("---")

# Visual: counts by type
st.subheader("3. Analyses by Type")

count_by_type = (
    filtered_df.groupby("type")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

st.bar_chart(
    data=count_by_type.set_index("type")["count"],
    use_container_width=True,
)

st.markdown("---")

# Visual: timeline
st.subheader("4. Timeline of Analyses (Current Session)")

# Convert timestamp to datetime if possible
try:
    filtered_df["timestamp_dt"] = pd.to_datetime(filtered_df["timestamp"])
    timeline_df = (
        filtered_df.sort_values("timestamp_dt")
        .groupby(filtered_df["timestamp_dt"].dt.floor("min"))
        .size()
        .reset_index(name="count")
        .rename(columns={"timestamp_dt": "time"})
    )

    st.line_chart(
        data=timeline_df.set_index("time")["count"],
        use_container_width=True,
    )
except Exception:
    st.info("Timestamp format could not be parsed into a timeline. Using raw table instead.")

st.markdown("---")

# Table of queries
st.subheader("5. Detailed Query Log (Current Session)")

st.dataframe(
    filtered_df[["timestamp", "type", "input", "output"]],
    use_container_width=True,
    height=400,
)

st.caption(
    "This view is based only on the current Streamlit session. "
    "Data is not persisted once the session ends."
)

