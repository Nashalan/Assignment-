# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------
st.set_page_config(page_title="Academic Stress Visualization", layout="wide")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/Nashalan/Assignment-/refs/heads/main/Academic%20Stress%20Level.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()
print(df.columns.tolist())


# detect stress column automatically
def get_stress_column(df):
    for c in df.columns:
        if "stress" in c.lower():
            return c
    return None

stress_col = get_stress_column(df)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("📊 Academic Stress Dashboard")
page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Home", "🎯 Stress Overview", "🎓 Academic Factors", "💤 Lifestyle & Well-being"]
)

# ---------------------------------------------------
# PAGE 1: HOME
# ---------------------------------------------------
if page == "🏠 Home":
    st.title("🏫 Academic Stress Level Dashboard")
    st.markdown("""
    Welcome to the **Academic Stress Visualization Dashboard**!  
    This dashboard explores how academic and lifestyle factors influence student stress.

    🔹 **Stress Overview:** General distribution of stress  
    🔹 **Academic Factors:** Study habits & performance  
    🔹 **Lifestyle & Well-being:** Health, satisfaction, & balance
    """)

    st.subheader("📘 Dataset Preview")
    st.dataframe(df.head())
    st.info("Use the sidebar to switch between pages.")

# ---------------------------------------------------
# PAGE 2: STRESS OVERVIEW
# ---------------------------------------------------
elif page == "🎯 Stress Overview":
    st.title("🎯 Stress Overview")

    st.markdown("### 🎯 Objective")
    st.write("To analyze how stress levels are distributed among students and across demographic groups.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This page explores how stress levels vary overall and across student categories.
    It helps identify whether most students experience low, moderate, or high stress.
    """)

    if stress_col:
        # Histogram
        fig1 = px.histogram(df, x=stress_col, nbins=20, title="Distribution of Student Stress Levels",
                            color_discrete_sequence=["#4FC3F7"])
        st.plotly_chart(fig1, use_container_width=True)

        # Gender (if available)
        if "gender" in df.columns:
            fig2 = px.box(df, x="gender", y=stress_col, color="gender",
                          title="Stress Levels by Gender", points="all")
            st.plotly_chart(fig2, use_container_width=True)

        # Age or any numeric trend
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if "age" in numeric_cols:
            fig3 = px.line(df.sort_values("age"), x="age", y=stress_col,
                           title="Stress Across Age", markers=True)
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("### 💬 Interpretation")
        st.success("""
        The distribution indicates how stress is spread across the student body.  
        Patterns by gender or age highlight which groups may experience higher stress,
        providing a basis for further academic or counseling interventions.
        """)
    else:
        st.error("No stress-related column found in dataset.")

# ---------------------------------------------------
# PAGE 3: ACADEMIC FACTORS
# ---------------------------------------------------
elif page == "🎓 Academic Factors":
    st.title("🎓 Academic Factors & Stress")

    st.markdown("### 🎯 Objective")
    st.write("To investigate the relationship between academic workload and stress using interactive comparisons.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    Academic pressures such as study time, test performance, or assignment load
    can have significant effects on stress.  
    This section visualizes how these academic metrics relate to stress levels.
    """)

    if stress_col:
        # Identify numeric columns besides stress
        numeric_cols = [col for col in df.select_dtypes(include="number").columns if col != stress_col]

        # Correlation with stress
        if numeric_cols:
            corr = df[numeric_cols + [stress_col]].corr()[stress_col].sort_values(ascending=False).reset_index()
            corr.columns = ['Variable', 'Correlation']
            fig_corr = px.bar(corr, x='Variable', y='Correlation', color='Correlation',
                              color_continuous_scale='RdBu', title="Correlation of Academic Variables with Stress")
            st.plotly_chart(fig_corr, use_container_width=True)

        # User choose variable for comparison
        if numeric_cols:
            selected = st.selectbox("Select Academic Variable:", numeric_cols)
            fig = px.scatter(df, x=selected, y=stress_col, color=stress_col,
                             trendline="ols", title=f"{selected.replace('_',' ').title()} vs Stress Level")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 💬 Interpretation")
        st.success("""
        Academic-related metrics such as workload or performance often show 
        strong correlations with stress.  
        The scatter plot helps visualize how changes in academic effort 
        or achievement may directly impact stress levels.
        """)
    else:
        st.error("No stress-related column found in dataset.")

# ---------------------------------------------------
# PAGE 4: LIFESTYLE & WELL-BEING
# ---------------------------------------------------
elif page == "💤 Lifestyle & Well-being":
    st.title("💤 Lifestyle & Well-being")

    st.markdown("### 🎯 Objective")
    st.write("To assess how students’ daily habits, satisfaction, and well-being correlate with their stress levels.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This section visualizes **stress against well-being indicators** (like happiness,
    satisfaction, or balance).  
    It helps identify whether students who report higher well-being experience less stress.
    """)

    if stress_col:
        # Try to find relevant lifestyle columns automatically
        possible_cols = [c for c in df.columns if any(x in c for x in
                         ["sleep", "activity", "wellbeing", "satisfaction", "happiness", "balance", "health"])]

        if not possible_cols:
            # fallback: just pick other numeric or ordinal columns
            possible_cols = [c for c in df.columns if c != stress_col and df[c].dtype != 'object']

        if possible_cols:
            for col in possible_cols[:3]:  # limit to 3 visuals
                fig = px.scatter(df, x=col, y=stress_col, color=stress_col,
                                 color_continuous_scale="Viridis",
                                 trendline="ols",
                                 title=f"{col.replace('_',' ').title()} vs Stress Level")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No suitable lifestyle or well-being columns found.")

        st.markdown("### 💬 Interpretation")
        st.success("""
        Students who report higher well-being or satisfaction levels typically show lower stress values.  
        Even if your dataset lacks direct lifestyle indicators, related measures like happiness 
        or self-evaluation can still reveal important stress patterns.
        """)
    else:
        st.error("No stress column found in dataset.")
