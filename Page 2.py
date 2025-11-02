import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("🎓 Objective 2: Analyze Academic Factors & Stress")
st.markdown("**Objective Statement:** To examine how academic performance and workload affect stress levels.")

st.info("""
**Summary:**  
This section analyzes how academic metrics (like GPA and study hours) relate to stress.  
Identifying these correlations can reveal whether performance pressure increases stress.
""")

# Load dataset
DATA_URL = "https://raw.githubusercontent.com/Nashalan/Assignment-/refs/heads/main/Academic%20Stress%20Level.csv"
@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

df = load_data()

# Select variable
numeric_cols = df.select_dtypes(include='number').columns.tolist()
x_axis = st.selectbox("Select academic variable to compare with Stress Level:", numeric_cols, index=1)

# Visualization 1: Scatter Plot
st.subheader(f"1️⃣ Scatter Plot: {x_axis} vs Stress Level")
fig = px.scatter(df, x=x_axis, y='Stress Level', trendline="ols", color_discrete_sequence=['teal'])
st.plotly_chart(fig)

# Visualization 2: Heatmap
st.subheader("2️⃣ Correlation Heatmap")
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Visualization 3: Pairplot
academic_vars = [col for col in ['GPA', 'Study Hours', 'Stress Level'] if col in df.columns]
if len(academic_vars) >= 2:
    sns.pairplot(df[academic_vars], diag_kind="kde")
    st.pyplot(plt.gcf())

st.success("""
**Interpretation:**  
The results show whether high study hours or low GPA relate to increased stress.  
Understanding these relationships can help educators design better academic support programs.
""")
