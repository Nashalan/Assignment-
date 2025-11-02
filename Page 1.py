import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import plotly.express as px

st.title("🎯 Objective 1: Explore Academic Stress Distribution")
st.markdown("**Objective Statement:** To understand how academic stress levels vary among students.")

st.info("""
**Summary:**  
This section visualizes the distribution of academic stress levels across students.  
The aim is to identify typical stress patterns, potential outliers, and group differences.
""")

# Load dataset
DATA_URL = "https://raw.githubusercontent.com/Nashalan/Assignment-/refs/heads/main/Academic%20Stress%20Level.csv"
@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

df = load_data()

# Visualization 1: Histogram
st.subheader("1️⃣ Stress Level Distribution (Histogram)")
fig, ax = plt.subplots()
sns.histplot(df['Stress Level'], kde=True, color="skyblue", ax=ax)
st.pyplot(fig)

# Visualization 2: Boxplot
st.subheader("2️⃣ Boxplot of Stress Levels")
fig, ax = plt.subplots()
sns.boxplot(x=df['Stress Level'], color="lightcoral", ax=ax)
st.pyplot(fig)

# Visualization 3: Pie Chart (Gender if available)
if 'Gender' in df.columns:
    st.subheader("3️⃣ Average Stress by Gender")
    avg_stress = df.groupby('Gender')['Stress Level'].mean().reset_index()
    fig = px.pie(avg_stress, names='Gender', values='Stress Level', title='Average Stress by Gender')
    st.plotly_chart(fig)

st.success("""
**Interpretation:**  
The visuals highlight how stress is distributed among students, showing common levels and any gender-based differences.  
This helps identify where interventions might be most needed.
""")
