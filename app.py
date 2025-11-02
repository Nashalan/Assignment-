# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# detect stress column automatically
def get_stress_column(df):
    for c in df.columns:
        if "stress" in c.lower():
            return c
    return None

stress_col = get_stress_column(df)

# ---------------------------------------------------
# SIDEBAR MENU
# ---------------------------------------------------
st.sidebar.title("📊 Academic Stress Dashboard")
page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Home", "🎯 Stress Overview", "🎓 Academic Factors", "💤 Lifestyle & Well-being"]
)

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
if page == "🏠 Home":
    st.title("🏫 Academic Stress Level Dashboard")
    st.markdown("""
    Welcome to the **Academic Stress Visualization Dashboard**!  
    This dashboard explores how academic and lifestyle factors influence student stress.

    🔹 **Stress Overview:** Understand the distribution of stress among students.  
    🔹 **Academic Factors:** Explore how study habits, grades, and workload affect stress.  
    🔹 **Lifestyle & Well-being:** See how sleep and activity patterns influence stress.
    """)

    st.subheader("📘 Dataset Overview")
    st.dataframe(df.head())

    st.info("👉 Use the sidebar to switch between pages and explore insights interactively!")

# ---------------------------------------------------
# STRESS OVERVIEW PAGE
# ---------------------------------------------------
elif page == "🎯 Stress Overview":
    st.title("🎯 Stress Distribution & Overview")

    st.markdown("### 🎯 Objective")
    st.write("To visualize how stress levels are distributed and understand overall patterns across students.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This section visualizes the **distribution and spread** of student stress levels.
    You can identify where most students fall on the stress scale and see 
    if any groups (like gender or course) experience higher average stress.
    """)

    if stress_col:
        # Histogram
        fig1 = px.histogram(df, x=stress_col, nbins=20, title="Distribution of Stress Levels",
                            color_discrete_sequence=["#4FC3F7"])
        fig1.update_layout(xaxis_title="Stress Level", yaxis_title="Count")
        st.plotly_chart(fig1, use_container_width=True)

        # Average stress by gender (if exists)
        if "gender" in df.columns:
            fig2 = px.bar(df, x="gender", y=stress_col, color="gender",
                          title="Average Stress Level by Gender", barmode="group")
            st.plotly_chart(fig2, use_container_width=True)

        # Trend by age (if exists)
        if "age" in df.columns:
            fig3 = px.line(df.sort_values("age"), x="age", y=stress_col,
                           title="Stress Trend Across Age", markers=True)
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("### 💬 Interpretation")
        st.success("""
        The distribution shows that most students fall within a moderate stress range.  
        Gender-based and age-based trends indicate how different groups experience stress differently, 
        revealing potential areas for student support.
        """)
    else:
        st.error("No stress column found in dataset.")

# ---------------------------------------------------
# ACADEMIC FACTORS PAGE (DIFFERENT VISUALS)
# ---------------------------------------------------
elif page == "🎓 Academic Factors":
    st.title("🎓 Academic Factors Influencing Stress")

    st.markdown("### 🎯 Objective")
    st.write("To explore how academic workload, performance, and habits affect students' stress levels using interactive visuals.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    Academic-related variables such as **study hours**, **course load**, and **grades** 
    can have strong links to stress.  
    The visuals here highlight which academic patterns most contribute to stress variation.
    """)

    if stress_col:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        # Correlation Heatmap
        corr = df[numeric_cols].corr()[stress_col].sort_values(ascending=False).reset_index()
        corr.columns = ['Variable', 'Correlation with Stress']
        fig_corr = px.bar(corr, x='Variable', y='Correlation with Stress', color='Correlation with Stress',
                          color_continuous_scale='RdBu', title="Correlation of Academic Factors with Stress")
        st.plotly_chart(fig_corr, use_container_width=True)

        # Scatter matrix (pairplot style)
        selected = st.multiselect("Select academic variables to compare with stress:", 
                                  [col for col in numeric_cols if col != stress_col],
                                  default=[numeric_cols[0]] if numeric_cols else [])
        if selected:
            fig_matrix = px.scatter_matrix(df, dimensions=selected + [stress_col],
                                           color=stress_col,
                                           title="Relationship Between Academic Variables and Stress")
            st.plotly_chart(fig_matrix, use_container_width=True)

        # Course Load (if available)
        if "course_load" in df.columns:
            avg_stress = df.groupby("course_load")[stress_col].mean().reset_index()
            fig_bar = px.bar(avg_stress, x="course_load", y=stress_col, color=stress_col,
                             title="Average Stress by Course Load")
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("### 💬 Interpretation")
        st.success("""
        The correlation chart shows which academic variables most influence stress.  
        A high positive correlation (red) means as that variable increases, stress rises too — 
        for instance, higher study hours or heavier course loads.  
        Interactive scatter plots reveal clusters of students with high or low stress,
        suggesting performance-based stress differences.
        """)
    else:
        st.error("No stress column found in dataset.")

# ---------------------------------------------------
# LIFESTYLE & WELL-BEING PAGE
# ---------------------------------------------------
elif page == "💤 Lifestyle & Well-being":
    st.title("💤 Lifestyle & Well-being Factors")

    st.markdown("### 🎯 Objective")
    st.write("To analyze how lifestyle factors like sleep duration, exercise, and social habits impact stress levels.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This page focuses on daily routines that affect stress management.  
    Factors such as **sleep**, **physical activity**, and **leisure time** 
    play crucial roles in determining a student's resilience to stress.
    """)

    if stress_col:
        # Sleep vs Stress
        if "sleep_duration" in df.columns:
            fig1 = px.scatter(df, x="sleep_duration", y=stress_col, color=stress_col,
                              color_continuous_scale="Viridis", trendline="ols",
                              title="Sleep Duration vs Stress Level")
            st.plotly_chart(fig1, use_container_width=True)

        # Physical activity vs Stress (using violin plot)
        if "physical_activity" in df.columns:
            fig2 = px.violin(df, x="physical_activity", y=stress_col, color="physical_activity",
                             box=True, points="all", title="Stress Levels by Physical Activity")
            st.plotly_chart(fig2, use_container_width=True)

        # Combined 3D plot
        if all(c in df.columns for c in ["sleep_duration", "physical_activity"]):
            fig3 = px.scatter_3d(df, x="sleep_duration", y="physical_activity", z=stress_col,
                                 color=stress_col, color_continuous_scale="Plasma",
                                 title="3D Relationship: Sleep, Activity & Stress")
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("### 💬 Interpretation")
        st.success("""
        The visuals show that students with **more sleep** and **regular physical activity** 
        report significantly lower stress levels.  
        The 3D visualization highlights that combining adequate rest with movement 
        creates the lowest stress zone — reinforcing the value of balanced routines.
        """)
    else:
        st.error("No stress column found in dataset.")
