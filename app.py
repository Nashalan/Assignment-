import streamlit as st

st.set_page_config(
  page_title="Academic Stress Level"
)

st.header("Academic Stress Level",divider="gray")

import pandas as pd

# Load the uploaded file
file_path = "/mnt/data/Academic Stress Level.csv"
df = pd.read_csv(file_path)

# Display the first few rows to understand its structure
df.head()

import matplotlib.pyplot as plt

stage_stress = df.groupby('Your Academic Stage')['Rate your academic stress index   '].mean()
stage_stress.plot(kind='bar')
plt.title('Average Academic Stress by Stage')
plt.xlabel('Academic Stage')
plt.ylabel('Average Stress Index')
st.pyplot(plt)

st.write(
  """
  Undergraduate students generally show higher stress levels compared to other stages. 
  This may indicate that early academic years bring more pressure due to adaptation and workload.
  """
)

  
