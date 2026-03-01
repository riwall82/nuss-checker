{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww17920\viewh14060\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import time\
\
# --- INITIALISIERUNG (SESSION STATE) ---\
if 'authenticated' not in st.session_state:\
    st.session_state['authenticated'] = False\
if 'scan_count' not in st.session_state:\
    st.session_state['scan_count'] = 0\
\
# --- DESIGN (CSS) ---\
st.markdown("""\
    <style>\
    .stButton>button \{ width: 100%; border-radius: 20px; height: 3em; background-color: #009EE3; color: white; \}\
    .footer \{ position: fixed; bottom: 0; left: 0; width: 100%; background-color: #D9D9D9; padding: 20px; text-align: center; border-top: 1px solid #ccc; \}\
    .scan-btn \{ display: inline-block; width: 80px; height: 80px; background-color: #009EE3; border-radius: 50%; margin: 10px; color: white; line-height: 80px; font-size: 12px; font-weight: bold; \}\
    </style>\
    """, unsafe_allow_html=True)\
\
# --- LOGIK: SCREEN 1 (DISCLAIMER) ---\
if not st.session_state['authenticated']:\
    st.title("Disklaimer")\
    st.write("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat.")\
    \
    akzeptiert = st.checkbox("Disklaimer akzeptiert")\
    \
    if st.button("App starten"):\
        if akzeptiert:\
            st.session_state['authenticated'] = True\
            st.rerun()\
        else:\
            st.warning("Bitte akzeptiere zuerst den Disklaimer.")\
\
# --- LOGIK: SCREEN 2 (HAUPTSCREEN / UPGRADE) ---\
else:\
    # Header\
    st.markdown("<div style='background-color: #D9D9D9; height: 60px; margin: -50px -20px 20px -20px;'></div>", unsafe_allow_html=True)\
    \
    # Platzhalter f\'fcr Content\
    st.write("### Dein Scanner")\
    st.write("Hier erscheinen die Ergebnisse deiner Pr\'fcfung.")\
\
    # Status-Logik (Dein Layout)\
    max_scans = 3\
    remaining = max_scans - st.session_state['scan_count']\
\
    st.markdown("---")\
    \
    if st.session_state['scan_count'] < max_scans:\
        st.info(f"Du hast noch \{remaining\} Scans f\'fcr heute frei.")\
        # Beispiel-Button um Scan zu simulieren\
        if st.button("Simuliere Scan"):\
            st.session_state['scan_count'] += 1\
            st.success("Scan erfolgreich durchgef\'fchrt!")\
            time.sleep(1)\
            st.rerun()\
    else:\
        st.error("Du hast heute schon 3-mal gepr\'fcft. Unterst\'fctze uns, um unbegrenzt zu scannen!")\
        if st.button("Erstelle ein Konto"):\
            st.write("Leite weiter zur Registrierung...")\
\
    # Footer mit den runden Buttons (Deine Skizze)\
    st.markdown(f"""\
        <div class='footer'>\
            <div style='display: flex; justify-content: center;'>\
                <div style='text-align: center;'>\
                    <div class='scan-btn'>SCAN</div>\
                    <div style='font-size: 10px; color: black;'>Barcode scannen</div>\
                </div>\
                <div style='text-align: center;'>\
                    <div class='scan-btn'>LIVE</div>\
                    <div style='font-size: 10px; color: black;'>Live-Texterkennung</div>\
                </div>\
            </div>\
        </div>\
    """, unsafe_allow_html=True)}