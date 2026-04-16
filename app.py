import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ferias Internacionales", layout="wide")

# Tu CSV
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIefEBOe9bST2rmGJt_aDSK_jMcrnbGFnNnO97mwUmJROtLcb-DVWJlsSPyOarTHSJeyPq0o7mm3Tu/pub?gid=1507359487&single=true&output=csv"

df = pd.read_csv(url)

# Limpiar nombres de columnas
df.columns = df.columns.str.strip().str.lower()

st.title("🌎 Ferias Internacionales")

# Buscador simple
busqueda = st.text_input("Buscar")

if busqueda:
    df = df[df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)]

st.divider()

# Mostrar datos
for _, row in df.iterrows():
    
    nombre = row[[c for c in df.columns if "feria" in c or "nombre" in c][0]]
    pais = row[[c for c in df.columns if "pais" in c][0]] if any("pais" in c for c in df.columns) else ""
    sector = row[[c for c in df.columns if "sector" in c][0]] if any("sector" in c for c in df.columns) else ""
    fecha = row[[c for c in df.columns if "fecha" in c][0]] if any("fecha" in c for c in df.columns) else ""

    st.subheader(nombre)
    st.write(f"📍 {pais} | 🏭 {sector} | 📅 {fecha}")
    st.divider()
