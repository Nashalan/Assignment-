# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ------------------------------------
# PAGE CONFIGURATION
# ------------------------------------
st.set_page_config(page_title="Academic Stress Dashboard", layout="wide")

# ------------------------------------
# LOAD DATASET
# ------------------------------------
DATA_URL = "https://raw.githubusercontent.com/Nashalan/Assignment-/refs/heads/main/Academic%20Stress%20Level.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()

# Helper function: automatically find stress column
def get_stress_column(df):
    for c in df.columns:
        if "stress" in c.lower():
            return c
    return None

stress_col = get_stress_column(df)

# ------------------------------------
# SIDEBAR MENU
# ------------------------------------
st.sidebar.title("📊 Academic Stress Dashboard")
page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Home", "🎯 Stress Distribution", "🎓 Academic Factors", "💤 Lifestyle Factors"]
)

# ------------------------------------
# HOME PAGE
# ------------------------------------
if page == "🏠 Home":
    st.title("🏠 Academic Stress Level Dashboard")
    st.markdown("""
    Welcome to the **Academic Stress Visualization Dashboard**!  
    This dashboard explores how **academic** and **lifestyle** factors influence student stress.

    **Sections Overview:**
    - 🎯 Stress Distribution: How stress levels vary among students  
    - 🎓 Academic Factors: Study habits, grades, and workload impact  
    - 💤 Lifestyle Factors: Sleep, physical activity, and well-being
    """)
    
    st.subheader("📘 Dataset Overview")
    st.dataframe(df.head())
    st.sidebar.info("👉 Use the sidebar to switch between pages.")


# ------------------------------------
# STRESS DISTRIBUTION PAGE
# ------------------------------------
elif page == "🎯 Stress Distribution":
    st.title("🎯 Stress Distribution Analysis")

    st.markdown("### 🎯 Objective")
    st.write("To visualize the overall distribution of students' stress levels and identify key patterns or outliers.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This visualization examines how students’ stress levels are distributed across the dataset.
    It reveals whether stress levels follow a normal, skewed, or bimodal pattern and compares
    stress across genders when applicable.
    """)

    if stress_col:
        st.markdown("### 📊 Visualizations")

        # 1. Histogram
        fig, ax = plt.subplots()
        sns.histplot(df[stress_col], kde=True, color="skyblue", ax=ax)
        ax.set_title("Distribution of Stress Levels")
        st.pyplot(fig)

        # 2. Boxplot
        fig, ax = plt.subplots()
        sns.boxplot(x=df[stress_col], color="salmon", ax=ax)
        ax.set_title("Boxplot of Stress Levels")
        st.pyplot(fig)

        # 3. Pie Chart (by gender if exists)
        if "gender" in df.columns:
            avg_stress = df.groupby("gender")[stress_col].mean().reset_index()
            fig = px.pie(avg_stress, names="gender", values=stress_col, title="Average Stress by Gender")
            st.plotly_chart(fig)

        st.markdown("### 💬 Interpretation / Discussion")
        st.write("""
        The histogram indicates how stress levels are spread among students.
        A right-skewed curve suggests most students experience moderate stress.
        The boxplot helps detect outliers—students reporting extreme stress.
        Gender differences, if visible, highlight variations in stress perception.
        """)
    else:
        st.error("⚠️ No column containing 'stress' found in the dataset.")


# ------------------------------------
# ACADEMIC FACTORS PAGE
# ------------------------------------
elif page == "🎓 Academic Factors":
    st.title("🎓 Academic Factors & Stress")

    st.markdown("### 🎯 Objective")
    st.write("To explore the impact of academic workload and performance variables on student stress levels.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This section investigates correlations between academic metrics (e.g., study hours, grades) and stress.
    Scatter plots, correlation heatmaps, and pairplots help visualize the strength and direction of these relationships.
    """)

    if stress_col:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if stress_col in numeric_cols:
            numeric_cols.remove(stress_col)

        if numeric_cols:
            st.markdown("### 📊 Visualizations")

            # 1. Scatter plot
            x_axis = st.selectbox("Select an academic variable to compare:", numeric_cols)
            fig = px.scatter(df, x=x_axis, y=stress_col, trendline="ols",
                             title=f"{x_axis.replace('_',' ').title()} vs Stress Level")
            st.plotly_chart(fig)

            # 2. Correlation heatmap
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
            ax.set_title("Correlation Heatmap of Academic Factors")
            st.pyplot(fig)

            # 3. Pairplot
            selected = st.multiselect("Select up to 3 variables for pairplot:", numeric_cols, numeric_cols[:3])
            if selected:
                sns.pairplot(df, vars=selected + [stress_col], diag_kind="kde")
                st.pyplot(plt.gcf())

            st.markdown("### 💬 Interpretation / Discussion")
            st.write("""
            Strong positive correlations imply that heavier academic workloads or lower grades
            are associated with higher stress. Conversely, weaker or negative correlations suggest
            better performance may reduce perceived stress. Pairplots reveal clusters or anomalies
            in the academic-stress relationship.
            """)
        else:
            st.warning("No numeric academic columns found.")
    else:
        st.error("⚠️ No stress column found in dataset.")


# ------------------------------------
# LIFESTYLE FACTORS PAGE
# ------------------------------------
elif page == "💤 Lifestyle Factors":
    st.title("💤 Lifestyle Factors & Stress")

    st.markdown("### 🎯 Objective")
    st.write("To assess how lifestyle factors—particularly sleep and physical activity—affect stress levels.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    Lifestyle behaviors such as sleep and exercise play key roles in managing stress.
    This section visualizes how these factors correlate with stress, showing whether
    healthier habits are linked to lower stress.
    """)

    if stress_col:
        st.markdown("### 📊 Visualizations")

        # 1. Sleep duration vs stress
        if "sleep_duration" in df.columns:
            fig = px.scatter(df, x="sleep_duration", y=stress_col,
                             color="sleep_duration", color_continuous_scale="viridis",
                             title="Sleep Duration vs Stress Level")
            st.plotly_chart(fig)

        # 2. Physical activity vs stress
        if "physical_activity" in df.columns:
            fig, ax = plt.subplots()
            sns.boxplot(x="physical_activity", y=stress_col, data=df, palette="coolwarm", ax=ax)
            ax.set_title("Stress Level by Physical Activity")
            st.pyplot(fig)

        # 3. 3D scatter
        if all(c in df.columns for c in ["sleep_duration", "physical_activity"]):
            fig = px.scatter_3d(
                df, x="sleep_duration", y="physical_activity", z=stress_col,
                color=stress_col, title="3D Relationship: Sleep, Activity & Stress"
            )
            st.plotly_chart(fig)

        st.markdown("### 💬 Interpretation / Discussion")
        st.write("""
        Students with longer sleep duration generally exhibit lower stress levels,
        while low physical activity tends to correspond with higher stress.
        The 3D visualization emphasizes the combined effect of sleep and activity
        on overall well-being and stress reduction.
        """)
    else:
        st.error("⚠️ No stress column found in dataset.")
