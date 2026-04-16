import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ferias Internacionales", layout="wide")

# URL de tu Google Sheet en CSV
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIefEBOe9bST2rmGJt_aDSK_jMcrnbGFnNnO97mwUmJROtLcb-DVWJlsSPyOarTHSJeyPq0o7mm3Tu/pub?gid=1507359487&single=true&output=csv"

# Cargar datos
df = pd.read_csv(url)

# Limpiar nombres de columnas (clave para evitar errores)
df.columns = df.columns.str.strip()

# Título
st.title("🌎 Ferias Internacionales")
st.markdown("Explorá oportunidades comerciales globales actualizadas en tiempo real.")

# 🔍 Buscador
busqueda = st.text_input("Buscar feria")

if busqueda:
    df = df[df.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)]

# 📊 Filtros dinámicos (solo si existen las columnas)
col1, col2 = st.columns(2)

with col1:
    if "Pais" in df.columns:
        paises = st.multiselect("Filtrar por país", df["Pais"].dropna().unique())
        if paises:
            df = df[df["Pais"].isin(paises)]

with col2:
    if "Sector" in df.columns:
        sectores = st.multiselect("Filtrar por sector", df["Sector"].dropna().unique())
        if sectores:
            df = df[df["Sector"].isin(sectores)]

st.divider()

# 📦 Mostrar como "cards"
for _, row in df.iterrows():
    with st.container():
        
        # Nombre de la feria (ajustá si tu columna se llama distinto)
        nombre = row["Nombre Feria"] if "Nombre Feria" in df.columns else "Feria sin nombre"
        st.subheader(nombre)

        col1, col2, col3 = st.columns(3)

        with col1:
            if "Pais" in df.columns:
                st.write("📍", row["Pais"])

        with col2:
            if "Sector" in df.columns:
                st.write("🏭", row["Sector"])

        with col3:
            if "Fecha" in df.columns:
                st.write("📅", row["Fecha"])

        # Link opcional
        if "Link" in df.columns:
            if pd.notna(row["Link"]):
                st.markdown(f"[🔗 Ver más]({row['Link']})")

        st.divider()
