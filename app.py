import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load Dataset from GitHub ---
url = "https://raw.githubusercontent.com/Nashalan/Tutorial/refs/heads/main/Academic%20Stress%20Level.csv"
df = pd.read_csv(url)
df.columns = df.columns.str.strip()
stage_stress = df.groupby('Your Academic Stage')['Rate your academic stress index'].mean()



st.title("📊 Academic Stress Analysis Dashboard")

# --- 1️⃣ Average Academic Stress by Stage ---
st.subheader("1️⃣ Average Academic Stress by Stage")
stage_stress = df.groupby('Your Academic Stage')['Rate your academic stress index   '].mean()
st.bar_chart(stage_stress)

st.markdown("""
**Interpretation:**  
Undergraduate students generally show higher stress levels compared to other stages.  
This may indicate that early academic years bring more pressure due to adaptation and workload.
""")

# --- 2️⃣ Home Pressure vs Stress Index ---
st.subheader("2️⃣ Home Pressure vs Stress Index")
fig2, ax2 = plt.subplots()
sns.boxplot(
    x='Academic pressure from your home',
    y='Rate your academic stress index   ',
    data=df,
    ax=ax2
)
ax2.set_title('Home Academic Pressure vs Stress Index')
st.pyplot(fig2)

st.markdown("""
**Interpretation:**  
Students with higher academic pressure from home exhibit greater stress index values,  
suggesting that parental expectations significantly influence academic stress.
""")

# --- 3️⃣ Study Environment Distribution ---
st.subheader("3️⃣ Study Environment Distribution")
env_counts = df['Study Environment'].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(env_counts, labels=env_counts.index, autopct='%1.1f%%', startangle=90)
ax3.set_title('Study Environment Distribution')
st.pyplot(fig3)

st.markdown("""
**Interpretation:**  
Most students report studying in a peaceful environment, but a notable portion face noisy surroundings.  
A noisy environment could be linked to higher stress levels.
""")

# --- 4️⃣ Coping Strategies Used by Students ---
st.subheader("4️⃣ Coping Strategies Used by Students")
coping_counts = df['What coping strategy you use as a student?'].value_counts().head(10)
st.bar_chart(coping_counts)

st.markdown("""
**Interpretation:**  
Students often use logical and social coping strategies such as analyzing situations or seeking social support.  
These indicate proactive stress management approaches.
""")

# --- 5️⃣ Peer Pressure vs Stress Index ---
st.subheader("5️⃣ Peer Pressure vs Academic Stress Index")
fig5, ax5 = plt.subplots()
ax5.scatter(df['Peer pressure'], df['Rate your academic stress index   '])
ax5.set_xlabel('Peer Pressure')
ax5.set_ylabel('Stress Index')
ax5.set_title('Peer Pressure vs Academic Stress Index')
st.pyplot(fig5)

st.markdown("""
**Interpretation:**  
A positive trend appears between peer pressure and stress index.  
Students under higher peer pressure tend to experience more academic stress.
""")
