import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Nuss-Checker", layout="centered")
st.title("🥜 Nuss-Checker: Speisekarten-Check")

# Diese ID habe ich direkt aus deinem Browser-Screenshot (18.42.23) übernommen:
SHEET_ID = "1KlVaK_b32tDo2uVqZKKxywdGVzGnYPHSzxD4OQRta00"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Wir versuchen das Blatt einzulesen
    df = conn.read(spreadsheet=SHEET_URL, worksheet="Speisekarte")

    st.success("✅ Wahnsinn, es läuft!")
    st.dataframe(df)

except Exception as e:
    st.error("Verbindung hakt noch.")
    st.code(f"Fehler-Details: {e}") # Zeigt den Fehler in einer Box an
