import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("💤 Objective 3: Lifestyle Factors & Stress")
st.markdown("**Objective Statement:** To explore how sleep and physical activity influence stress levels.")

st.info("""
**Summary:**  
This section investigates lifestyle habits and their impact on academic stress.  
Healthy routines, such as proper sleep and regular exercise, may help lower stress.
""")

# Load data
DATA_URL = "https://raw.githubusercontent.com/Nashalan/Assignment-/refs/heads/main/Academic%20Stress%20Level.csv"
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()

# Visualization 1: Sleep vs Stress
if 'sleep_duration' in df.columns:
    st.subheader("1️⃣ Sleep Duration vs Stress Level")
    fig = px.scatter(df, x='sleep_duration', y='stress_level', color='sleep_duration',
                     color_continuous_scale='viridis')
    st.plotly_chart(fig)

# Visualization 2: Physical Activity vs Stress
if 'physical_activity' in df.columns:
    st.subheader("2️⃣ Stress Level by Physical Activity")
    fig, ax = plt.subplots()
    sns.boxplot(x='physical_activity', y='stress_level', data=df, palette='coolwarm', ax=ax)
    st.pyplot(fig)

# Visualization 3: 3D Plot
if all(c in df.columns for c in ['sleep_duration', 'physical_activity', 'stress_level']):
    st.subheader("3️⃣ 3D Plot: Sleep, Activity & Stress")
    fig = px.scatter_3d(df, x='sleep_duration', y='physical_activity', z='stress_level', color='stress_level')
    st.plotly_chart(fig)

st.success("""
**Interpretation:**  
These visualizations suggest that students with better sleep and active lifestyles report lower stress levels.  
This highlights the importance of healthy habits for academic and emotional well-being.
""")
