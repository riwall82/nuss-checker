import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Nuss-Checker", layout="centered")
st.title("🥜 Nuss-Checker: Speisekarten-Check")

# Dies ist die EXAKTE URL aus deinem Screenshot
SHEET_URL = "https://docs.google.com/spreadsheets/d/1KlVaK_b32tDo2uVqZKKxywdGVzGnYPHSzxD4OQRta00/edit"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Wir lesen das Blatt "Speisekarte" ein
    df = conn.read(spreadsheet=SHEET_URL, worksheet="Speisekarte")

    st.success("✅ Wahnsinn, es läuft!")
    st.write("Hier sind die Daten aus deinem Google Sheet:")
    st.dataframe(df)

except Exception as e:
    st.error("Verbindung hakt noch.")
    st.code(f"Fehler-Details: {e}")
