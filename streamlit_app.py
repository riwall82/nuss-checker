import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Titel der App
st.title("Nuss-Checker: Speisekarten-Check")

try:
    # Verbindung herstellen
    # Streamlit nutzt die Infos aus deinen Secrets (Projekt: AllergNo-Backend)
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Daten einlesen
    # Wir nutzen die URL aus den Secrets und greifen auf das Blatt 'Speisekarte' zu
    df = conn.read(
        spreadsheet=st.secrets["public_gsheets_url"],
        worksheet="Speisekarte" 
    )

    # Wenn alles klappt:
    st.success("✅ Verbindung zur 'Nussfrei_Database' erfolgreich!")
    
    # Zeige die ersten Zeilen deiner Speisekarte an
    st.subheader("Aktuelle Speisekarte:")
    st.dataframe(df)

except Exception as e:
    st.error("Oje, die Verbindung zur Datenbank hakt noch.")
    st.info(f"Fehlermeldung: {e}")
    st.write("---")
    st.write("**Fehlersuche für dich:**")
    st.write(f"- Heißt das Blatt im Google Sheet wirklich exakt: **Speisekarte**? (Kein Leerzeichen davor oder dahinter?)")
    st.write(f"- Ist der 'sheet-reader' Dienstaccount als Editor in der Datei 'Nussfrei_Database' eingetragen?")
