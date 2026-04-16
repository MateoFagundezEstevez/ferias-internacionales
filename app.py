import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calendario de Ferias Internacionales", layout="wide")

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

# Limpiar columnas
df.columns = df.columns.str.strip()

# Limpiar solo texto (FIX)
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# Año limpio
df["Año de edición"] = (
    df["Año de edición"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)
df["Año de edición"] = pd.to_numeric(df["Año de edición"], errors="coerce").astype("Int64")

# Fecha
df["Fecha de Inicio"] = pd.to_datetime(df["Fecha de Inicio"], errors="coerce")

# =========================
# 💰 APOYO ECONÓMICO (VECTORIAL)
# =========================

col_apoyo = "¿Ofrece apoyo económico a la participación?"

df[col_apoyo] = df[col_apoyo].astype(str).str.lower()

df["Apoyo limpio"] = "Otro"

df.loc[
    df[col_apoyo].str.contains("si", case=False, na=False),
    "Apoyo limpio"
] = "Sí"

df.loc[
    df[col_apoyo].str.contains("no", case=False, na=False),
    "Apoyo limpio"
] = "No"

# =========================
# 🧭 HEADER
# =========================

col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("logo.png", width=240)

with col2:
    st.markdown("## Calendario de Ferias Internacionales")
    st.markdown("Una inicativa del departamento de Negocios Internacionales de la Cámara de Comercio y Servicios del Uruguay para nuclear la oferta de Ferias Internacionales, clave para su diversificación e inserción comercial.")
    st.markdown("Algunas de estas ferias ofrecen apoyo económico a la participación, existe un filtro para encontrarlas, aplíquelo y si tiene dudas, contáctenos al mail al pie de la página.")

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
    df_filtrado = df_filtrado[df_filtrado["Apoyo limpio"] == apoyo]

# =========================
# 📊 ORDENAR
# =========================

df_filtrado = df_filtrado.sort_values(by="Fecha de Inicio")

st.divider()

# =========================
# 📦 RESULTADOS
# =========================

st.markdown(f"**Resultados encontrados: {len(df_filtrado)}**")

for _, row in df_filtrado.iterrows():
    with st.container():

        st.subheader(row["Nombre de la feria"])

        st.markdown(f"**📍 {row['Ciudad']}, {row['País']}**")
        st.markdown(f"🏭 {row['Industria / Sector']} — {row['Subsector']}")

        fecha_inicio = row["Fecha de Inicio"].date() if pd.notna(row["Fecha de Inicio"]) else "No disponible"

        st.markdown(f"📅 {fecha_inicio} → {row['Fecha de finalización']}")
        st.markdown(f"📊 Expositores: {row['Cantidad estimada de expositores']} | Visitantes: {row['Cantidad estimada de visitantes']}")

        # Badge visual
        if row["Apoyo limpio"] == "Sí":
            st.markdown("🟢 **Apoyo disponible**")
        elif row["Apoyo limpio"] == "No":
            st.markdown("🔴 **Sin apoyo**")

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
**Lic. Mateo Fagúndez - Departamento de Negocios Internacionales de la Cámara de Comercio y Servicios del Uruguay**  
📧 comex@cncs.com.uy  
""")
