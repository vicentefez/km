import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuración inicial ---
st.set_page_config(page_title="Registro de KM compartidos", page_icon="🚗")

st.title("🚗 Registro de KM compartidos")

# --- Inicializar CSV si no existe ---
DATA_FILE = "data.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Fecha", "Nombre", "KM"])
    df.to_csv(DATA_FILE, index=False)

# --- Cargar datos ---
df = pd.read_csv(DATA_FILE)

# --- Formulario de registro ---
st.subheader("Registrar nuevo uso")

with st.form("registro_km"):
    nombre = st.selectbox("¿Quién usó el auto?", ["Vicente", "Maz"])
    km = st.number_input("¿Cuántos km hiciste?", min_value=0.0, step=0.1)
    submit = st.form_submit_button("Guardar")

    if submit:
        if km > 0:
            nuevo = pd.DataFrame({
                "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M")],
                "Nombre": [nombre],
                "KM": [km]
            })
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Registro guardado correctamente.")
        else:
            st.warning("Ingresa una cantidad válida de km.")

# --- Mostrar registros ---
st.subheader("Historial de usos")
st.dataframe(df)

# --- Cálculo de totales ---
if not df.empty:
    totales = df.groupby("Nombre")["KM"].sum().reset_index()
    total_km = totales["KM"].sum()
    st.subheader("Totales acumulados")
    st.write(f"**Total de kilómetros:** {total_km:.1f} km")
    st.table(totales)

    # --- Cálculo del reparto ---
    st.subheader("💰 Reparto del gasto de bencina")
    gasto = st.number_input("Monto total de bencina ($)", min_value=0, step=1000)

    if gasto > 0 and total_km > 0:
        totales["Proporción"] = totales["KM"] / total_km
        totales["Pago"] = totales["Proporción"] * gasto
        st.table(totales[["Nombre", "KM", "Pago"]])
else:
    st.info("Aún no hay registros. Agrega el primero arriba 👆")
