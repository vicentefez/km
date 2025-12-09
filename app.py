import streamlit as st
import pandas as pd
import requests

# URL del Apps Script
APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxe2zD0BJd2OPs3bzBb01Dw5pcynIzSBYrGhub5Yxu94ctTHblD4F5ewmN9OBljLan3VQ/exec"

st.title("🚗 Registro de uso del auto (basado en odómetro)")

st.write("Registra el odómetro FINAL cada vez que dejas de usar el auto.")

usuario = st.selectbox(
    "¿Quién usó el auto?",
    ["Vicente", "Max", "Ambos"]
)

odometro = st.number_input("Odómetro actual del auto (km)", min_value=0.0, step=0.1)

if st.button("Registrar uso"):
    params = {"usuario": usuario, "odometro": odometro}
    r = requests.get(APP_SCRIPT_URL, params=params)

    if r.text == "OK":
        st.success("Registro guardado exitosamente.")
    else:
        st.error("Error: " + r.text)

st.divider()

st.subheader("📊 Historial completo")

# IMPORTANTE: poner tu sheet_id
SHEET_ID = "15BIHvfKWqpAtbf59YXn6hMjXoqIR-q5nkOQ5oowtcYE"

csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    df = pd.read_csv(csv_url)
    st.dataframe(df)
except:
    st.warning("No se pudo cargar la hoja todavía.")

