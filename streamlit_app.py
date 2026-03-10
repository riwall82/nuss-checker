import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Nuss-Checker", layout="centered", initial_sidebar_state="collapsed")

# ─────────────────────────────────────────────
# SUPABASE VERBINDUNG
# Secrets in Streamlit: .streamlit/secrets.toml
# ─────────────────────────────────────────────
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# ─────────────────────────────────────────────
# KONFIGURATION
# ─────────────────────────────────────────────
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

FREEMIUM_SCAN_LIMIT = 3

# ─────────────────────────────────────────────
# SESSION STATE INITIALISIERUNG
# ─────────────────────────────────────────────
defaults = {
    "page": "disclaimer",
    "user": None,           # Supabase Auth User-Objekt
    "profile": None,        # user_profiles Zeile
    "user_allergene": [],
    "disclaimer_accepted": False,
    "restaurant_logged_in": False,
    "restaurant_data": None,
    "scan_result": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

def navigate(page):
    st.session_state.page = page

# ─────────────────────────────────────────────
# AUTHENTIFIZIERUNG & PROFIL
# ─────────────────────────────────────────────
def load_profile(user_id: str):
    """Lädt das user_profile aus Supabase und befüllt session_state."""
    res = supabase.table("user_profiles").select("*").eq("id", user_id).single().execute()
    if res.data:
        profile = res.data
        st.session_state.profile = profile
        st.session_state.disclaimer_accepted = profile.get("disclaimer_accepted", False)
        # Allergene aus Boolean-Spalten zurück in Liste
        st.session_state.user_allergene = [
            key for key in ALLERGEN_LABELS if profile.get(key, False)
        ]

def save_profile_allergene(selected: list):
    """Speichert Allergen-Auswahl als Boolean-Spalten in user_profiles."""
    if not st.session_state.user:
        return
    allergen_update = {key: (key in selected) for key in ALLERGEN_LABELS}
    supabase.table("user_profiles").update(allergen_update).eq(
        "id", st.session_state.user.id
    ).execute()
    st.session_state.user_allergene = selected

def save_disclaimer_accepted():
    """Setzt disclaimer_accepted = TRUE in user_profiles."""
    if not st.session_state.user:
        return
    from datetime import datetime, timezone
    supabase.table("user_profiles").update({
        "disclaimer_accepted": True,
        "disclaimer_accepted_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", st.session_state.user.id).execute()
    st.session_state.disclaimer_accepted = True

def get_scan_count() -> int:
    """Gibt die Anzahl der Scans des aktuellen Users zurück."""
    if not st.session_state.user:
        return 0
    res = supabase.table("scan_log").select("id", count="exact").eq(
        "user_id", st.session_state.user.id
    ).execute()
    return res.count or 0

def log_scan(scan_type: str):
    """Trägt einen neuen Scan in scan_log ein."""
    if not st.session_state.user:
        return
    supabase.table("scan_log").insert({
        "user_id": st.session_state.user.id,
        "scan_type": scan_type
    }).execute()

def is_premium() -> bool:
    profile = st.session_state.profile
    return profile and profile.get("plan") == "premium"

# ─────────────────────────────────────────────
# HILFS-FUNKTIONEN
# ─────────────────────────────────────────────
def check_ampel(gericht: dict, user_allergene: list):
    for allergen in user_allergene:
        if gericht.get(allergen):
            return "🔴", f"Enthält {ALLERGEN_LABELS[allergen]}"
    return "🟢", "Laut Angaben verträglich"

# ─────────────────────────────────────────────
# SEITE: LOGIN / REGISTRIERUNG
# ─────────────────────────────────────────────
def page_auth():
    st.title("🥜 Nuss-Checker")
    tab_login, tab_register = st.tabs(["Einloggen", "Registrieren"])

    with tab_login:
        email = st.text_input("E-Mail", key="login_email")
        password = st.text_input("Passwort", type="password", key="login_password")

        def do_login():
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                load_profile(res.user.id)
                if not st.session_state.disclaimer_accepted:
                    navigate("disclaimer")
                else:
                    navigate("main")
            except Exception as e:
                st.error(f"Login fehlgeschlagen: {e}")

        st.button("Einloggen", on_click=do_login, type="primary")

    with tab_register:
        email_r = st.text_input("E-Mail", key="reg_email")
        password_r = st.text_input("Passwort (min. 6 Zeichen)", type="password", key="reg_password")

        def do_register():
            try:
                res = supabase.auth.sign_up({"email": email_r, "password": password_r})
                st.session_state.user = res.user
                load_profile(res.user.id)
                navigate("disclaimer")
            except Exception as e:
                st.error(f"Registrierung fehlgeschlagen: {e}")

        st.button("Registrieren", on_click=do_register, type="primary")
        st.caption("Nach der Registrierung bitte E-Mail bestätigen.")

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

    def accept_and_continue():
        save_disclaimer_accepted()
        navigate("allergen_settings")

    st.button(
        "App starten →",
        disabled=not accepted,
        on_click=accept_and_continue,
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

    def save_and_go():
        save_profile_allergene(selected)
        navigate("main")

    st.button(btn_label, on_click=save_and_go, type="primary")

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

    # Freemium-Anzeige
    if not is_premium():
        scan_count = get_scan_count()
        remaining = max(0, FREEMIUM_SCAN_LIMIT - scan_count)
        st.caption(f"☕ Free-Plan: noch {remaining} von {FREEMIUM_SCAN_LIMIT} Scans übrig.")

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
    st.button("🏪 Restaurant-Login", on_click=lambda: navigate("restaurant_admin"))

    st.markdown("---")
    def do_logout():
        supabase.auth.sign_out()
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.button("🚪 Abmelden", on_click=do_logout)

# ─────────────────────────────────────────────
# SEITE 4: TEXTERKENNUNG / KAMERA-SCAN
# ─────────────────────────────────────────────
def page_scan():
    st.button("← Zurück", on_click=lambda: navigate("main"))
    st.title("📷 Scannen")

    # Freemium-Check
    if not is_premium():
        scan_count = get_scan_count()
        if scan_count >= FREEMIUM_SCAN_LIMIT:
            st.error(f"Du hast dein Scan-Limit von {FREEMIUM_SCAN_LIMIT} Scans erreicht.")
            st.info("☕ Unterstütze den Nuss-Checker mit einem kleinen Beitrag für mehr Scans.")
            st.button("💛 Kaffee spenden", on_click=lambda: None)  # PLATZHALTER – Zahlungslink folgt
            return

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
            log_scan("produkt")
            st.subheader("🔍 Erkannte Allergene")
            st.info("⚙️ Texterkennung wird hier verarbeitet...")  # PLATZHALTER – OCR folgt
            for allergen in st.session_state.user_allergene:
                st.warning(f"⚠️ Enthält: **{ALLERGEN_LABELS[allergen]}**")
            if st.session_state.user_allergene:
                st.button("🔄 Sichere Alternativen anzeigen",
                          on_click=lambda: navigate("alternatives"), type="primary")

        elif scan_mode == "🌍 Fremdsprachiges Etikett":
            log_scan("fremdsprache")
            st.subheader("🌍 Übersetzung & Allergene")
            st.info("⚙️ Sprache wird erkannt und übersetzt...")  # PLATZHALTER – Übersetzungs-API folgt
            st.text_area("Erkannter Text (Platzhalter):", value="Esempio di testo in italiano...", disabled=True)
            for allergen in st.session_state.user_allergene:
                st.warning(f"⚠️ Enthält: **{ALLERGEN_LABELS[allergen]}**")
            if st.session_state.user_allergene:
                st.button("🔄 Sichere Alternativen anzeigen",
                          on_click=lambda: navigate("alternatives"), type="primary")

        elif scan_mode == "📋 Restaurant-Speisekarte (QR-Code)":
            log_scan("qr_code")
            st.subheader("📋 QR-Code erkannt")
            st.info("⚙️ QR-Code wird ausgelesen und Restaurant geladen...")  # PLATZHALTER – QR-Decode folgt
            st.button("🍽️ Gefilterte Speisekarte öffnen",
                      on_click=lambda: navigate("restaurant_menu"), type="primary")

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
    st.info("⚙️ Alternativen werden aus der Open Food Facts Datenbank geladen...")  # PLATZHALTER

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
        res = supabase.table("gerichte").select("*, restaurants(name)").eq("aktiv", True).execute()
        gerichte = res.data

        if not gerichte:
            st.info("Noch keine Gerichte in der Datenbank.")
            return

        for gericht in gerichte:
            ampel_icon, ampel_text = check_ampel(gericht, st.session_state.user_allergene)
            with st.container():
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(f"## {gericht.get('gericht_nummer', '–')}")
                with col2:
                    st.markdown(f"### {ampel_icon} {gericht['name']}")
                    st.write(gericht.get("beschreibung", ""))
                    st.write(f"💶 {gericht.get('preis', '–')} €")
                    st.caption(ampel_text)
                st.markdown("---")

    except Exception as e:
        st.error(f"Fehler beim Laden der Speisekarte: {e}")

# ─────────────────────────────────────────────
# SEITE 7: RESTAURANT-ADMIN (Restaurant-Sicht)
# ─────────────────────────────────────────────
def page_restaurant_admin():
    st.button("← Zurück", on_click=lambda: navigate("main"))
    st.title("🏪 Restaurant-Verwaltung")

    if not st.session_state.restaurant_logged_in:
        st.subheader("Restaurant-Login")
        email = st.text_input("E-Mail", key="rest_email")
        password = st.text_input("Passwort", type="password", key="rest_password")

        def do_restaurant_login():
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                user = res.user
                # Prüfen ob ein Restaurant zu diesem Account gehört
                rest_res = supabase.table("restaurants").select("*").eq("owner_id", user.id).single().execute()
                if rest_res.data:
                    st.session_state.restaurant_logged_in = True
                    st.session_state.restaurant_data = rest_res.data
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Kein Restaurant-Account gefunden. Bitte wende dich an den Support.")
            except Exception as e:
                st.error(f"Login fehlgeschlagen: {e}")

        st.button("Einloggen", on_click=do_restaurant_login, type="primary")
        st.caption("⚙️ Restaurant-Registrierung folgt in einer späteren Phase.")

    else:
        restaurant = st.session_state.restaurant_data
        st.success(f"Eingeloggt als: **{restaurant['name']}**")
        st.markdown("---")
        st.subheader("📋 Gericht hinzufügen")

        gericht_nummer = st.text_input("Gerichtnummer (z.B. 14 oder B2)")
        gericht_name = st.text_input("Name des Gerichts")
        beschreibung = st.text_area("Beschreibung")
        preis = st.number_input("Preis (€)", min_value=0.0, step=0.5)

        st.write("Enthaltene Allergene:")
        cols = st.columns(4)
        allergen_selection = {}
        for i, (key, label) in enumerate(ALLERGEN_LABELS.items()):
            with cols[i % 4]:
                allergen_selection[key] = st.checkbox(f"{key} – {label}", key=f"admin_{key}")

        def save_gericht():
            try:
                new_gericht = {
                    "restaurant_id": restaurant["id"],
                    "gericht_nummer": gericht_nummer,
                    "name": gericht_name,
                    "beschreibung": beschreibung,
                    "preis": preis,
                    **allergen_selection
                }
                supabase.table("gerichte").insert(new_gericht).execute()
                st.success("✅ Gericht gespeichert!")
            except Exception as e:
                st.error(f"Fehler beim Speichern: {e}")

        st.button("💾 Gericht speichern", on_click=save_gericht, type="primary")

        st.markdown("---")
        def restaurant_logout():
            st.session_state.restaurant_logged_in = False
            st.session_state.restaurant_data = None
            navigate("main")

        st.button("🚪 Ausloggen", on_click=restaurant_logout)

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────

# Nicht eingeloggte User → Auth-Seite
# Ausnahme: disclaimer & allergen_settings kommen nach dem Login
if not st.session_state.user and st.session_state.page not in ("disclaimer", "allergen_settings"):
    page_auth()
else:
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
    else:
        page_auth()
