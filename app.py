import streamlit as st
import pandas as pd
import unicodedata

st.set_page_config(page_title="Calendario de Ferias Internacionales", layout="wide")

# =========================
# 📡 DATA
# =========================

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIefEBOe9bST2rmGJt_aDSK_jMcrnbGFnNnO97mwUmJROtLcb-DVWJlsSPyOarTHSJeyPq0o7mm3Tu/pub?gid=1507359487&single=true&output=csv"

df = pd.read_csv(url)

# =========================
# 🧹 LIMPIEZA DE DATOS
# =========================

# Limpiar nombres de columnas
df.columns = df.columns.str.strip()

# Limpiar solo columnas de texto
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# Año limpio (simple y directo)
df["Año de edición"] = pd.to_numeric(df["Año de edición"], errors="coerce")
df = df.dropna(subset=["Año de edición"])
df["Año de edición"] = df["Año de edición"].astype(int)

# Fechas
df["Fecha de Inicio"] = pd.to_datetime(df["Fecha de Inicio"], errors="coerce")
df["Fecha de finalización"] = pd.to_datetime(df["Fecha de finalización"], errors="coerce")

# =========================
# 💰 APOYO ECONÓMICO
# =========================

def limpiar_texto(texto):
    if pd.isna(texto):
        return ""
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

col_apoyo = "¿Ofrece apoyo económico a la participación?"

df["apoyo_normalizado"] = df[col_apoyo].apply(limpiar_texto)

df["Apoyo limpio"] = "Otro"

df.loc[df["apoyo_normalizado"].str.contains("si", na=False), "Apoyo limpio"] = "Sí"
df.loc[df["apoyo_normalizado"].str.contains("no", na=False), "Apoyo limpio"] = "No"

# =========================
# 🧭 HEADER
# =========================

col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("logo.png", width=240)

with col2:
    st.markdown("## Calendario de Ferias Internacionales")
    st.markdown("Una iniciativa del Departamento de Negocios Internacionales de la Cámara de Comercio y Servicios del Uruguay.")

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
    anios = st.multiselect("Año", sorted(df["Año de edición"].unique()))

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

        fecha_inicio = row["Fecha de Inicio"].strftime("%d/%m/%Y") if pd.notna(row["Fecha de Inicio"]) else "No disponible"
        fecha_fin = row["Fecha de finalización"].strftime("%d/%m/%Y") if pd.notna(row["Fecha de finalización"]) else "No disponible"

        st.markdown(f"📅 {fecha_inicio} → {fecha_fin}")
        st.markdown(f"📊 Expositores: {row['Cantidad estimada de expositores']} | Visitantes: {row['Cantidad estimada de visitantes']}")

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
**Lic. Mateo Fagúndez - Departamento de Negocios Internacionales**  
📧 comex@cncs.com.uy  
""")
