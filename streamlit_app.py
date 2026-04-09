import streamlit as st
from supabase import create_client, Client

st.set_page_config(
    page_title="Nuss-Checker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# SVG ICONS (base64)
# ─────────────────────────────────────────────
ICON_PROFIL_AKTIV  = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgeyBmaWxsOiAjYjFiMmIyOyB9CiAgICAgIC5jbHMtMiB7IGZvbnQtZmFtaWx5OiAnQWxiZXJ0IFNhbnMnOyBmb250LXNpemU6IDEycHg7IGZpbGw6ICNiNzg3MTU7IH0KICAgICAgLmNscy0zIHsgZmlsbDogI2I3ODcxNTsgfQogICAgICAuY2xzLTQgeyBmaWxsOiBub25lOyBzdHJva2U6ICNiNzg3MTU7IHN0cm9rZS1saW5lY2FwOiByb3VuZDsgc3Ryb2tlLWxpbmVqb2luOiByb3VuZDsgc3Ryb2tlLXdpZHRoOiAxLjdweDsgfQogICAgICAuY2xzLTUgeyBmaWxsOiBub25lOyBzdHJva2U6ICNiMWIyYjI7IHN0cm9rZS1saW5lY2FwOiByb3VuZDsgc3Ryb2tlLWxpbmVqb2luOiByb3VuZDsgc3Ryb2tlLXdpZHRoOiAxLjdweDsgfQogICAgPC9zdHlsZT4KICA8L2RlZnM+CiAgPHRleHQgY2xhc3M9ImNscy0yIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0OS4xMyA2MCkiPlByb2ZpbDwvdGV4dD4KICA8cGF0aCBjbGFzcz0iY2xzLTMiIGQ9Ik02NC43NSwzOS4zMmMzLjg3LDAsNy4zNC0xLjY2LDkuNzctNC4yOS0xLjM5LTQuMDctNS4yMy03LTkuNzctN3MtOC4zOSwyLjkzLTkuNzcsN2MyLjQzLDIuNjMsNS45LDQuMjksOS43Nyw0LjI5WiIvPgogIDxjaXJjbGUgY2xhc3M9ImNscy0zIiBjeD0iNjQuNzUiIGN5PSIyMS41NCIgcj0iNC44NCIvPgogIDxjaXJjbGUgY2xhc3M9ImNscy00IiBjeD0iNjQuNzUiIGN5PSIyNS45OSIgcj0iMTMuMSIvPgogIDxwYXRoIGNsYXNzPSJjbHMtNSIgZD0iTTY0Ljc1LDguNGM3LjI5LDAsMTMuNTQsNC40MywxNi4yMSwxMC43NCIvPgogIDxjaXJjbGUgY2xhc3M9ImNscy0xIiBjeD0iODEuNDUiIGN5PSIyMi42MiIgcj0iMS4wOSIvPgo8L3N2Zz4="
ICON_PROFIL_PASSIV = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgeyBmaWxsOiAjM2M1NzdhOyB9CiAgICAgIC5jbHMtMiB7IGZvbnQtZmFtaWx5OiAnQWxiZXJ0IFNhbnMnOyBmb250LXNpemU6IDEycHg7IGZpbGw6ICM2ZjcwNmY7IH0KICAgICAgLmNscy0zIHsgZmlsbDogI2IxYjJiMjsgfQogICAgICAuY2xzLTQgeyBmaWxsOiBub25lOyBzdHJva2U6ICMzYzU3N2E7IHN0cm9rZS1saW5lY2FwOiByb3VuZDsgc3Ryb2tlLWxpbmVqb2luOiByb3VuZDsgc3Ryb2tlLXdpZHRoOiAxLjdweDsgfQogICAgICAuY2xzLTUgeyBmaWxsOiBub25lOyBzdHJva2U6ICNiMWIyYjI7IHN0cm9rZS1saW5lY2FwOiByb3VuZDsgc3Ryb2tlLWxpbmVqb2luOiByb3VuZDsgc3Ryb2tlLXdpZHRoOiAxLjdweDsgfQogICAgPC9zdHlsZT4KICA8L2RlZnM+CiAgPHRleHQgY2xhc3M9ImNscy0yIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0OS4xMyA2MCkiPlByb2ZpbDwvdGV4dD4KICA8cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik02NC43NSwzOS4zMmMzLjg3LDAsNy4zNC0xLjY2LDkuNzctNC4yOS0xLjM5LTQuMDctNS4yMy03LTkuNzctN3MtOC4zOSwyLjkzLTkuNzcsN2MyLjQzLDIuNjMsNS45LDQuMjksOS43Nyw0LjI5WiIvPgogIDxjaXJjbGUgY2xhc3M9ImNscy0xIiBjeD0iNjQuNzUiIGN5PSIyMS41NCIgcj0iNC44NCIvPgogIDxjaXJjbGUgY2xhc3M9ImNscy00IiBjeD0iNjQuNzUiIGN5PSIyNS45OSIgcj0iMTMuMSIvPgogIDxwYXRoIGNsYXNzPSJjbHMtNSIgZD0iTTY0Ljc1LDguNGM3LjI5LDAsMTMuNTQsNC40MywxNi4yMSwxMC43NCIvPgogIDxjaXJjbGUgY2xhc3M9ImNscy0zIiBjeD0iODEuNDUiIGN5PSIyMi42MiIgcj0iMS4wOSIvPgo8L3N2Zz4="
ICON_SCAN_AKTIV    = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPjxkZWZzPjxzdHlsZT4uYXtmaWxsOm5vbmU7c3Ryb2tlOiNiNzg3MTU7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7c3Ryb2tlLW1pdGVybGltaXQ6MTA7c3Ryb2tlLXdpZHRoOjEuN3B4fS5ie2ZvbnQtZmFtaWx5OidBbGJlcnQgU2Fucyc7Zm9udC1zaXplOjEycHg7ZmlsbDojYjc4NzE1fTwvc3R5bGU+PC9kZWZzPjx0ZXh0IGNsYXNzPSJiIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg1NC44NyA2MCkiPlNjYW48L3RleHQ+PHBhdGggY2xhc3M9ImEiIGQ9Ik00Ni4zNywyMC4wOXYtMy4wN2MwLTIuMTcsMS43Ni0zLjkyLDMuOTItMy45Mmg5LjA3Ii8+PHBhdGggY2xhc3M9ImEiIGQ9Ik00Ni4zNywzMi4zMnYzLjA3YzAsMi4xNywxLjc2LDMuOTIsMy45MiwzLjkyaDkuMDciLz48cGF0aCBjbGFzcz0iYSIgZD0iTTkxLjAzLDIwLjA5di0zLjA3YzAtMi4xNy0xLjc2LTMuOTItMy45Mi0zLjkyaC05LjA3Ii8+PHBhdGggY2xhc3M9ImEiIGQ9Ik05MS4wMywzMi4zMnYzLjA3YzAsMi4xNy0xLjc2LDMuOTItMy45MiwzLjkyaC05LjA3Ii8+PC9zdmc+"
ICON_SCAN_PASSIV   = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPjxkZWZzPjxzdHlsZT4uYXtmb250LWZhbWlseTonQWxiZXJ0IFNhbnMnO2ZvbnQtc2l6ZToxMnB4O2ZpbGw6IzZmNzA2Zn0uYntmaWxsOm5vbmU7c3Ryb2tlOiMzYzU3N2E7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7c3Ryb2tlLW1pdGVybGltaXQ6MTA7c3Ryb2tlLXdpZHRoOjEuN3B4fTwvc3R5bGU+PC9kZWZzPjx0ZXh0IGNsYXNzPSJhIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg1NC44NyA2MCkiPlNjYW48L3RleHQ+PHBhdGggY2xhc3M9ImIiIGQ9Ik00Ni4zNywyMC4wOXYtMy4wN2MwLTIuMTcsMS43Ni0zLjkyLDMuOTItMy45Mmg5LjA3Ii8+PHBhdGggY2xhc3M9ImIiIGQ9Ik00Ni4zNywzMi4zMnYzLjA3YzAsMi4xNywxLjc2LDMuOTIsMy45MiwzLjkyaDkuMDciLz48cGF0aCBjbGFzcz0iYiIgZD0iTTkxLjAzLDIwLjA5di0zLjA3YzAtMi4xNy0xLjc2LTMuOTItMy45Mi0zLjkyaC05LjA3Ii8+PHBhdGggY2xhc3M9ImIiIGQ9Ik05MS4wMywzMi4zMnYzLjA3YzAsMi4xNy0xLjc2LDMuOTItMy45MiwzLjkyaC05LjA3Ii8+PC9zdmc+"
ICON_REST_AKTIV    = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPjxkZWZzPjxzdHlsZT4uYXtmaWxsOiNlNGU0ZTR9LmJ7ZmlsbDpub25lO3N0cm9rZTojYjc4NzE1O3N0cm9rZS13aWR0aDoxLjdweDtzdHJva2UtbGluZWNhcDpyb3VuZDtzdHJva2UtbGluZWpvaW46cm91bmR9LmN7Zm9udC1mYW1pbHk6J0FsYmVydCBTYW5zJztmb250LXNpemU6MTJweDtmaWxsOiNiNzg3MTV9LmR7ZmlsbDpub25lO3N0cm9rZTojYjFiMmIyO3N0cm9rZS13aWR0aDoxLjdweDtzdHJva2UtbGluZWNhcDpyb3VuZDtzdHJva2UtbGluZWpvaW46cm91bmR9LmV7ZmlsbDojYjFiMmIyfTwvc3R5bGU+PC9kZWZzPjxwYXRoIGNsYXNzPSJhIiBkPSJNNzUuOTgsMzIuNzhWMTQuOThjMC0xLjE0LS45My0yLjA3LTIuMDctMi4wN2gtMTUuNjNjLTEuMTQsMC0yLjA3LjkzLTIuMDcsMi4wN3YzLjU5YzkuMDkuMjUsMTYuNzksNi4wOSwxOS43NywxNC4yMVoiLz48cmVjdCBjbGFzcz0iYiIgeD0iNTYuMiIgeT0iMTIuOTEiIHdpZHRoPSIxOS43NyIgaGVpZ2h0PSIyNi4xOSIgcng9IjMuNTQiIHJ5PSIzLjU0Ii8+PHRleHQgY2xhc3M9ImMiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDMzLjAxIDYwKSI+UmVzdGF1cmFudHM8L3RleHQ+PHBhdGggY2xhc3M9ImQiIGQ9Ik02OS44Myw4LjQ2aDUuMjRjMi45MSwwLDUuMjcsMi4zNiw1LjI3LDUuMjd2NS41MiIvPjxjaXJjbGUgY2xhc3M9ImUiIGN4PSI4MC4zNCIgY3k9IjIyLjYyIiByPSIxLjA5Ii8+PC9zdmc+"
ICON_REST_PASSIV   = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPjxkZWZzPjxzdHlsZT4uYXtmaWxsOiNlNGU0ZTR9LmJ7ZmlsbDpub25lO3N0cm9rZTojM2M1NzdhO3N0cm9rZS13aWR0aDoxLjdweDtzdHJva2UtbGluZWNhcDpyb3VuZDtzdHJva2UtbGluZWpvaW46cm91bmR9LmN7Zm9udC1mYW1pbHk6J0FsYmVydCBTYW5zJztmb250LXNpemU6MTJweDtmaWxsOiM2ZjcwNmZ9LmR7ZmlsbDpub25lO3N0cm9rZTojYjFiMmIyO3N0cm9rZS13aWR0aDoxLjdweDtzdHJva2UtbGluZWNhcDpyb3VuZDtzdHJva2UtbGluZWpvaW46cm91bmR9LmV7ZmlsbDojYjFiMmIyfTwvc3R5bGU+PC9kZWZzPjxwYXRoIGNsYXNzPSJhIiBkPSJNNzUuOTgsMzIuNzhWMTQuOThjMC0xLjE0LS45My0yLjA3LTIuMDctMi4wN2gtMTUuNjNjLTEuMTQsMC0yLjA3LjkzLTIuMDcsMi4wN3YzLjU5YzkuMDkuMjUsMTYuNzksNi4wOSwxOS43NywxNC4yMVoiLz48cmVjdCBjbGFzcz0iYiIgeD0iNTYuMiIgeT0iMTIuOTEiIHdpZHRoPSIxOS43NyIgaGVpZ2h0PSIyNi4xOSIgcng9IjMuNTQiIHJ5PSIzLjU0Ii8+PHRleHQgY2xhc3M9ImMiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDMzLjAxIDYwKSI+UmVzdGF1cmFudHM8L3RleHQ+PHBhdGggY2xhc3M9ImQiIGQ9Ik02OS44Myw4LjQ2aDUuMjRjMi45MSwwLDUuMjcsMi4zNiw1LjI3LDUuMjd2NS41MiIvPjxjaXJjbGUgY2xhc3M9ImUiIGN4PSI4MC4zNCIgY3k9IjIyLjYyIiByPSIxLjA5Ii8+PC9zdmc+"
ICON_HAKEN         = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMC42MSAxNi4zOSI+PHBhdGggZD0iTTcuMTYsMTUuODloMGMtLjY1LDAtMS4yNy0uMjYtMS43My0uNzJMMS4yMiwxMC45NWMtLjk2LS45NS0uOTYtMi41LDAtMy40Ni45Ni0uOTUsMi41LS45NSwzLjQ2LDBsMi40OSwyLjQ5TDE1LjkzLDEuMjJjLjk2LS45NiwyLjUtLjk2LDMuNDYsMCwuOTYuOTUuOTYsMi41LDAsMy40NmwtMTAuNSwxMC41Yy0uNDYuNDYtMS4wOC43Mi0xLjczLjcyWiIgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2U6IzliOTI4YjtzdHJva2UtbWl0ZXJsaW1pdDoxMCIvPjwvc3ZnPg=="
ICON_FAV_PASSIV    = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNy44NSAxNi40NiI+PHBhdGggZD0iTTguOTIsMTUuOTZDNS40NCwxMy4xNy41LDguMy41LDQuNDQuNSwyLjIxLDIuNC41LDQuNzUuNWMyLjAzLDAsMy40NiwxLjA1LDQuMTcsMy42My43Mi0yLjU4LDIuMTItMy42Myw0LjE3LTMuNjMsMi4zNSwwLDQuMjUsMS43MSw0LjI1LDMuOTQsMCwzLjg2LTQuOTQsOC43My04LjQyLDExLjUyWiIgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2U6IzliOTI4YjtzdHJva2UtbGluZWNhcDpyb3VuZDtzdHJva2UtbGluZWpvaW46cm91bmQiLz48L3N2Zz4="

def svg_img(b64, width="100%"):
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{width}" style="display:block"/>'

# ─────────────────────────────────────────────
# CSS: alle Fixes
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600;700&display=swap');

/* ── Hide Streamlit chrome ── */
#MainMenu, header[data-testid="stHeader"], [data-testid="stToolbar"],
footer, .viewerBadge_container__1QSob, [data-testid="stDecoration"],
.stDeployButton, [data-testid="manage-app-button"] {{
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}}

/* ── Basis ── */
html, body, [class*="css"] {{
    font-family: 'Albert Sans', sans-serif !important;
    background: #fff;
    -webkit-text-size-adjust: 100%;
}}
.stApp {{ background: #fff; }}
.block-container {{
    padding: 16px 16px 100px 16px !important;
    max-width: 430px !important;
    margin: 0 auto !important;
}}

/* ── Typografie ── */
h1 {{
    font-family: 'Albert Sans', sans-serif !important;
    font-size: 26px !important; font-weight: 700 !important;
    color: #b78715 !important; margin-bottom: 4px !important;
}}
h2 {{
    font-family: 'Albert Sans', sans-serif !important;
    font-size: 16px !important; font-weight: 600 !important;
    color: #9b928b !important; margin: 14px 0 4px !important;
}}
p, .stMarkdown p {{
    font-family: 'Albert Sans', sans-serif !important;
    color: #000 !important; font-size: 15px !important;
}}
label {{ font-family: 'Albert Sans', sans-serif !important; color: #000 !important; }}

/* ── Buttons allgemein ── */
.stButton > button {{
    font-family: 'Albert Sans', sans-serif !important;
    border-radius: 12px !important; cursor: pointer !important;
    transition: opacity 0.2s !important;
}}
.stButton > button[kind="primary"] {{
    background: #b78715 !important; color: #fff !important;
    border: none !important; font-weight: 600 !important;
    font-size: 16px !important; padding: 14px 24px !important; width: 100% !important;
}}
.stButton > button[kind="primary"]:hover {{ opacity: 0.88 !important; }}
.stButton > button[kind="primary"]:disabled {{
    background: #e0d5c0 !important; color: #a0906a !important;
}}
.stButton > button[kind="secondary"] {{
    background: transparent !important; color: #3c577a !important;
    border: 1.5px solid #3c577a !important; font-weight: 500 !important;
    font-size: 15px !important; padding: 10px 20px !important; width: 100% !important;
}}
.stButton > button:not([kind]) {{
    background: transparent !important; border: none !important;
    color: #3c577a !important; font-weight: 500 !important;
    padding: 4px 0 !important; box-shadow: none !important;
}}

/* ── Inputs ── */
.stTextInput > div > div > input, .stTextArea textarea, .stNumberInput input {{
    font-family: 'Albert Sans', sans-serif !important;
    border: 1.5px solid #e0e0e0 !important; border-radius: 10px !important;
    padding: 12px 14px !important; font-size: 15px !important;
    color: #000 !important; background: #f9f9f9 !important;
}}
.stTextInput > div > div > input:focus, .stTextArea textarea:focus {{
    border-color: #b78715 !important;
    box-shadow: 0 0 0 2px rgba(183,135,21,0.15) !important;
}}
.stTextInput label, .stTextArea label, .stNumberInput label {{
    color: #9b928b !important; font-size: 13px !important; font-weight: 500 !important;
}}

/* ── Checkbox ── */
.stCheckbox input[type="checkbox"] {{ accent-color: #b78715 !important; width: 18px !important; height: 18px !important; }}
.stCheckbox label span {{ color: #000 !important; font-size: 14px !important; }}

/* ── Radio ── */
.stRadio label {{ color: #000 !important; font-size: 15px !important; }}
.stRadio input[type="radio"]:checked {{ accent-color: #b78715 !important; }}

/* ── Tabs – kein beweglicher Unterstrich ── */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1.5px solid #f0f0f0 !important; gap: 0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'Albert Sans', sans-serif !important;
    font-weight: 500 !important; font-size: 15px !important;
    color: #9b928b !important;
    border-bottom: 2px solid transparent !important;
    padding: 12px 24px !important; flex: 1 !important;
    justify-content: center !important;
    transition: none !important;
}}
.stTabs [aria-selected="true"] {{
    color: #b78715 !important;
    border-bottom: 2px solid #b78715 !important;
    background: transparent !important;
}}
.stTabs [data-baseweb="tab-highlight"] {{ display: none !important; }}
.stTabs [data-baseweb="tab-border"] {{ display: none !important; }}

/* ── Alerts ── */
.stAlert {{ border-radius: 12px !important; font-family: 'Albert Sans', sans-serif !important; }}
.stCaption {{ color: #9b928b !important; font-size: 13px !important; }}
hr {{ border: none !important; border-top: 1px solid #f0f0f0 !important; margin: 10px 0 !important; }}

/* ── Kamera Fullscreen ── */
[data-testid="stCameraInput"] {{
    position: fixed !important; top: 0 !important; left: 0 !important;
    width: 100vw !important; height: 100vh !important;
    z-index: 8000 !important; background: #000 !important;
    display: flex !important; flex-direction: column !important;
}}
[data-testid="stCameraInput"] video {{
    width: 100% !important; height: calc(100vh - 80px) !important;
    object-fit: cover !important;
}}
[data-testid="stCameraInput"] button {{
    position: absolute !important; bottom: 20px !important;
    left: 50% !important; transform: translateX(-50%) !important;
    background: #b78715 !important; color: #fff !important;
    border: none !important; border-radius: 50px !important;
    padding: 14px 40px !important; font-size: 16px !important;
    font-weight: 600 !important; z-index: 8001 !important;
}}

/* ── Bottom Navigation ── */
.nav-wrapper {{
    position: fixed; bottom: 0; left: 50%; transform: translateX(-50%);
    width: 100%; max-width: 430px;
    background: #fff; border-top: 1px solid #f0f0f0;
    z-index: 9000; box-shadow: 0 -2px 12px rgba(0,0,0,0.07);
    display: flex; align-items: stretch;
}}
/* FIX: background-size auf "auto 68px" → Icon füllt die Nav-Bar-Höhe korrekt aus */
.nav-wrapper .stButton > button {{
    background-color: transparent !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: auto 68px !important;
    border: none !important; border-radius: 0 !important;
    width: 100% !important; height: 72px !important;
    color: transparent !important; font-size: 1px !important;
    box-shadow: none !important; padding: 0 !important;
}}

/* Profil List Rows */
.profil-row {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 4px; border-bottom: 1px solid #f0f0f0; cursor: pointer;
}}
.profil-row-label {{ font-size: 16px; color: #000; font-weight: 400; font-family: 'Albert Sans', sans-serif; }}
.profil-row-right {{ display: flex; align-items: center; gap: 8px; }}
.profil-row-value {{ font-size: 14px; color: #9b928b; font-family: 'Albert Sans', sans-serif; }}
.profil-row-arrow {{ font-size: 16px; color: #9b928b; }}
.profil-section-title {{
    font-size: 13px; font-weight: 600; color: #9b928b;
    text-transform: uppercase; letter-spacing: 0.5px;
    font-family: 'Albert Sans', sans-serif;
    margin: 20px 0 0; padding-bottom: 2px;
}}
.profil-row-btn .stButton > button {{
    position: absolute !important; top: 0 !important; left: 0 !important;
    width: 100% !important; height: 100% !important;
    opacity: 0 !important; cursor: pointer !important;
    border-radius: 0 !important;
}}
.profil-row-container {{ position: relative; }}

/* Upgrade Tabelle: nur horizontale Linien */
.upgrade-table {{
    width: 100%; border-collapse: collapse;
    font-family: 'Albert Sans', sans-serif; font-size: 15px; margin: 8px 0;
}}
.upgrade-table th {{
    text-align: left; padding: 10px 8px; font-weight: 600;
    color: #9b928b; border-bottom: 1.5px solid #f0f0f0;
    border-left: none !important; border-right: none !important;
}}
.upgrade-table th.plan {{ text-align: center; width: 70px; }}
.upgrade-table th.plus {{ color: #b78715; }}
.upgrade-table td {{
    padding: 14px 8px; border-bottom: 1px solid #f5f5f5;
    color: #000; border-left: none !important; border-right: none !important;
}}
.upgrade-table td.center {{ text-align: center; color: #9b928b; }}
.upgrade-table td.ja {{ text-align: center; color: #b78715; }}

/* Gericht Card */
.gericht-card {{
    background: #f9f9f9; border-radius: 14px; padding: 14px 16px;
    margin-bottom: 10px; border: 1px solid #f0f0f0;
}}
.gericht-nr {{ font-size: 12px; color: #9b928b; margin-bottom: 2px; }}
.gericht-name {{ font-size: 16px; font-weight: 600; color: #000; }}
.gericht-preis {{ font-size: 14px; color: #b78715; font-weight: 500; margin-top: 4px; }}
.ampel-sicher {{ color: #2e7d32; font-size: 13px; font-weight: 500; }}
.ampel-warnung {{ color: #c0392b; font-size: 13px; font-weight: 500; }}

/* Disclaimer Box */
.disclaimer-box {{
    background: #f9f9f9; border-radius: 14px; padding: 20px; margin: 16px 0;
    font-family: 'Albert Sans', sans-serif; font-size: 14px;
    line-height: 1.7; color: #000;
}}

/* Scan Limit */
.scan-limit-box {{
    background: #fffbf0; border: 1.5px solid #b78715; border-radius: 16px;
    padding: 24px; text-align: center; margin: 24px 0;
    font-family: 'Albert Sans', sans-serif;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SUPABASE
# ─────────────────────────────────────────────
@st.cache_resource
def init_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_supabase()

# ─────────────────────────────────────────────
# KONFIGURATION
# ─────────────────────────────────────────────
ALLERGEN_LABELS = {
    "A": "Glutenhaltiges Getreide (Weizen, Roggen, Gerste, Hafer, Dinkel ...)",
    "B": "Krebstiere",
    "C": "Eier",
    "D": "Fische",
    "E": "Erdnüsse",
    "F": "Soja",
    "G": "Milch (Kuh, Schaf, Ziege, Pferd, Esel und Erzeugnisse)",
    "H": "Schalenfrüchte (Mandeln, Haselnüsse, Walnüsse, Cashews ...)",
    "L": "Sellerie",
    "M": "Senf",
    "N": "Sesam",
    "O": "Schwefeldioxid und Sulfite (> 10 mg/kg oder 10 mg/l)",
    "P": "Lupinen",
    "R": "Weichtiere"
}
ALLERGEN_SHORT = {
    "A": "Gluten", "B": "Krebstiere", "C": "Eier", "D": "Fische",
    "E": "Erdnüsse", "F": "Soja", "G": "Milch", "H": "Schalenfrüchte",
    "L": "Sellerie", "M": "Senf", "N": "Sesam", "O": "Sulfite",
    "P": "Lupinen", "R": "Weichtiere"
}
FREEMIUM_SCAN_LIMIT = 3

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for k, v in {
    "page": "disclaimer",
    "user": None,
    "profile": None,
    "user_allergene": [],
    "disclaimer_accepted": False,
    # FIX: Eigenes Flag für Onboarding-Status (getrennt von disclaimer_accepted)
    # Verhindert, dass allergen_settings fälschlicherweise denkt, kein Onboarding läuft
    "onboarding_complete": False,
    "restaurant_logged_in": False,
    "restaurant_data": None,
    "active_tab": "scan",
    "local_scan_count": 0,
    "camera_active": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def navigate(page):
    st.session_state.page = page
    st.rerun()

# ─────────────────────────────────────────────
# HILFSFUNKTIONEN
# ─────────────────────────────────────────────
def load_profile(user_id):
    res = supabase.table("user_profiles").select("*").eq("id", user_id).single().execute()
    if res.data:
        p = res.data
        st.session_state.profile = p
        # FIX: Lokales disclaimer_accepted NICHT mit False aus DB überschreiben.
        # Wenn der User als Gast akzeptiert hat und sich danach einloggt/registriert,
        # bleibt die Akzeptanz erhalten.
        if not st.session_state.disclaimer_accepted:
            st.session_state.disclaimer_accepted = p.get("disclaimer_accepted", False)
        st.session_state.user_allergene = [k for k in ALLERGEN_LABELS if p.get(k, False)]

def save_allergene(selected):
    st.session_state.user_allergene = selected
    if not st.session_state.user:
        return
    upd = {k: (k in selected) for k in ALLERGEN_LABELS}
    supabase.table("user_profiles").update(upd).eq("id", st.session_state.user.id).execute()

def save_disclaimer():
    st.session_state.disclaimer_accepted = True
    if not st.session_state.user:
        return
    from datetime import datetime, timezone
    supabase.table("user_profiles").update({
        "disclaimer_accepted": True,
        "disclaimer_accepted_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", st.session_state.user.id).execute()

def get_scan_count():
    if not st.session_state.user:
        return st.session_state.local_scan_count
    res = supabase.table("scan_log").select("id", count="exact").eq("user_id", st.session_state.user.id).execute()
    return res.count or 0

def log_scan(scan_type):
    if not st.session_state.user:
        st.session_state.local_scan_count += 1
    else:
        supabase.table("scan_log").insert({"user_id": st.session_state.user.id, "scan_type": scan_type}).execute()

def is_premium():
    return st.session_state.profile and st.session_state.profile.get("plan") == "premium"

def check_ampel(gericht, allergene):
    for a in allergene:
        if gericht.get(a):
            return False, ALLERGEN_SHORT[a]
    return True, ""

# ─────────────────────────────────────────────
# BOTTOM NAVIGATION
# ─────────────────────────────────────────────
def bottom_nav():
    tab = st.session_state.active_tab
    p_icon = ICON_PROFIL_AKTIV if tab == "profil"       else ICON_PROFIL_PASSIV
    s_icon = ICON_SCAN_AKTIV   if tab == "scan"         else ICON_SCAN_PASSIV
    r_icon = ICON_REST_AKTIV   if tab == "restaurants"  else ICON_REST_PASSIV

    st.markdown(f"""
    <style>
    div[data-testid="column"]:nth-of-type(1) .stButton > button {{
        background-image: url('data:image/svg+xml;base64,{p_icon}') !important;
    }}
    div[data-testid="column"]:nth-of-type(2) .stButton > button {{
        background-image: url('data:image/svg+xml;base64,{s_icon}') !important;
    }}
    div[data-testid="column"]:nth-of-type(3) .stButton > button {{
        background-image: url('data:image/svg+xml;base64,{r_icon}') !important;
    }}
    </style>
    <div class="nav-wrapper">
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("p", key="nb_p", use_container_width=True):
            st.session_state.active_tab = "profil"
            navigate("profil_uebersicht")
    with c2:
        if st.button("s", key="nb_s", use_container_width=True):
            st.session_state.active_tab = "scan"
            navigate("scan")
    with c3:
        if st.button("r", key="nb_r", use_container_width=True):
            st.session_state.active_tab = "restaurants"
            navigate("restaurants")

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEITE 1: DISCLAIMER
# ─────────────────────────────────────────────
def page_disclaimer():
    st.markdown("# 🥜 Nuss-Checker")
    st.markdown("---")
    st.markdown("## Wichtiger Hinweis")
    st.markdown("""
    <div class="disclaimer-box">
    <strong>Diese App dient ausschließlich als Hilfestellung.</strong><br><br>
    Der Nuss-Checker kann keine Garantie für die Richtigkeit, Vollständigkeit
    oder Aktualität der angezeigten Allergeninformationen übernehmen.
    Die Angaben basieren auf Daten Dritter (Restaurants, Hersteller, Open Food DB)
    und können fehlerhaft oder veraltet sein.<br><br>
    Bei schweren Allergien oder Unverträglichkeiten wende dich bitte immer
    direkt an das Restaurant oder den Hersteller und konsultiere im Zweifelsfall einen Arzt.<br><br>
    <strong>Die Nutzung der App erfolgt auf eigene Verantwortung.</strong>
    </div>
    """, unsafe_allow_html=True)

    accepted = st.checkbox("Ich habe den Hinweis gelesen und akzeptiere, dass diese App keine Haftung übernimmt.")

    def start():
        save_disclaimer()
        navigate("allergen_settings")

    st.button("App starten →", on_click=start, type="primary", disabled=not accepted)

# ─────────────────────────────────────────────
# SEITE 2: ALLERGEN-EINSTELLUNGEN
# ─────────────────────────────────────────────
def page_allergen_settings():
    # FIX: Onboarding-Status über eigenes Flag prüfen, nicht über disclaimer_accepted.
    # disclaimer_accepted wird schon auf True gesetzt, bevor man hier hinnavigiert —
    # daher war is_onboarding vorher immer False (= falsches Verhalten).
    is_onboarding = not st.session_state.onboarding_complete

    if not is_onboarding:
        if st.button("← Zurück"):
            navigate("profil_uebersicht")

    st.markdown("# Meine Allergene")
    st.markdown('<p style="color:#9b928b;font-size:14px;margin-bottom:8px">Welche Allergene soll die App für dich hervorheben?</p>', unsafe_allow_html=True)

    selected = []
    for key, label in ALLERGEN_LABELS.items():
        checked = st.checkbox(f"**{key}** – {label}", value=(key in st.session_state.user_allergene), key=f"al_{key}")
        if checked:
            selected.append(key)

    st.markdown("---")

    def save_and_go():
        save_allergene(selected)
        # FIX: Onboarding als abgeschlossen markieren
        st.session_state.onboarding_complete = True
        navigate("scan")

    btn = "Speichern und weiter →" if is_onboarding else "Speichern"
    st.button(btn, on_click=save_and_go, type="primary")

    if not is_onboarding:
        bottom_nav()

# ─────────────────────────────────────────────
# SEITE 3: AUTH
# ─────────────────────────────────────────────
def page_auth():
    tab_reg, tab_login = st.tabs(["Registrieren", "Einloggen"])

    with tab_reg:
        st.markdown("## Neues Konto")
        reg_type = st.radio("", ["Ich bin Endkunde", "Ich registriere mich als Restaurant"],
                            label_visibility="collapsed", key="reg_type")
        email_r = st.text_input("E-Mail-Adresse", key="reg_email")
        pw_r    = st.text_input("Passwort (mindestens 6 Zeichen)", type="password", key="reg_pw")
        pw_r2   = st.text_input("Passwort wiederholen", type="password", key="reg_pw2")

        is_restaurant = "Restaurant" in reg_type
        rest_name = rest_land = rest_plz = rest_adresse = rest_hnr = ""
        if is_restaurant:
            rest_name    = st.text_input("Restaurantname", key="rn")
            rest_land    = st.text_input("Land", key="rl")
            rest_plz     = st.text_input("Postleitzahl", key="rp")
            rest_adresse = st.text_input("Adresse", key="ra")
            rest_hnr     = st.text_input("Hausnummer", key="rh")

        all_ok = bool(email_r and pw_r and pw_r2)
        if is_restaurant:
            all_ok = all_ok and bool(rest_name and rest_land)

        btn_lbl = "Registrieren" if is_restaurant else "Für 2,99 €/Monat registrieren"

        def do_register():
            if pw_r != pw_r2:
                st.error("Passwörter stimmen nicht überein.")
                return
            if len(pw_r) < 6:
                st.error("Passwort muss mindestens 6 Zeichen haben.")
                return
            try:
                res = supabase.auth.sign_up({"email": email_r, "password": pw_r})
                st.session_state.user = res.user
                load_profile(res.user.id)
                if is_restaurant:
                    supabase.table("restaurants").insert({
                        "owner_id": res.user.id, "name": rest_name,
                        "adresse": f"{rest_adresse} {rest_hnr}, {rest_plz} {rest_land}"
                    }).execute()
                # FIX: Nach Registrierung nicht immer zum Disclaimer.
                # User hat Disclaimer bereits akzeptiert → weiter zum nächsten sinnvollen Screen.
                if st.session_state.disclaimer_accepted:
                    navigate("scan")
                else:
                    navigate("disclaimer")
            except Exception as e:
                st.error(f"Registrierung fehlgeschlagen: {e}")

        st.button(btn_lbl, on_click=do_register, type="primary", disabled=not all_ok)
        st.caption("Nach der Registrierung bitte E-Mail bestätigen.")

    with tab_login:
        st.markdown("## Anmelden")
        email_l = st.text_input("E-Mail-Adresse", key="login_email")
        pw_l    = st.text_input("Passwort", type="password", key="login_pw")
        st.markdown('<p style="color:#3c577a;font-size:13px">Passwort vergessen?</p>', unsafe_allow_html=True)

        def do_login():
            try:
                res = supabase.auth.sign_in_with_password({"email": email_l, "password": pw_l})
                st.session_state.user = res.user
                # load_profile überschreibt disclaimer_accepted nur falls es lokal False ist (FIX oben)
                load_profile(res.user.id)
                navigate("scan" if st.session_state.disclaimer_accepted else "disclaimer")
            except Exception as e:
                st.error(f"Login fehlgeschlagen: {e}")

        st.button("Einloggen", on_click=do_login, type="primary")

    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 4: SCAN
# ─────────────────────────────────────────────
def page_scan():
    st.session_state.active_tab = "scan"
    scan_count = get_scan_count()

    if not is_premium() and scan_count >= FREEMIUM_SCAN_LIMIT:
        st.markdown(f"""
        <div class="scan-limit-box">
            <p style="font-size:16px;color:#000;line-height:1.6;margin-bottom:20px">
                Du hast heute schon<br>
                <strong>{FREEMIUM_SCAN_LIMIT}-mal geprüft.</strong><br>
                Unterstütze uns, um unbegrenzt zu scannen!
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Upgrade für 2,99 €/Monat", type="primary", on_click=lambda: navigate("upgrade"))
        bottom_nav()
        return

    if not is_premium():
        st.caption(f"Noch {FREEMIUM_SCAN_LIMIT - scan_count} von {FREEMIUM_SCAN_LIMIT} heutigen Scans")

    scan_mode = st.radio("", [
        "🛒 Produktetikett",
        "🌍 Fremdsprachiges Etikett",
        "📋 Restaurant QR-Code"
    ], label_visibility="collapsed", horizontal=True)

    camera_image = st.camera_input("", label_visibility="collapsed")

    if camera_image:
        st.markdown("---")
        if "Produktetikett" in scan_mode:
            log_scan("produkt")
            st.markdown("#### 🔍 Erkannte Allergene")
            st.info("⚙️ Texterkennung folgt in Phase 2 (OCR)")
            for a in st.session_state.user_allergene:
                st.markdown(f'<p class="ampel-warnung">⚠️ Enthält: {ALLERGEN_SHORT[a]}</p>', unsafe_allow_html=True)
            if st.session_state.user_allergene:
                st.button("🔄 Sichere Alternativen", type="primary", on_click=lambda: navigate("alternatives"))
        elif "Fremdsprachig" in scan_mode:
            log_scan("fremdsprache")
            st.info("⚙️ Übersetzungs-API folgt in Phase 2")
            for a in st.session_state.user_allergene:
                st.markdown(f'<p class="ampel-warnung">⚠️ Enthält: {ALLERGEN_SHORT[a]}</p>', unsafe_allow_html=True)
        else:
            log_scan("qr_code")
            st.info("⚙️ QR-Decode folgt in Phase 2")
            st.button("🍽️ Speisekarte öffnen", type="primary", on_click=lambda: navigate("restaurants"))

    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 5: RESTAURANTS
# ─────────────────────────────────────────────
def page_restaurants():
    st.session_state.active_tab = "restaurants"

    tab_karte, tab_liste, tab_lesezeichen = st.tabs(["Karte", "Liste", "Lesezeichen"])

    with tab_karte:
        st.info("⚙️ Kartenansicht folgt in Phase 2 (Google Maps / Mapbox)")

    with tab_liste:
        try:
            res = supabase.table("restaurants").select("id, name, adresse").eq("aktiv", True).execute()
            restaurants = res.data or []
        except:
            restaurants = []

        if not restaurants:
            st.markdown('<p style="color:#9b928b">Noch keine Restaurants eingetragen.</p>', unsafe_allow_html=True)
        else:
            for r in restaurants:
                col1, col2 = st.columns([8, 1])
                with col1:
                    if st.button(f"**{r['name']}**  \n{r.get('adresse','')}", key=f"r_{r['id']}"):
                        st.session_state["sel_rest_id"] = r["id"]
                        st.session_state["sel_rest_name"] = r["name"]
                        navigate("speisekarte")
                with col2:
                    st.markdown(svg_img(ICON_FAV_PASSIV, "24px"), unsafe_allow_html=True)
                st.markdown("<hr style='margin:4px 0'>", unsafe_allow_html=True)

    with tab_lesezeichen:
        if not is_premium():
            st.markdown('<div class="disclaimer-box" style="text-align:center"><strong>Plus-Feature</strong><br>Lesezeichen sind im Plus-Tarif verfügbar.</div>', unsafe_allow_html=True)
            st.button("Upgrade für 2,99 €/Monat", type="primary", on_click=lambda: navigate("upgrade"))
        else:
            st.info("Deine gespeicherten Restaurants erscheinen hier.")

    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 6: SPEISEKARTE
# ─────────────────────────────────────────────
def page_speisekarte():
    rest_name = st.session_state.get("sel_rest_name", "Speisekarte")
    rest_id   = st.session_state.get("sel_rest_id")
    st.markdown(f"# {rest_name}")
    if st.session_state.user_allergene:
        st.caption("Gefiltert nach: " + " · ".join([ALLERGEN_SHORT[a] for a in st.session_state.user_allergene]))
    st.markdown("---")

    try:
        q = supabase.table("gerichte").select("*").eq("aktiv", True)
        if rest_id:
            q = q.eq("restaurant_id", rest_id)
        gerichte = q.execute().data or []
    except Exception as e:
        st.error(f"Fehler: {e}")
        gerichte = []

    for g in gerichte:
        sicher, warnung = check_ampel(g, st.session_state.user_allergene)
        if st.session_state.user_allergene and not sicher:
            continue
        preis = f"{g.get('preis','–')} €" if g.get("preis") else "–"
        ampel = '<span class="ampel-sicher">✓ Verträglich</span>' if sicher else f'<span class="ampel-warnung">⚠️ Enthält {warnung}</span>'
        st.markdown(f"""
        <div class="gericht-card">
            <div class="gericht-nr">Nr. {g.get('gericht_nummer','–')}</div>
            <div class="gericht-name">{g.get('name','')}</div>
            <div style="font-size:13px;color:#9b928b;margin:4px 0">{g.get('beschreibung','')}</div>
            <div class="gericht-preis">{preis}</div>
            <div style="margin-top:6px">{ampel}</div>
        </div>
        """, unsafe_allow_html=True)

    if not gerichte:
        st.markdown('<p style="color:#9b928b">Noch keine Gerichte eingetragen.</p>', unsafe_allow_html=True)

    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 7: SICHERE ALTERNATIVEN
# ─────────────────────────────────────────────
def page_alternatives():
    st.markdown("# Sichere Alternativen")
    if st.session_state.user_allergene:
        st.caption("Gefiltert nach: " + " · ".join([ALLERGEN_SHORT[a] for a in st.session_state.user_allergene]))
    st.markdown("---")
    st.info("⚙️ Open Food Facts DB folgt in Phase 2.")
    import pandas as pd
    df = pd.DataFrame({
        "Produkt": ["Rote Linsen", "Kichererbsen", "Quinoa"],
        "Marke": ["Ja! Natürlich", "Spar Bio", "dm Bio"],
        "Status": ["✅ Sicher", "✅ Sicher", "✅ Sicher"]
    })
    st.dataframe(df, use_container_width=True)
    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 8: PROFIL
# ─────────────────────────────────────────────
def page_profil_uebersicht():
    st.session_state.active_tab = "profil"
    st.markdown("# Profil")

    plan = "Plus" if is_premium() else "Gratistarif"

    st.markdown('<div class="profil-section-title">Konto</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="profil-row" id="row-abo">
        <span class="profil-row-label">Abonnement</span>
        <span class="profil-row-right">
            <span class="profil-row-value">{plan}</span>
            <span class="profil-row-arrow">›</span>
        </span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Abonnement", key="btn_abo", use_container_width=True):
        navigate("upgrade")
    st.markdown("""
    <style>
    button[data-key="btn_abo"] {
        position: relative !important; margin-top: -52px !important;
        height: 52px !important; opacity: 0 !important; z-index: 10 !important;
        border-radius: 0 !important; background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="profil-section-title">App</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="profil-row">
        <span class="profil-row-label">Meine Allergene</span>
        <span class="profil-row-arrow">›</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Meine Allergene", key="btn_alg", use_container_width=True):
        navigate("allergen_settings")
    st.markdown("""
    <style>
    button[data-key="btn_alg"] {
        position: relative !important; margin-top: -52px !important;
        height: 52px !important; opacity: 0 !important; z-index: 10 !important;
        border-radius: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="profil-row">
        <span class="profil-row-label">Sprache</span>
        <span class="profil-row-right">
            <span class="profil-row-value">Deutsch</span>
            <span class="profil-row-arrow">›</span>
        </span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Sprache", key="btn_lang", use_container_width=True):
        st.toast("Mehrsprachigkeit folgt in Phase 2 ⚙️")
    st.markdown("""
    <style>
    button[data-key="btn_lang"] {
        position: relative !important; margin-top: -52px !important;
        height: 52px !important; opacity: 0 !important; z-index: 10 !important;
        border-radius: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.user:
        def do_logout():
            supabase.auth.sign_out()
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
        st.button("🚪 Abmelden", on_click=do_logout)
    else:
        st.caption("Noch kein Konto?")
        st.button("Anmelden / Registrieren", type="secondary", on_click=lambda: navigate("auth"))

    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 9: UPGRADE
# ─────────────────────────────────────────────
def page_upgrade():
    st.markdown("# Hol dir Nuss-Checker Plus")
    st.markdown('<p style="color:#9b928b;font-size:14px">Alle Funktionen, keine Limits.</p>', unsafe_allow_html=True)
    st.markdown("---")

    haken = svg_img(ICON_HAKEN, "18px")
    st.markdown(f"""
    <table class="upgrade-table">
        <thead>
            <tr>
                <th>Funktion</th>
                <th class="plan free">Free</th>
                <th class="plan plus">Plus</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Tägliche Scans</td>
                <td class="center">3</td>
                <td class="ja">∞</td>
            </tr>
            <tr>
                <td>Sichere Alternativen</td>
                <td class="center">–</td>
                <td class="ja">{haken}</td>
            </tr>
            <tr>
                <td>Lesezeichen</td>
                <td class="center">–</td>
                <td class="ja">{haken}</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.button("Upgrade für 2,99 €/Monat →", type="primary", on_click=lambda: navigate("auth"))
    st.caption("⚙️ Zahlungsabwicklung via Stripe folgt in Phase 2.")
    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 10: RESTAURANT ADMIN
# ─────────────────────────────────────────────
def page_restaurant_admin():
    st.markdown("# Restaurant-Verwaltung")

    if not st.session_state.restaurant_logged_in:
        st.markdown("## Login")
        email_r = st.text_input("E-Mail", key="rl_e")
        pw_r    = st.text_input("Passwort", type="password", key="rl_p")

        def do_rest_login():
            try:
                res = supabase.auth.sign_in_with_password({"email": email_r, "password": pw_r})
                rr = supabase.table("restaurants").select("*").eq("owner_id", res.user.id).single().execute()
                if rr.data:
                    st.session_state.restaurant_logged_in = True
                    st.session_state.restaurant_data = rr.data
                    st.session_state.user = res.user
                    st.rerun()
                else:
                    st.error("Kein Restaurant-Account gefunden.")
            except Exception as e:
                st.error(f"Login fehlgeschlagen: {e}")

        st.button("Einloggen", on_click=do_rest_login, type="primary")
    else:
        r = st.session_state.restaurant_data
        st.success(f"Eingeloggt als: **{r['name']}**")
        st.markdown("---")
        st.markdown("## Gericht hinzufügen")
        gericht_nr   = st.text_input("Gerichtnummer (z.B. 14 oder B2)")
        gericht_name = st.text_input("Name des Gerichts")
        beschreibung = st.text_area("Beschreibung")
        preis        = st.number_input("Preis (€)", min_value=0.0, step=0.5)
        st.markdown("**Enthaltene Allergene:**")
        cols = st.columns(4)
        allergen_sel = {}
        for i, (key, lbl) in enumerate(ALLERGEN_SHORT.items()):
            with cols[i % 4]:
                allergen_sel[key] = st.checkbox(f"{key}", key=f"adm_{key}", help=lbl)

        def save_gericht():
            try:
                supabase.table("gerichte").insert({
                    "restaurant_id": r["id"], "gericht_nummer": gericht_nr,
                    "name": gericht_name, "beschreibung": beschreibung,
                    "preis": preis, **allergen_sel
                }).execute()
                st.success("✅ Gericht gespeichert!")
            except Exception as e:
                st.error(f"Fehler: {e}")

        st.button("💾 Gericht speichern", on_click=save_gericht, type="primary")
        st.markdown("---")
        st.button("🚪 Ausloggen", on_click=lambda: [
            st.session_state.__setitem__("restaurant_logged_in", False),
            st.session_state.__setitem__("restaurant_data", None),
            navigate("profil_uebersicht")
        ])

    bottom_nav()

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
page = st.session_state.page

routes = {
    "disclaimer":        page_disclaimer,
    "allergen_settings": page_allergen_settings,
    "auth":              page_auth,
    "scan":              page_scan,
    "restaurants":       page_restaurants,
    "speisekarte":       page_speisekarte,
    "alternatives":      page_alternatives,
    "profil_uebersicht": page_profil_uebersicht,
    "upgrade":           page_upgrade,
    "restaurant_admin":  page_restaurant_admin,
}

routes.get(page, page_scan)()
