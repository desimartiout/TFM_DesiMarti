import streamlit as st
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Simulación de datos
heatmap_data = pd.DataFrame(
    np.random.randint(50, 100, size=(5, 5)), 
    columns=[f"Context {i}" for i in range(1, 6)],
    index=[f"Query {i}" for i in range(1, 6)]
)

st.subheader("Heatmap de Context Recall por Consulta")

# Heatmap con Seaborn
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", fmt="d", ax=ax)
plt.title("Rendimiento del Context Recall")
st.pyplot(fig)