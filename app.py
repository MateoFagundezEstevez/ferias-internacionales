import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ferias Internacionales", layout="wide")

# =========================
# 📡 DATA
# =========================

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIefEBOe9bST2rmGJt_aDSK_jMcrnbGFnNnO97mwUmJROtLcb-DVWJlsSPyOarTHSJeyPq0o7mm3Tu/pub?gid=1507359487&single=true&output=csv"

df = pd.read_csv(url)
df.columns = df.columns.str.strip()

# =========================
# 🧭 HEADER
# =========================

col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("logo.png", width=220)

with col2:
    st.markdown("## Ferias Internacionales")
    st.markdown("Cámara de Comercio y Servicios del Uruguay")

with col3:
    st.markdown("## Consultar")
    st.markdown("[📧 Contacto](mailto:comex@cncs.com.uy)")

st.divider()

# =========================
# 🔍 BUSCADOR
# =========================

busqueda = st.text_input("Buscar feria, país o sector")

if busqueda:
    df = df[df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)]

# =========================
# 🎯 FILTROS
# =========================

st.markdown("### 🔎 Filtrar oportunidades")

col1, col2, col3, col4 = st.columns(4)

with col1:
    paises = st.multiselect("País", df["País"].dropna().unique())

with col2:
    sectores = st.multiselect("Sector", df["Industria / Sector"].dropna().unique())

with col3:
    anios = st.multiselect("Año", df["Año de edición"].dropna().unique())

with col4:
    apoyo = st.selectbox(
        "Apoyo económico",
        ["Todos", "Sí", "No"]
    )

# Aplicar filtros
df_filtrado = df.copy()

if paises:
    df_filtrado = df_filtrado[df_filtrado["País"].isin(paises)]

if sectores:
    df_filtrado = df_filtrado[df_filtrado["Industria / Sector"].isin(sectores)]

if anios:
    df_filtrado = df_filtrado[df_filtrado["Año de edición"].isin(anios)]

if apoyo != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["¿Ofrece apoyo económico a la participación?"].str.contains(apoyo, case=False, na=False)
    ]

st.divider()

# =========================
# 📦 RESULTADOS
# =========================

for _, row in df_filtrado.iterrows():
    with st.container():

        st.subheader(row["Nombre de la feria"])

        st.markdown(f"**📍 {row['Ciudad']}, {row['País']}**")
        st.markdown(f"🏭 {row['Industria / Sector']} — {row['Subsector']}")
        st.markdown(f"📅 {row['Fecha de Inicio']} → {row['Fecha de finalización']}")
        st.markdown(f"📊 Expositores: {row['Cantidad estimada de expositores']} | Visitantes: {row['Cantidad estimada de visitantes']}")
        st.markdown(f"💰 Apoyo: {row['¿Ofrece apoyo económico a la participación?']}")

        if pd.notna(row["Fecha límite para postular al apoyo"]):
            st.markdown(f"⏳ Postulación hasta: {row['Fecha límite para postular al apoyo']}")

        if pd.notna(row["Más info (página web):"]):
            st.markdown(f"[🔗 Más información]({row['Más info (página web):']})")

        st.divider()

# =========================
# 📧 FOOTER
# =========================

st.markdown("""
---
**Cámara de Comercio y Servicios del Uruguay**  
📧 internacionales@ccsu.org.uy  
""")
