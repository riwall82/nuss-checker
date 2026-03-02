import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Nuss-Checker", layout="centered")
st.title("🥜 Nuss-Checker: Speisekarten-Check")

# Wir definieren die URL zur Sicherheit hier nochmal direkt als Variable
SHEET_URL = "https://docs.google.com/spreadsheets/d/1KIVaK_b32tDo2uVqZKKxywdGVzGnYPshzXd4OQRta00/edit#gid=492057983"

try:
    # Verbindung herstellen
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Daten einlesen mit Fehlertoleranz für die URL
    df = conn.read(
        spreadsheet=SHEET_URL,
        worksheet="Speisekarte"
    )

    st.success("✅ Verbindung zur Datenbank erfolgreich!")
    st.write("Hier sind deine aktuellen Gerichte:")
    st.dataframe(df)

except Exception as e:
    st.error("Oje, die Verbindung hakt noch.")
    st.info(f"Details: {e}")
