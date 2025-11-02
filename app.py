# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

# find stress column
def get_stress_column(df):
    for c in df.columns:
        if "stress" in c.lower():
            return c
    return None

stress_col = get_stress_column(df)

# ---------------------------------------------------
# SIDEBAR MENU
# ---------------------------------------------------
st.sidebar.title("📊 Navigation Menu")
page = st.sidebar.radio(
    "Select a Page:",
    ["🏠 Home", "🎯 Stress Overview", "🎓 Academic Factors", "💤 Lifestyle & Well-being"]
)

# ---------------------------------------------------
# PAGE 1 — HOME
# ---------------------------------------------------
if page == "🏠 Home":
    st.title("🏫 Academic Stress Level Dashboard")
    st.markdown("""
    Welcome to the **Academic Stress Visualization Dashboard**!  
    This tool provides insights into how academic workload, habits, and lifestyle choices affect students' stress levels.
    """)

    st.subheader("📘 Dataset Preview")
    st.dataframe(df.head())

    st.info("""
    Use the sidebar to navigate through the pages:
    - 🎯 *Stress Overview* — overall distribution of stress levels  
    - 🎓 *Academic Factors* — academic habits and performance  
    - 💤 *Lifestyle & Well-being* — impact of daily routines
    """)

# ---------------------------------------------------
# PAGE 2 — STRESS OVERVIEW
# ---------------------------------------------------
elif page == "🎯 Stress Overview":
    st.title("🎯 Stress Overview & Patterns")

    st.markdown("### 🎯 Objective")
    st.write("To understand how stress levels are distributed among students and whether any patterns exist across demographic factors.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This section explores the **overall distribution** of stress levels.
    It highlights whether most students experience high, medium, or low stress, 
    and how stress varies across groups such as gender or course load.
    """)

    if stress_col:
        st.markdown("### 📊 Visualizations")

        # Histogram
        fig, ax = plt.subplots()
        sns.histplot(df[stress_col], kde=True, color="skyblue", ax=ax)
        ax.set_title("Distribution of Student Stress Levels")
        st.pyplot(fig)

        # Boxplot
        fig, ax = plt.subplots()
        sns.boxplot(x=df[stress_col], color="lightcoral", ax=ax)
        ax.set_title("Boxplot of Stress Levels")
        st.pyplot(fig)

        # Gender Comparison (if available)
        if "gender" in df.columns:
            fig = px.violin(df, x="gender", y=stress_col, color="gender",
                            box=True, points="all", title="Stress Levels by Gender")
            st.plotly_chart(fig)

        st.markdown("### 💬 Interpretation")
        st.success("""
        The histogram shows that stress levels are concentrated around the middle range, 
        indicating moderate stress among most students.  
        The boxplot reveals some outliers—students reporting extreme stress levels.  
        If gender differences appear, it may suggest how social or academic pressures differ between groups.
        """)
    else:
        st.error("No column containing 'stress' found in the dataset.")

# ---------------------------------------------------
# PAGE 3 — ACADEMIC FACTORS
# ---------------------------------------------------
elif page == "🎓 Academic Factors":
    st.title("🎓 Academic Factors & Student Stress")

    st.markdown("### 🎯 Objective")
    st.write("To investigate how study habits, workload, and academic performance influence students' stress levels.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This page focuses on **academic influences** such as study hours, 
    course difficulty, and grades.  
    Using correlation and scatter plots, it shows whether academic pressure 
    significantly raises student stress levels.
    """)

    if stress_col:
        st.markdown("### 📊 Visualizations")

        # Correlation Heatmap
        numeric_df = df.select_dtypes(include="number")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Between Academic Variables")
        st.pyplot(fig)

        # Scatter plot with user selection
        num_cols = [col for col in numeric_df.columns if col != stress_col]
        if num_cols:
            x_var = st.selectbox("Select Academic Variable:", num_cols)
            fig = px.scatter(df, x=x_var, y=stress_col, color=stress_col,
                             trendline="ols", title=f"{x_var.replace('_',' ').title()} vs Stress Level")
            st.plotly_chart(fig)

        # Average stress by grade or course load (if exists)
        if "course_load" in df.columns:
            avg_stress = df.groupby("course_load")[stress_col].mean().reset_index()
            fig = px.bar(avg_stress, x="course_load", y=stress_col,
                         title="Average Stress by Course Load", color=stress_col)
            st.plotly_chart(fig)

        st.markdown("### 💬 Interpretation")
        st.success("""
        The correlation heatmap highlights which academic factors most strongly influence stress.  
        A positive correlation suggests that increased workload or lower grades are linked to higher stress.  
        Scatter plots visualize these relationships, making it clear how academic performance affects mental well-being.
        """)
    else:
        st.error("No stress column found in dataset.")

# ---------------------------------------------------
# PAGE 4 — LIFESTYLE & WELL-BEING
# ---------------------------------------------------
elif page == "💤 Lifestyle & Well-being":
    st.title("💤 Lifestyle Habits and Stress Management")

    st.markdown("### 🎯 Objective")
    st.write("To explore how lifestyle behaviors such as sleep duration and physical activity influence student stress levels.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    Healthy routines can significantly reduce stress.  
    This section visualizes how **sleep duration**, **physical activity**, 
    and other lifestyle patterns correlate with stress among students.
    """)

    if stress_col:
        st.markdown("### 📊 Visualizations")

        # 1. Sleep vs Stress
        if "sleep_duration" in df.columns:
            fig = px.scatter(df, x="sleep_duration", y=stress_col, color=stress_col,
                             color_continuous_scale="viridis", trendline="ols",
                             title="Sleep Duration vs Stress Level")
            st.plotly_chart(fig)

        # 2. Physical Activity vs Stress
        if "physical_activity" in df.columns:
            fig, ax = plt.subplots()
            sns.boxplot(x="physical_activity", y=stress_col, data=df, palette="Set2", ax=ax)
            ax.set_title("Stress Levels Across Physical Activity Levels")
            st.pyplot(fig)

        # 3. 3D Relationship (if both present)
        if all(c in df.columns for c in ["sleep_duration", "physical_activity"]):
            fig = px.scatter_3d(df, x="sleep_duration", y="physical_activity", z=stress_col,
                                color=stress_col, color_continuous_scale="Plasma",
                                title="3D Relationship: Sleep, Activity & Stress")
            st.plotly_chart(fig)

        st.markdown("### 💬 Interpretation")
        st.success("""
        Students who get adequate sleep or engage in regular physical activity 
        generally report lower stress levels.  
        Short sleep durations and inactivity correlate with higher stress.  
        The 3D visualization shows how combining good sleep and active habits 
        can help reduce academic stress effectively.
        """)
    else:
        st.error("No stress column found in dataset.")
