import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Nuss-Checker", layout="centered", initial_sidebar_state="collapsed")

# ─────────────────────────────────────────────
# KONFIGURATION
# ─────────────────────────────────────────────
SHEET_URL = "https://docs.google.com/spreadsheets/d/1KIVaK_b32tDo2uVqZKKxywdGVzGnYpHSzxD4OQRta00/edit?usp=sharing"

ALLERGEN_LABELS = {
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

# ─────────────────────────────────────────────
# SESSION STATE INITIALISIERUNG
# ─────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "disclaimer"
if "disclaimer_accepted" not in st.session_state:
    st.session_state.disclaimer_accepted = False
if "user_allergene" not in st.session_state:
    st.session_state.user_allergene = []
if "scan_result" not in st.session_state:
    st.session_state.scan_result = None
if "restaurant_logged_in" not in st.session_state:
    st.session_state.restaurant_logged_in = False
if "restaurant_name" not in st.session_state:
    st.session_state.restaurant_name = None

def navigate(page):
    st.session_state.page = page
    st.rerun()

# ─────────────────────────────────────────────
# HILFS-FUNKTIONEN
# ─────────────────────────────────────────────
def check_ampel(row, user_allergene):
    for allergen in user_allergene:
        if row.get(allergen) == 1:
            return "🔴", f"Enthält {ALLERGEN_LABELS[allergen]}"
    return "🟢", "Laut Angaben verträglich"

# ─────────────────────────────────────────────
# SEITE 1: DISCLAIMER
# ─────────────────────────────────────────────
def page_disclaimer():
    st.title("🥜 Nuss-Checker")
    st.subheader("Wichtiger Hinweis")

    st.info(
        """
        **Diese App dient ausschließlich als Hilfestellung.**

        Der Nuss-Checker kann keine Garantie für die Richtigkeit, Vollständigkeit
        oder Aktualität der angezeigten Allergeninformationen übernehmen.
        Die Angaben basieren auf Daten Dritter (Restaurants, Hersteller,
        Open Food DB) und können fehlerhaft oder veraltet sein.

        Bei schweren Allergien oder Unverträglichkeiten wende dich bitte immer
        direkt an das Restaurant oder den Hersteller und konsultiere im Zweifelsfall
        einen Arzt.

        **Die Nutzung der App erfolgt auf eigene Verantwortung.**
        """
    )

    accepted = st.checkbox("Ich habe den Hinweis gelesen und akzeptiere, dass diese App keine Haftung übernimmt.")

    st.button(
        "App starten →",
        disabled=not accepted,
        on_click=lambda: navigate("allergen_settings"),
        type="primary"
    )

# ─────────────────────────────────────────────
# SEITE 2: ALLERGEN-EINSTELLUNGEN
# ─────────────────────────────────────────────
def page_allergen_settings():
    is_onboarding = not st.session_state.disclaimer_accepted

    if not is_onboarding:
        st.button("← Zurück", on_click=lambda: navigate("main"))

    st.title("🧬 Meine Allergene")

    if is_onboarding:
        st.write("Welche Allergene soll die App für dich hervorheben?")
    else:
        st.write("Hier kannst du deine Allergen-Auswahl jederzeit anpassen.")

    selected = st.multiselect(
        "Allergene auswählen:",
        options=list(ALLERGEN_LABELS.keys()),
        default=st.session_state.user_allergene,
        format_func=lambda x: f"{x} – {ALLERGEN_LABELS[x]}"
    )

    btn_label = "Weiter →" if is_onboarding else "Speichern"
    st.button(
        btn_label,
        on_click=lambda: _save_allergene_and_go(selected, is_onboarding),
        type="primary"
    )

def _save_allergene_and_go(selected, is_onboarding):
    st.session_state.user_allergene = selected
    if is_onboarding:
        st.session_state.disclaimer_accepted = True
    navigate("main")

# ─────────────────────────────────────────────
# SEITE 3: HAUPTBILDSCHIRM
# ─────────────────────────────────────────────
def page_main():
    col_title, col_settings = st.columns([6, 1])
    with col_title:
        st.title("🥜 Nuss-Checker")
    with col_settings:
        st.button("⚙️", on_click=lambda: navigate("allergen_settings"), help="Einstellungen")

    if st.session_state.user_allergene:
        allergen_namen = ", ".join([ALLERGEN_LABELS[a] for a in st.session_state.user_allergene])
        st.caption(f"Aktive Allergene: {allergen_namen}")
    else:
        st.warning("Noch keine Allergene ausgewählt – gehe zu den Einstellungen.")

    st.markdown("---")
    st.markdown("### Was möchtest du tun?")

    st.button(
        "📷  Produkt oder Speisekarte scannen",
        on_click=lambda: navigate("scan"),
        use_container_width=True,
        type="primary"
    )

    st.markdown(" ")

    st.button(
        "🍽️  Digitale Speisekarte öffnen",
        on_click=lambda: navigate("restaurant_menu"),
        use_container_width=True
    )

    st.markdown("---")
    st.caption("Du bist ein Restaurant?")
    st.button(
        "🏪 Restaurant-Login",
        on_click=lambda: navigate("restaurant_admin")
    )

# ─────────────────────────────────────────────
# SEITE 4: TEXTERKENNUNG / KAMERA-SCAN
# ─────────────────────────────────────────────
def page_scan():
    st.button("← Zurück", on_click=lambda: navigate("main"))
    st.title("📷 Scannen")

    scan_mode = st.radio(
        "Was möchtest du scannen?",
        [
            "🛒 Produktetikett (Supermarkt)",
            "🌍 Fremdsprachiges Etikett",
            "📋 Restaurant-Speisekarte (QR-Code)"
        ]
    )

    st.markdown("---")
    camera_image = st.camera_input("Kamera aktivieren")

    if camera_image:
        st.image(camera_image, caption="Aufgenommenes Bild", use_column_width=True)
        st.markdown("---")

        if scan_mode == "🛒 Produktetikett (Supermarkt)":
            st.subheader("🔍 Erkannte Allergene")
            # PLATZHALTER – OCR + Allergen-Matching kommt später
            st.info("⚙️ Texterkennung wird hier verarbeitet...")

            for allergen in st.session_state.user_allergene:
                st.warning(f"⚠️ Enthält: **{ALLERGEN_LABELS[allergen]}**")

            if st.session_state.user_allergene:
                st.button(
                    "🔄 Sichere Alternativen anzeigen",
                    on_click=lambda: navigate("alternatives"),
                    type="primary"
                )

        elif scan_mode == "🌍 Fremdsprachiges Etikett":
            st.subheader("🌍 Übersetzung & Allergene")
            # PLATZHALTER – Übersetzungs-API kommt später
            st.info("⚙️ Sprache wird erkannt und übersetzt...")
            st.text_area("Erkannter Text (Platzhalter):", value="Esempio di testo in italiano...", disabled=True)

            for allergen in st.session_state.user_allergene:
                st.warning(f"⚠️ Enthält: **{ALLERGEN_LABELS[allergen]}**")

            if st.session_state.user_allergene:
                st.button(
                    "🔄 Sichere Alternativen anzeigen",
                    on_click=lambda: navigate("alternatives"),
                    type="primary"
                )

        elif scan_mode == "📋 Restaurant-Speisekarte (QR-Code)":
            st.subheader("📋 QR-Code erkannt")
            # PLATZHALTER – QR-Decode + Restaurant-ID laden kommt später
            st.info("⚙️ QR-Code wird ausgelesen und Restaurant geladen...")
            st.button(
                "🍽️ Gefilterte Speisekarte öffnen",
                on_click=lambda: navigate("restaurant_menu"),
                type="primary"
            )

# ─────────────────────────────────────────────
# SEITE 5: SICHERE ALTERNATIVEN
# ─────────────────────────────────────────────
def page_alternatives():
    import pandas as pd

    st.button("← Zurück", on_click=lambda: navigate("scan"))
    st.title("✅ Sichere Alternativen")

    if st.session_state.user_allergene:
        allergen_namen = ", ".join([ALLERGEN_LABELS[a] for a in st.session_state.user_allergene])
        st.caption(f"Gefiltert nach: {allergen_namen}")

    st.markdown("---")

    # PLATZHALTER – Open Food DB Abfrage kommt später
    st.info("⚙️ Alternativen werden aus der Open Food Facts Datenbank geladen...")

    placeholder_data = {
        "Produkt": ["Rote Linsen", "Kichererbsen", "Quinoa"],
        "Marke": ["Ja! Natürlich", "Spar Bio", "dm Bio"],
        "Allergene": ["Keine", "Keine", "Keine"],
        "Status": ["✅ Sicher", "✅ Sicher", "✅ Sicher"]
    }
    df = pd.DataFrame(placeholder_data)
    st.dataframe(df, use_container_width=True)

    st.caption("Daten stammen aus der Open Food Facts Datenbank. Keine Gewähr für Richtigkeit.")

# ─────────────────────────────────────────────
# SEITE 6: RESTAURANT-SPEISEKARTE (Nutzer-Sicht)
# ─────────────────────────────────────────────
def page_restaurant_menu():
    st.button("← Zurück", on_click=lambda: navigate("main"))
    st.title("🍽️ Speisekarte")

    if st.session_state.user_allergene:
        allergen_namen = ", ".join([ALLERGEN_LABELS[a] for a in st.session_state.user_allergene])
        st.caption(f"Gefiltert nach deinen Allergenen: {allergen_namen}")
    else:
        st.info("Keine Allergene ausgewählt – alle Gerichte werden angezeigt.")

    st.markdown("---")

    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Speisekarte", ttl=0)

        for _, row in df.iterrows():
            ampel_icon, ampel_text = check_ampel(row, st.session_state.user_allergene)
            with st.container():
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(f"## {row['Gericht_Nummer']}")
                with col2:
                    st.markdown(f"### {ampel_icon} {row['Name']}")
                    st.write(row["Beschreibung"])
                    st.write(f"💶 {row['Preis']} €")
                    st.caption(ampel_text)
                st.markdown("---")

    except Exception as e:
        st.warning("⚙️ Google Sheets Verbindung prüfen.")
        st.caption(f"Details: {e}")
        st.markdown("**Beispiel-Einträge (Platzhalter):**")
        st.markdown("🟢 **1 – Wiener Schnitzel** – Klassisch mit Erdäpfelsalat – 14,90 €")
        st.markdown("🔴 **2 – Spaghetti Bolognese** – Mit Parmesan – 11,50 €")

# ─────────────────────────────────────────────
# SEITE 7: RESTAURANT-ADMIN (Restaurant-Sicht)
# ─────────────────────────────────────────────
def page_restaurant_admin():
    st.button("← Zurück", on_click=lambda: navigate("main"))
    st.title("🏪 Restaurant-Verwaltung")

    if not st.session_state.restaurant_logged_in:
        st.subheader("Login")
        # PLATZHALTER – echte Authentifizierung kommt später
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")

        def do_login():
            if username and password:
                st.session_state.restaurant_logged_in = True
                st.session_state.restaurant_name = username
                st.rerun()

        st.button("Einloggen", on_click=do_login, type="primary")
        st.caption("⚙️ Echte Authentifizierung folgt in einer späteren Phase.")

    else:
        st.success(f"Eingeloggt als: **{st.session_state.restaurant_name}**")
        st.markdown("---")
        st.subheader("📋 Gericht hinzufügen")

        # PLATZHALTER – Speichern in Google Sheets kommt später
        gericht_name = st.text_input("Name des Gerichts")
        beschreibung = st.text_area("Beschreibung")
        preis = st.number_input("Preis (€)", min_value=0.0, step=0.5)

        st.write("Enthaltene Allergene:")
        cols = st.columns(4)
        for i, (key, label) in enumerate(ALLERGEN_LABELS.items()):
            with cols[i % 4]:
                st.checkbox(f"{key} – {label}", key=f"admin_{key}")

        st.button("💾 Gericht speichern", type="primary")
        st.caption("⚙️ Speichern in Google Sheets folgt in einer späteren Phase.")

        st.markdown("---")
        st.button("🚪 Ausloggen", on_click=_restaurant_logout)

def _restaurant_logout():
    st.session_state.restaurant_logged_in = False
    st.session_state.restaurant_name = None
    navigate("main")

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
page = st.session_state.page

if page == "disclaimer":
    page_disclaimer()
elif page == "allergen_settings":
    page_allergen_settings()
elif page == "main":
    page_main()
elif page == "scan":
    page_scan()
elif page == "alternatives":
    page_alternatives()
elif page == "restaurant_menu":
    page_restaurant_menu()
elif page == "restaurant_admin":
    page_restaurant_admin()
