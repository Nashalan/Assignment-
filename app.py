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
    ["🏠 Home", "🎯 Stress Overview", "🎓 Academic Factors", "💡 Stress Management & Recommendations"]
)

# ---------------------------------------------------
# PAGE 1 — HOME
# ---------------------------------------------------
if page == "🏠 Home":
    st.title("🏫 Academic Stress Level Dashboard")
    st.markdown("""
    Welcome to the **Academic Stress Visualization Dashboard**!  
    This dashboard helps explore how academic and lifestyle factors influence students' stress levels.

    **Sections Overview:**
    - 🎯 *Stress Overview*: General distribution of student stress  
    - 🎓 *Academic Factors*: Workload, grades, and study habits  
    - 💡 *Stress Management*: Insights and practical tips
    """)

    st.subheader("📘 Dataset Preview")
    st.dataframe(df.head())

    st.info("👉 Use the sidebar to explore stress-related insights and practical recommendations.")

# ---------------------------------------------------
# PAGE 2 — STRESS OVERVIEW
# ---------------------------------------------------
elif page == "🎯 Stress Overview":
    st.title("🎯 Stress Distribution & Overview")

    st.markdown("### 🎯 Objective")
    st.write("To visualize how stress levels are distributed and identify overall stress trends.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    This section explores the **spread of stress levels** and highlights group differences 
    such as gender or age. It helps identify which demographics experience higher stress.
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

        # Stress by age
        if "age" in df.columns:
            fig3 = px.line(df.sort_values("age"), x="age", y=stress_col,
                           title="Stress Level by Age", markers=True)
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("### 💬 Interpretation")
        st.success("""
        The histogram shows that most students report moderate stress levels.  
        Gender and age comparisons reveal how demographic factors influence stress variation.  
        Younger or less experienced students may show higher stress due to adjustment challenges.
        """)
    else:
        st.error("⚠️ No column containing 'stress' found in the dataset.")

# ---------------------------------------------------
# PAGE 3 — ACADEMIC FACTORS
# ---------------------------------------------------
elif page == "🎓 Academic Factors":
    st.title("🎓 Academic Factors Affecting Stress")

    st.markdown("### 🎯 Objective")
    st.write("To investigate how academic workload and performance influence student stress levels.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    Academic elements such as **study hours**, **course load**, and **grades** are often key sources of stress.  
    This section examines how these academic metrics are linked to stress intensity.
    """)

    if stress_col:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        # Correlation with stress
        corr = df[numeric_cols].corr()[stress_col].sort_values(ascending=False).reset_index()
        corr.columns = ['Variable', 'Correlation with Stress']
        fig_corr = px.bar(corr, x='Variable', y='Correlation with Stress', color='Correlation with Stress',
                          color_continuous_scale='RdBu', title="Correlation of Academic Factors with Stress")
        st.plotly_chart(fig_corr, use_container_width=True)

        # Parallel coordinates (to see multi-variable relation)
        if len(numeric_cols) > 3:
            fig_para = px.parallel_coordinates(df, color=stress_col,
                                               color_continuous_scale="Plasma",
                                               dimensions=numeric_cols[:5],
                                               title="Parallel View: Academic Factors vs Stress")
            st.plotly_chart(fig_para, use_container_width=True)

        # Academic scatter (choose variable)
        num_cols = [col for col in numeric_cols if col != stress_col]
        if num_cols:
            x_var = st.selectbox("Select an Academic Variable to Compare with Stress:", num_cols)
            fig_scat = px.scatter(df, x=x_var, y=stress_col, trendline="ols",
                                  color=stress_col, color_continuous_scale="Viridis",
                                  title=f"{x_var.replace('_',' ').title()} vs Stress Level")
            st.plotly_chart(fig_scat, use_container_width=True)

        st.markdown("### 💬 Interpretation")
        st.success("""
        Academic workload shows strong correlations with stress.  
        Students with heavy course loads or lower grades generally report higher stress.  
        Parallel plots highlight how multiple academic pressures combine to raise stress levels.
        """)
    else:
        st.error("⚠️ No stress column found in dataset.")

# ---------------------------------------------------
# PAGE 4 — STRESS MANAGEMENT & RECOMMENDATIONS
# ---------------------------------------------------
elif page == "💡 Stress Management & Recommendations":
    st.title("💡 Stress Management & Recommendations")

    st.markdown("### 🎯 Objective")
    st.write("To identify high-stress patterns in the data and provide personalized tips for stress management.")

    st.markdown("### 📦 Summary Box")
    st.info("""
    Based on data analysis, this section identifies **which student groups experience higher stress**
    and offers **data-driven recommendations** to help manage it effectively.
    """)

    if stress_col:
        # High stress analysis
        high_stress_df = df[df[stress_col] > df[stress_col].mean()]
        avg_stress = df[stress_col].mean()
        st.metric("📈 Average Stress Level", f"{avg_stress:.2f}")

        # Gender-based stress (if available)
        if "gender" in df.columns:
            avg_stress_gender = df.groupby("gender")[stress_col].mean().reset_index()
            fig1 = px.bar(avg_stress_gender, x="gender", y=stress_col, color="gender",
                          title="Average Stress Level by Gender")
            st.plotly_chart(fig1, use_container_width=True)

        # Course Load stress (if available)
        if "course_load" in df.columns:
            avg_stress_course = df.groupby("course_load")[stress_col].mean().reset_index()
            fig2 = px.bar(avg_stress_course, x="course_load", y=stress_col, color=stress_col,
                          color_continuous_scale="Tealgrn", title="Average Stress by Course Load")
            st.plotly_chart(fig2, use_container_width=True)

        # Automated Recommendations
        st.markdown("### 🧘 Recommendations for Reducing Academic Stress")

        if avg_stress > 6:
            st.warning("""
            🔺 **High Stress Detected!**
            - Prioritize rest and schedule regular breaks.
            - Talk to a counselor or academic advisor.
            - Avoid perfectionism; focus on progress.
            """)
        elif 4 <= avg_stress <= 6:
            st.info("""
            ⚖️ **Moderate Stress Observed**
            - Maintain balance between study and recreation.
            - Use time-management tools and planners.
            - Practice relaxation techniques such as deep breathing or light exercise.
            """)
        else:
            st.success("""
            🌿 **Low Stress Levels**
            - Keep up your healthy habits!
            - Continue good sleep, hydration, and balanced study routines.
            - Offer peer support to classmates who might feel overwhelmed.
            """)

        st.markdown("### 💬 Interpretation")
        st.success("""
        The analysis highlights groups under more pressure — for example, 
        certain genders or course loads.  
        The recommendations are generated dynamically based on the dataset’s average stress level, 
        helping interpret patterns into practical, actionable advice.
        """)
    else:
        st.error("⚠️ No stress column found in dataset.")
