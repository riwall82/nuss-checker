import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Nuss-Checker", layout="centered")
st.title("🥜 Nuss-Checker: Speisekarten-Check")

# Wir nehmen die ganz saubere URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1KIVaK_b32tDo2uVqZKKxywdGVzGnYPshzXd4OQRta00/edit"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Wir lesen einfach das erste verfügbare Blatt ein
    df = conn.read(spreadsheet=SHEET_URL)

    st.success("✅ Verbindung steht! Hier sind deine Daten:")
    st.dataframe(df)

except Exception as e:
    st.error("Verbindung hakt noch.")
    st.info(f"Details: {e}")
