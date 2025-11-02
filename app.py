import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Academic Stress Dashboard", layout="wide")

# Load data
DATA_URL = "https://raw.githubusercontent.com/Nashalan/Assignment-/refs/heads/main/Academic%20Stress%20Level.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df
    
df = load_data()
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# ------------------------
# Sidebar menu
# ------------------------
st.sidebar.title("📊 Academic Stress Dashboard")
page = st.sidebar.radio(
    "Select a Section:",
    ["Home", "Stress Distribution", "Academic Factors", "Lifestyle Factors"]
)

# ------------------------
# Home Page
# ------------------------
if page == "Home":
    st.title("🏠 Academic Stress Level Dashboard")
    st.markdown("""
    This app visualizes how students experience **academic stress** and which factors affect it.
    
    **Sections:**
    - 📈 Stress Distribution
    - 🎓 Academic Factors
    - 💤 Lifestyle Factors
    """)
    st.dataframe(df.head())

# ------------------------
# Stress Distribution
# ------------------------
elif page == "Stress Distribution":
    st.title("🎯 Stress Level Distribution")
    fig, ax = plt.subplots()
    # Find the column that contains the word "stress"
stress_col = next((c for c in df.columns if 'stress' in c.lower()), None)

if stress_col:
    sns.histplot(df[stress_col], kde=True, color="skyblue", ax=ax)
else:
    st.error("⚠️ No column containing 'stress' found. Check dataset column names above.")

    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.boxplot(x=df['stress_level'], color="lightcoral", ax=ax)
    st.pyplot(fig)

    if 'gender' in df.columns:
        avg_stress = df.groupby('gender')['stress_level'].mean().reset_index()
        fig = px.pie(avg_stress, names='gender', values='stress_level', title='Average Stress by Gender')
        st.plotly_chart(fig)

# ------------------------
# Academic Factors
# ------------------------
elif page == "Academic Factors":
    st.title("🎓 Academic Factors & Stress")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    x_axis = st.selectbox("Select academic variable:", numeric_cols, index=0)

    fig = px.scatter(df, x=x_axis, y='stress_level', trendline="ols")
    st.plotly_chart(fig)

    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# ------------------------
# Lifestyle Factors
# ------------------------
elif page == "Lifestyle Factors":
    st.title("💤 Lifestyle Factors & Stress")

    if 'sleep_duration' in df.columns:
        fig = px.scatter(df, x='sleep_duration', y='stress_level', color='sleep_duration', color_continuous_scale='viridis')
        st.plotly_chart(fig)

    if 'physical_activity' in df.columns:
        fig, ax = plt.subplots()
        sns.boxplot(x='physical_activity', y='stress_level', data=df, palette='coolwarm', ax=ax)
        st.pyplot(fig)

    if all(c in df.columns for c in ['sleep_duration', 'physical_activity', 'stress_level']):
        fig = px.scatter_3d(df, x='sleep_duration', y='physical_activity', z='stress_level', color='stress_level')
        st.plotly_chart(fig)
