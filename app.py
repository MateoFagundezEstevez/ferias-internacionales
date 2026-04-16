import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ferias Internacionales", layout="wide")

# =========================
# 📡 DATA
# =========================

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIefEBOe9bST2rmGJt_aDSK_jMcrnbGFnNnO97mwUmJROtLcb-DVWJlsSPyOarTHSJeyPq0o7mm3Tu/pub?gid=1507359487&single=true&output=csv"

df = pd.read_csv(url)

# Limpiar columnas
df.columns = df.columns.str.strip()

# =========================
# 🧹 LIMPIEZA DE DATOS
# =========================

# Año como entero (FIX CLAVE)
df["Año de edición"] = pd.to_numeric(df["Año de edición"], errors="coerce").astype("Int64")

# Limpiar textos
df["País"] = df["País"].astype(str).str.strip()
df["Industria / Sector"] = df["Industria / Sector"].astype(str).str.strip()
df["¿Ofrece apoyo económico a la participación?"] = df["¿Ofrece apoyo económico a la participación?"].astype(str).str.strip()

# Fecha
df["Fecha de Inicio"] = pd.to_datetime(df["Fecha de Inicio"], errors="coerce")

# =========================
# 🧭 HEADER
# =========================

col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("logo.png", width=240)

with col2:
    st.markdown("## Ferias Internacionales")
    st.markdown("Cámara de Comercio y Servicios del Uruguay")

with col3:
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
    paises = st.multiselect("País", sorted(df["País"].dropna().unique()))

with col2:
    sectores = st.multiselect("Sector", sorted(df["Industria / Sector"].dropna().unique()))

with col3:
    anios = st.multiselect("Año", sorted(df["Año de edición"].dropna().unique()))

with col4:
    apoyo = st.selectbox("Apoyo económico", ["Todos", "Sí", "No"])

# =========================
# 🔎 APLICAR FILTROS
# =========================

df_filtrado = df.copy()

if paises:
    df_filtrado = df_filtrado[df_filtrado["País"].isin(paises)]

if sectores:
    df_filtrado = df_filtrado[df_filtrado["Industria / Sector"].isin(sectores)]

if anios:
    df_filtrado = df_filtrado[df_filtrado["Año de edición"].isin(anios)]

if apoyo != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["¿Ofrece apoyo económico a la participación?"]
        .str.contains(apoyo, case=False, na=False)
    ]

# =========================
# 📊 ORDENAR
# =========================

df_filtrado = df_filtrado.sort_values(by="Fecha de Inicio")

st.divider()

# =========================
# 📦 RESULTADOS
# =========================

for _, row in df_filtrado.iterrows():
    with st.container():

        st.subheader(row["Nombre de la feria"])

        st.markdown(f"**📍 {row['Ciudad']}, {row['País']}**")
        st.markdown(f"🏭 {row['Industria / Sector']} — {row['Subsector']}")

        fecha_inicio = row["Fecha de Inicio"].date() if pd.notna(row["Fecha de Inicio"]) else "No disponible"

        st.markdown(f"📅 {fecha_inicio} → {row['Fecha de finalización']}")
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
📧 comex@cncs.com.uy 
""")
