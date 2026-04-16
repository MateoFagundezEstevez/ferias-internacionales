import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Ferias Internacionales", layout="wide")

col1, col2 = st.columns([1, 4])

with col1:
    st.image("logo.png", width=220)

with col2:
    st.title("Ferias Internacionales")
    st.markdown("Departamento de Negocios Internacionales de la Cámara de Comercio y Servicios del Uruguay - Lic. Mateo Fagúndez")

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIefEBOe9bST2rmGJt_aDSK_jMcrnbGFnNnO97mwUmJROtLcb-DVWJlsSPyOarTHSJeyPq0o7mm3Tu/pub?gid=1507359487&single=true&output=csv"

df = pd.read_csv(url)
df.columns = df.columns.str.strip()

st.title("🌎 Ferias Internacionales")

# =========================
# 🔍 FILTROS
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    paises = st.multiselect("País", df["País"].dropna().unique())

with col2:
    sectores = st.multiselect("Sector", df["Industria / Sector"].dropna().unique())

with col3:
    anios = st.multiselect("Año", df["Año de edición"].dropna().unique())

# Aplicar filtros
df_filtrado = df.copy()

if paises:
    df_filtrado = df_filtrado[df_filtrado["País"].isin(paises)]

if sectores:
    df_filtrado = df_filtrado[df_filtrado["Industria / Sector"].isin(sectores)]

if anios:
    df_filtrado = df_filtrado[df_filtrado["Año de edición"].isin(anios)]

st.divider()

# =========================
# 📦 MOSTRAR FERIAS
# =========================

for _, row in df_filtrado.iterrows():
    with st.container():

        st.subheader(row["Nombre de la feria"])

        st.write(f"📍 {row['Ciudad']}, {row['País']}")
        st.write(f"🏭 {row['Industria / Sector']} | {row['Subsector']}")
        st.write(f"📅 {row['Fecha de Inicio']} → {row['Fecha de finalización']}")
        st.write(f"📊 Expositores: {row['Cantidad estimada de expositores']} | Visitantes: {row['Cantidad estimada de visitantes']}")

        if pd.notna(row["Más info (página web):"]):
            st.markdown(f"[🔗 Más información]({row['Más info (página web):']})")

        st.divider()

# =========================
# 🔔 ALERTAS (registro simple)
# =========================

st.header("🔔 Recibir alertas de nuevas ferias")

email = st.text_input("Tu email")

if st.button("Activar alerta"):
    
    if email:

        nueva_alerta = pd.DataFrame([{
            "email": email,
            "paises": ",".join(paises),
            "sectores": ",".join(sectores),
            "anios": ",".join(map(str, anios))
        }])

        if os.path.exists("alertas.csv"):
            alertas = pd.read_csv("alertas.csv")
            alertas = pd.concat([alertas, nueva_alerta], ignore_index=True)
        else:
            alertas = nueva_alerta

        alertas.to_csv("alertas.csv", index=False)

        st.success("Alerta guardada correctamente")
    else:
        st.warning("Ingresá un email")
