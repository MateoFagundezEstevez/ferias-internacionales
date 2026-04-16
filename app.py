import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ferias Internacionales", layout="wide")

# URL de tu Google Sheet en CSV
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIefEBOe9bST2rmGJt_aDSK_jMcrnbGFnNnO97mwUmJROtLcb-DVWJlsSPyOarTHSJeyPq0o7mm3Tu/pub?gid=1507359487&single=true&output=csv"

df = pd.read_csv(url)

st.title("🌎 Ferias Internacionales")

# Buscador
busqueda = st.text_input("Buscar feria")

if busqueda:
    df = df[df.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)]

# Mostrar datos
for _, row in df.iterrows():
    with st.container():
        st.subheader(row[0])
        st.write("📍", row[1])
        st.write("🏭", row[2])
        st.write("📅", row[3])
        st.divider()
