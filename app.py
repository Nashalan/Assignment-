import streamlit as st
import pandas as pd

st.set_page_config(page_title="Academic Stress Level Dashboard", layout="wide")

st.title("📊 Academic Stress Level Dashboard")
st.markdown("""
Welcome to the **Academic Stress Level Visualization App**.  
This dashboard explores how stress levels vary among students and the factors that influence them.

### 📘 Pages
- **Stress Level Distribution:** Explore how stress varies among students.  
- **Academic Factors & Stress:** Examine how academic variables like GPA or study hours relate to stress.  
- **Lifestyle Factors & Stress:** Discover how sleep and physical activity impact stress.

The dataset used is from:
[Academic Stress Level.csv](https://raw.githubusercontent.com/Nashalan/Assignment-/refs/heads/main/Academic%20Stress%20Level.csv)
""")

# Load and preview data
DATA_URL = "https://raw.githubusercontent.com/Nashalan/Assignment-/refs/heads/main/Academic%20Stress%20Level.csv"
@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

df = load_data()

st.subheader("📂 Dataset Preview")

# Sidebar navigation
st.sidebar.title("📊 Academic Stress Dashboard")
page = st.sidebar.radio(
    "Select a section:",
    ["Stress Distribution", "Academic Factors & Stress", "Lifestyle Factors & Stress"]
)

# PAGE 1
if page == "Stress Distribution":
    st.title("🎯 Stress Level Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['Stress Level'], kde=True, color="skyblue", ax=ax)
    st.pyplot(fig)

# PAGE 2
elif page == "Academic Factors & Stress":
    st.title("🎓 Academic Factors & Stress")
    fig = px.scatter(df, x='Study Hours', y='Stress Level', trendline="ols")
    st.plotly_chart(fig)

# PAGE 3
elif page == "Lifestyle Factors & Stress":
    st.title("💤 Lifestyle Factors & Stress")
    fig = px.scatter_3d(df, x='Sleep Duration', y='Physical Activity', z='Stress Level', color='Stress Level')
    st.plotly_chart(fig)

st.dataframe(df.head())
