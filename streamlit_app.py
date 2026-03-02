import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Titel der App
st.title("Verbindungs-Test: Nuss-Checker & Google Sheets")

# Verbindung zum Google Sheet herstellen
try:
    # Erstellt die Verbindung basierend auf deinen Secrets
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Daten aus dem Tabellenblatt "Speisekarte" lesen
    # WICHTIG: Prüfe, ob dein Tabellenblatt unten im Google Sheet exakt so heißt!
    df = conn.read(worksheet="Speisekarte")

    # Erfolgskontrolle
    st.success("🎉 Wahnsinn! Die Verbindung zum Google Sheet steht!")
    
    # Zeige die Daten als Tabelle an
    st.write("Hier sind die aktuellen Daten aus deiner Google-Tabelle:")
    st.dataframe(df)

except Exception as e:
    # Falls etwas schiefgeht, zeigt die App hier den Fehler an
    st.error("Oje, da hakt noch was bei der Verbindung.")
    st.info(f"Fehlermeldung: {e}")
    st.write("Checkliste:")
    st.write("1. Sind die Secrets in Streamlit korrekt hinterlegt?")
    st.write("2. Hast du die Service-Account-Email im Google Sheet als 'Editor' freigegeben?")
