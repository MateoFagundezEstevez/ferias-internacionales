import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ferias Internacionales", layout="wide")

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIefEBOe9bST2rmGJt_aDSK_jMcrnbGFnNnO97mwUmJROtLcb-DVWJlsSPyOarTHSJeyPq0o7mm3Tu/pub?gid=1507359487&single=true&output=csv"

df = pd.read_csv(url)

# Limpiar nombres de columnas
df.columns = df.columns.str.strip()

st.title("🌎 Ferias Internacionales")
st.markdown("Explorá oportunidades comerciales para empresas uruguayas")

# 🔍 Buscador
busqueda = st.text_input("Buscar feria, país o sector")

if busqueda:
    df = df[df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)]

st.divider()

# 📦 Mostrar ferias
for _, row in df.iterrows():
    with st.container():

        st.subheader(row["Nombre de la feria"])

        st.write(f"📍 {row['Ciudad']}, {row['País']}")
        st.write(f"🏭 {row['Industria / Sector']} | {row['Subsector']}")
        st.write(f"📅 {row['Fecha de Inicio']} → {row['Fecha de finalización']}")
        st.write(f"📊 Expositores: {row['Cantidad estimada de expositores']} | Visitantes: {row['Cantidad estimada de visitantes']}")
        st.write(f"💰 Apoyo: {row['¿Ofrece apoyo económico a la participación?']}")

        if pd.notna(row["Fecha límite para postular al apoyo"]):
            st.write(f"⏳ Postulación hasta: {row['Fecha límite para postular al apoyo']}")

        if pd.notna(row["Más info (página web):"]):
            st.markdown(f"[🔗 Más información]({row['Más info (página web):']})")

        st.divider()
