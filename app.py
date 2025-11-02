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
    ["🏠 Home", "🎯 Stress Overview", "🎓 Academic Factors", "💡 Stress Management & Recommendations"]
)

# ---------------------------------------------------
# PAGE 1 — HOME
# ---------------------------------------------------
if page == "🏠 Home":
    st.title("🏫 Academic Stress Level Dashboard")
    st.markdown("""
    Welcome to the **Academic Stress Visualization Dashboard**!  
    This tool explores how academic and personal factors impact student stress levels.

    **Sections Overview:**
    - 🎯 *Stress Overview*: General stress trends  
    - 🎓 *Academic Factors*: Study workload and academic influences  
    - 💡 *Stress Management*: Insights and personalized recommendations
    """)

    st.subheader("📘 Dataset Preview")
    st.dataframe(df.head())

    st.info("👉 Use the sidebar to navigate between visualization sections.")

# ---------------------------------------------------
# PAGE 2 — STRESS OVERVIEW
# ---------------------------------------------------
elif page == "🎯 Stress Overview":
    st.title("🎯 Stress Level Distribution and Overview")

    st.markdown("### 🎯 Objective")
    st.write("To visualize how stress levels are distributed and identify general patterns.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This page examines the **spread and variation of student stress levels**, including differences 
    by gender and age (if available). The aim is to highlight which demographics experience higher stress.
    """)

    if stress_col:
        # Histogram
        fig1 = px.histogram(df, x=stress_col, nbins=20, title="Distribution of Stress Levels",
                            color_discrete_sequence=["#4FC3F7"])
        fig1.update_layout(xaxis_title="Stress Level", yaxis_title="Number of Students")
        st.plotly_chart(fig1, use_container_width=True)

        # Stress by gender
        if "gender" in df.columns:
            avg_stress_gender = df.groupby("gender")[stress_col].mean().reset_index()
            fig2 = px.bar(avg_stress_gender, x="gender", y=stress_col, color="gender",
                          title="Average Stress by Gender")
            st.plotly_chart(fig2, use_container_width=True)

        # Stress by age (if available)
        if "age" in df.columns:
            fig3 = px.line(df.sort_values("age"), x="age", y=stress_col,
                           title="Stress Level by Age", markers=True)
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("### 💬 Interpretation")
        st.success("""
        Most students experience **moderate stress levels**, with some variations by age and gender.  
        Such insights can guide interventions or support systems targeting more vulnerable groups.
        """)
    else:
        st.error("⚠️ No column containing 'stress' found in the dataset.")

# ---------------------------------------------------
# PAGE 3 — ACADEMIC FACTORS
# ---------------------------------------------------
elif page == "🎓 Academic Factors":
    st.title("🎓 Academic Factors Affecting Stress")

    st.markdown("### 🎯 Objective")
    st.write("To explore how academic workload, grades, and study habits influence stress levels.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    Academic factors such as **course load**, **study hours**, and **grades** are common stress drivers.  
    This page examines how these academic metrics correlate with students’ stress levels.
    """)

    if stress_col:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        # Correlation with stress
        corr = df[numeric_cols].corr()[stress_col].sort_values(ascending=False).reset_index()
        corr.columns = ['Variable', 'Correlation with Stress']
        fig_corr = px.bar(corr, x='Variable', y='Correlation with Stress', color='Correlation with Stress',
                          color_continuous_scale='RdBu', title="Correlation of Academic Factors with Stress")
        st.plotly_chart(fig_corr, use_container_width=True)

        # Scatter plot to compare stress with selected variable
        num_cols = [col for col in numeric_cols if col != stress_col]
        if num_cols:
            x_var = st.selectbox("Select an Academic Variable to Compare with Stress:", num_cols)
            fig_scat = px.scatter(df, x=x_var, y=stress_col,
                                  color=stress_col, color_continuous_scale="Viridis",
                                  title=f"{x_var.replace('_',' ').title()} vs Stress Level")
            st.plotly_chart(fig_scat, use_container_width=True)

        st.markdown("### 💬 Interpretation")
        st.success("""
        High correlations between **academic load** or **lower performance** and stress confirm that 
        heavy workloads and low grades significantly increase pressure.  
        These findings support the need for balanced scheduling and academic counseling.
        """)
    else:
        st.error("⚠️ No stress column found in dataset.")

# ---------------------------------------------------
# PAGE 4 — STRESS MANAGEMENT & RECOMMENDATIONS
# ---------------------------------------------------
elif page == "💡 Stress Management & Recommendations":
    st.title("💡 Stress Management & Recommendations")

    st.markdown("### 🎯 Objective")
    st.write("To identify high-stress patterns and offer practical recommendations to reduce stress.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This section identifies **which groups experience more stress** and provides 
    **personalized, data-driven suggestions** to improve well-being and productivity.
    """)

    if stress_col:
        avg_stress = df[stress_col].mean()
        st.metric("📈 Average Stress Level", f"{avg_stress:.2f}")

        # Stress by gender (if available)
        if "gender" in df.columns:
            avg_stress_gender = df.groupby("gender")[stress_col].mean().reset_index()
            fig1 = px.bar(avg_stress_gender, x="gender", y=stress_col, color="gender",
                          title="Average Stress Level by Gender")
            st.plotly_chart(fig1, use_container_width=True)

        # Stress by course load (if available)
        if "course_load" in df.columns:
            avg_stress_course = df.groupby("course_load")[stress_col].mean().reset_index()
            fig2 = px.bar(avg_stress_course, x="course_load", y=stress_col, color=stress_col,
                          color_continuous_scale="Tealgrn", title="Average Stress by Course Load")
            st.plotly_chart(fig2, use_container_width=True)

        # Dynamic recommendations
        st.markdown("### 🧘 Recommendations for Managing Academic Stress")

        if avg_stress > 6:
            st.warning("""
            🔺 **High Stress Detected**
            - Prioritize adequate rest and regular exercise.
            - Use relaxation apps (like Headspace or Calm) for guided mindfulness.
            - Talk to trusted mentors, counselors, or peers for support.
            """)
        elif 4 <= avg_stress <= 6:
            st.info("""
            ⚖️ **Moderate Stress Levels**
            - Maintain a structured study schedule with frequent short breaks.
            - Balance study with hobbies and physical activity.
            - Stay socially connected and avoid burnout.
            """)
        else:
            st.success("""
            🌿 **Low Stress Levels**
            - Keep practicing your healthy habits!
            - Continue regular sleep and positive routines.
            - Offer support to classmates who may be struggling.
            """)

        st.markdown("### 💬 Interpretation")
        st.success("""
        The data shows that stress varies across demographics and academic conditions.  
        Using these insights, students can implement healthier routines and better stress-management techniques.
        """)
    else:
        st.error("⚠️ No stress column found in dataset.")
