import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Nuss-Checker", layout="centered")
st.title("🥜 Nuss-Checker: Speisekarten-Check")

st.title("🍽️ Nuss-Checker: Speisekarten-Check")

# ---------- HIER EINFÜGEN ----------
allergen_labels = {
    "A": "Glutenhaltiges Getreide",
    "B": "Krebstiere",
    "C": "Eier",
    "D": "Fische",
    "E": "Erdnüsse",
    "F": "Soja",
    "G": "Milch",
    "H": "Schalenfrüchte",
    "L": "Sellerie",
    "M": "Senf",
    "N": "Sesam",
    "O": "Sulfite",
    "P": "Lupinen",
    "R": "Weichtiere"
}

st.sidebar.header("🧬 Allergene vermeiden")

user_allergene = st.sidebar.multiselect(
    "Bitte auswählen:",
    options=list(allergen_labels.keys()),
    format_func=lambda x: f"{x} – {allergen_labels[x]}"
)
# ---------- ENDE BLOCK ----------

# Dies ist die EXAKTE URL aus deinem Screenshot
SHEET_URL = "https://docs.google.com/spreadsheets/d/1KIVaK_b32tDo2uVqZKKxywdGVzGnYpHSzxD4OQRta00/edit?usp=sharing"

def check_ampel(row, user_allergene):
    for allergen in user_allergene:
        if row[allergen] == 1:
            return "🔴", f"Enthält {allergen_labels[allergen]}"
    return "🟢", "Laut Angaben verträglich"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Wir lesen das Blatt "Speisekarte" ein
    df = conn.read(spreadsheet=SHEET_URL, worksheet="Speisekarte", ttl=0)

    st.success("✅ Wahnsinn, es läuft!")
    st.write("Hier sind die Daten aus deinem Google Sheet:")
    st.write("## 🍽️ Speisekarte")

for _, row in df.iterrows():

    ampel_icon, ampel_text = check_ampel(row, user_allergene)

    with st.container():
        st.markdown("---")

        col1, col2 = st.columns([1, 5])

        with col1:
            st.markdown(f"## {row['Gericht_Nummer']}")

        with col2:
            st.markdown(f"### {ampel_icon} {row['Name']}")
            st.write(row["Beschreibung"])
            st.write(f"💶 {row['Preis']} €")
            st.caption(ampel_text)

except Exception as e:
    st.error("Verbindung hakt noch.")
    st.code(f"Fehler-Details: {e}")
