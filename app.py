# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Academic Stress Dashboard", layout="wide")

# -------------------------------
# LOAD DATA
# -------------------------------
DATA_URL = "https://raw.githubusercontent.com/Nashalan/Assignment-/refs/heads/main/Academic%20Stress%20Level.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()

# Helper: find the stress column automatically
def get_stress_column(df):
    for c in df.columns:
        if "stress" in c.lower():
            return c
    return None

stress_col = get_stress_column(df)

# -------------------------------
# SIDEBAR MENU
# -------------------------------
st.sidebar.title("📊 Academic Stress Dashboard")
page = st.sidebar.radio(
    "Select Page:",
    ["🏠 Home", "🎯 Stress Distribution", "🎓 Academic Factors", "💤 Lifestyle Factors"]
)

# -------------------------------
# HOME PAGE
# -------------------------------
if page == "🏠 Home":
    st.title("🏠 Academic Stress Level Dashboard")
    st.markdown("""
    Welcome to the **Academic Stress Visualization Dashboard**!  
    This dashboard explores how **academic** and **lifestyle** factors relate to students' stress levels.

    ### Contents:
    - 🎯 *Stress Distribution*: Overview of stress patterns  
    - 🎓 *Academic Factors*: Study habits, performance, and their correlation with stress  
    - 💤 *Lifestyle Factors*: Sleep, exercise, and health impacts on stress
    """)

    st.subheader("📘 Dataset Overview")
    st.dataframe(df.head())

    st.sidebar.success("Use the sidebar to explore different pages.")


# -------------------------------
# STRESS DISTRIBUTION PAGE
# -------------------------------
elif page == "🎯 Stress Distribution":
    st.title("🎯 Stress Distribution Analysis")

    # Objective
    st.markdown("### 🎯 Objective")
    st.write("To visualize the overall distribution of students' stress levels and identify any patterns or outliers in the dataset.")

    # Summary
    st.markdown("### 📦 Summary Box")
    st.info("""
    This section analyzes the distribution of academic stress levels across all students.
    It highlights whether the stress levels are normally distributed or skewed, and identifies
    differences across gender or other demographic groups if available.
    """)

    # Visualizations
    if stress_col:
        st.markdown("### 📊 Visualizations")

        # Histogram
        fig, ax = plt.subplots()
        sns.histplot(df[stress_col], kde=True, color="skyblue", ax=ax)
        ax.set_title("Distribution of Stress Levels")
        st.pyplot(fig)

        # Boxplot
        fig, ax = plt.subplots()
        sns.boxplot(x=df[stress_col], color="salmon", ax=ax)
        ax.set_title("Boxplot of Stress Levels")
        st.pyplot(fig)

        # Gender-based Pie Chart (if available)
        if "gender" in df.columns:
            avg_stress = df.groupby("gender")[stress_col].mean().reset_index()
            fig = px.pie(avg_stress, names="gender", values=stress_col, title="Average Stress by Gender")
            st.plotly_chart(fig)

        # Interpretation
        st.markdown("### 💬 Interpretation / Discussion")
        st.write("""
        The histogram shows how stress levels are distributed among students.
        A right-skewed shape indicates that most students have moderate stress, while
        a left-skewed pattern would indicate high stress among many students.
        The boxplot helps detect outliers, and gender-based visualization reveals
        potential differences in stress perception across groups.
        """)
    else:
        st.error("⚠️ No column containing 'stress' found in dataset.")


# -------------------------------
# ACADEMIC FACTORS PAGE
# -------------------------------
elif page == "🎓 Academic Factors":
    st.title("🎓 Academic Factors & Stress")

    # Objective
    st.markdown("### 🎯 Objective")
    st.write("To examine how academic variables such as study hours or grades influence stress levels.")

    # Summary
    st.markdown("### 📦 Summary Box")
    st.info("""
    This section explores how different academic performance indicators affect stress levels.
    It uses scatter plots and correlation heatmaps to detect linear or nonlinear relationships
    between study-related factors and students’ reported stress.
    """)

    if stress_col:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if stress_col in numeric_cols:
            numeric_cols.remove(stress_col)

        if numeric_cols:
            st.markdown("### 📊 Visualizations")

            # Scatter Plot
            x_axis = st.selectbox("Select an academic variable to compare:", numeric_cols)
            fig = px.scatter(df, x=x_axis, y=stress_col, trendline="ols",
                             title=f"{x_axis.replace('_',' ').title()} vs Stress Level")
            st.plotly_chart(fig)

            # Correlation Heatmap
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
            ax.set_title("Correlation Heatmap of Academic Factors")
            st.pyplot(fig)

            # Pairplot
            selected = st.multiselect("Select up to 3 variables for pairplot:", numeric_cols, numeric_cols[:3])
            if selected:
                sns.pairplot(df, vars=selected + [stress_col], diag_kind="kde")
                st.pyplot(plt.gcf())

            # Interpretation
            st.markdown("### 💬 Interpretation / Discussion")
            st.write("""
            Strong positive correlations indicate that as academic workload or study hours increase,
            stress levels also tend to rise. Conversely, negative correlations may imply that effective
            study habits or higher academic performance reduce stress. Outliers may represent students
            who handle stress differently despite similar workloads.
            """)
        else:
            st.warning("No numeric academic columns found.")
    else:
        st.error("⚠️ No stress column found in dataset.")


# -------------------------------
# LIFESTYLE FACTORS PAGE
# -------------------------------
elif page == "💤 Lifestyle Factors":
    st.title("💤 Lifestyle Factors & Stress")

    # Objective
    st.markdown("### 🎯 Objective")
    st.write("To analyze how lifestyle choices such as sleep and physical activity influence academic stress levels.")

    # Summary
    st.markdown("### 📦 Summary Box")
    st.info("""
    Lifestyle habits, including sleep duration and physical activity, are known to affect mental well-being.
    This section visualizes how these behaviors correlate with students’ reported stress levels.
    """)

    if stress_col:
        st.markdown("### 📊 Visualizations")

        # Sleep Duration
        if "sleep_duration" in df.columns:
            fig = px.scatter(df, x="sleep_duration", y=stress_col,
                             color="sleep_duration", color_continuous_scale="viridis",
                             title="Sleep Duration vs Stress Level")
            st.plotly_chart(fig)

        # Physical Activity
        if "physical_activity" in df.columns:
            fig, ax = plt.subplots()
            sns.boxplot(x="physical_activity", y=stress_col, data=df, palette="coolwarm", ax=ax)
            ax.set_title("Stress Level by Physical Activity")
            st.pyplot(fig)

        # 3D Relationship
        if all(c in df.columns for c in ["sleep_duration", "physical_activity"]):
            fig = px.scatter_3d(
                df, x="sleep_duration", y="physical_activity", z=stress_col,
                color=stress_col, title="3D Relationship: Sleep, Activity & Stress"
            )
            st.plotly_chart(fig)

        # Interpretation
        st.markdown("### 💬 Interpretation / Discussion")
        st.write("""
        Students with longer sleep duration generally exhibit lower stress levels,
        while those with insufficient sleep report higher stress. Similarly, regular
        physical activity appears to buffer stress. The 3D plot highlights how
        balanced sleep and activity together contribute to reduced stress.
        """)
    else:
        st.error("⚠️ No stress column found in dataset.")
