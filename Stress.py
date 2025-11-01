import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# --- Load Dataset from GitHub ---
url = "https://raw.githubusercontent.com/Nashalan/Tutorial/refs/heads/main/Academic%20Stress%20Level.csv"
df = pd.read_csv(url)

# --- Clean column names ---
df.columns = df.columns.str.strip()

st.title("📊 Academic Stress Analysis Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(label='PLO 2', value=f'3.5',help='PLO 2: Cognitive skill',border=True)
col2.metric(label='PLO 3', value=f'3.5',help='PLO 3: Digital skill',border=True)
col3.metric(label='PLO 4', value=f'4.0',help='PLO 4: Interpersonal skill',border=True)
col1.metric(label='PLO 5', value=f'4.3',help='PLO 2: Communication skill',border=True)

# --- 1️⃣ Average Academic Stress by Stage ---
st.subheader("1️⃣ Average Academic Stress by Stage")
if 'Your Academic Stage' in df.columns and 'Rate your academic stress index' in df.columns:
    stage_stress = df.groupby('Your Academic Stage')['Rate your academic stress index'].mean()
    st.bar_chart(stage_stress)
    st.markdown("""
    **Interpretation:**  
    Undergraduate students generally show higher stress levels compared to other stages.  
    This may indicate that early academic years bring more pressure due to adaptation and workload.
    """)
else:
    st.warning("Columns for academic stage or stress index not found in dataset.")

# --- 3️⃣ Study Environment Distribution ---
st.subheader("3️⃣ Study Environment Distribution")
if 'Study Environment' in df.columns:
    env_counts = df['Study Environment'].value_counts().reset_index()
    env_counts.columns = ['Study Environment', 'Count']
    fig3 = px.pie(
        env_counts,
        names='Study Environment',
        values='Count',
        title='Study Environment Distribution',
        hole=0.4
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
    **Interpretation:**  
    Most students report studying in a peaceful environment, but a notable portion face noisy surroundings.  
    A noisy environment could be linked to higher stress levels.
    """)
else:
    st.warning("Study Environment column not found in dataset.")

# --- 4️⃣ Coping Strategies Used by Students ---
st.subheader("4️⃣ Coping Strategies Used by Students")
if 'What coping strategy you use as a student?' in df.columns:
    coping_counts = df['What coping strategy you use as a student?'].value_counts().reset_index()
    coping_counts.columns = ['Coping Strategy', 'Count']
    fig4 = px.bar(
        coping_counts.head(10),
        x='Count',
        y='Coping Strategy',
        orientation='h',
        color='Coping Strategy',
        title='Top 10 Coping Strategies Used by Students'
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("""
    **Interpretation:**  
    Students often use logical and social coping strategies such as analyzing situations or seeking social support.  
    These indicate proactive stress management approaches.
    """)
else:
    st.warning("Coping strategy column not found in dataset.")

# --- 5️⃣ Peer Pressure vs Stress Index ---
st.subheader("5️⃣ Peer Pressure vs Academic Stress Index")
if 'Peer pressure' in df.columns and 'Rate your academic stress index' in df.columns:
    fig5 = px.scatter(
        df,
        x='Peer pressure',
        y='Rate your academic stress index',
        color='Peer pressure',
        title='Peer Pressure vs Academic Stress Index',
        trendline='ols'
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("""
    **Interpretation:**  
    A positive trend appears between peer pressure and stress index.  
    Students under higher peer pressure tend to experience more academic stress.
    """)
else:
    st.warning("Columns for peer pressure or stress index not found in dataset.")
