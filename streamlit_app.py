import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Verbindungs-Test: Nuss-Checker")

try:
    # Hier sagen wir der App explizit: Nutze die URL aus den Secrets!
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Wir lesen das Sheet unter Verwendung der URL aus den Secrets
    df = conn.read(
        spreadsheet=st.secrets["public_gsheets_url"],
        worksheet="Speisekarte"
    )

    st.success("🎉 Verbindung steht! Daten wurden geladen.")
    st.write("Hier ist deine Speisekarte:")
    st.dataframe(df)

except Exception as e:
    st.error(f"Fehler: {e}")
    st.info("Hinweis: Prüfe, ob der Name des Tabellenblatts exakt 'Speisekarte' lautet.")
