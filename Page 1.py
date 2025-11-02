import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("🎯 Objective 1: Stress Level Distribution")
st.markdown("**Objective Statement:** To understand how academic stress levels vary among students.")

st.info("""
**Summary:**  
This section visualizes the overall distribution of academic stress levels.  
It identifies common stress levels, potential outliers, and patterns across demographic groups.
""")

# Load data
DATA_URL = "https://raw.githubusercontent.com/Nashalan/Assignment-/refs/heads/main/Academic%20Stress%20Level.csv"
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df = load_data()

# Visualization 1: Histogram
st.subheader("1️⃣ Stress Level Distribution")
fig, ax = plt.subplots()
sns.histplot(df['stress_level'], kde=True, color="skyblue", ax=ax)
st.pyplot(fig)

# Visualization 2: Boxplot
st.subheader("2️⃣ Boxplot of Stress Levels")
fig, ax = plt.subplots()
sns.boxplot(x=df['stress_level'], color="lightcoral", ax=ax)
st.pyplot(fig)

# Visualization 3: Pie Chart (if gender exists)
if 'gender' in df.columns:
    st.subheader("3️⃣ Average Stress by Gender")
    avg_stress = df.groupby('gender')['stress_level'].mean().reset_index()
    fig = px.pie(avg_stress, names='gender', values='stress_level', title='Average Stress by Gender')
    st.plotly_chart(fig)

st.success("""
**Interpretation:**  
These plots show how stress levels are distributed among students.  
Peaks indicate typical stress levels, while outliers show extreme cases.  
Gender comparison reveals any demographic differences in stress perception.
""")
