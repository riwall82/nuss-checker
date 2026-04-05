import streamlit as st
from supabase import create_client, Client

st.set_page_config(
    page_title="Nuss-Checker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# ICONS (base64 encoded SVGs)
# ─────────────────────────────────────────────
ICON_PROFIL_AKTIV    = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgewogICAgICAgIGZpbGw6ICNiMWIyYjI7CiAgICAgIH0KCiAgICAgIC5jbHMtMiB7CiAgICAgICAgZm9udC1mYW1pbHk6IEFsYmVydFNhbnNSb21hbi1NZWRpdW0sICdBbGJlcnQgU2Fucyc7CiAgICAgICAgZm9udC1zaXplOiAxMnB4OwogICAgICAgIGZvbnQtdmFyaWF0aW9uLXNldHRpbmdzOiAnd2dodCcgNTAwOwogICAgICAgIGZvbnQtd2VpZ2h0OiA1MDA7CiAgICAgIH0KCiAgICAgIC5jbHMtMiwgLmNscy0zIHsKICAgICAgICBmaWxsOiAjYjc4NzE1OwogICAgICB9CgogICAgICAuY2xzLTQgewogICAgICAgIHN0cm9rZTogI2I3ODcxNTsKICAgICAgfQoKICAgICAgLmNscy00LCAuY2xzLTUgewogICAgICAgIGZpbGw6IG5vbmU7CiAgICAgICAgc3Ryb2tlLWxpbmVjYXA6IHJvdW5kOwogICAgICAgIHN0cm9rZS1saW5lam9pbjogcm91bmQ7CiAgICAgICAgc3Ryb2tlLXdpZHRoOiAxLjdweDsKICAgICAgfQoKICAgICAgLmNscy02IHsKICAgICAgICBsZXR0ZXItc3BhY2luZzogLS4wMWVtOwogICAgICB9CgogICAgICAuY2xzLTUgewogICAgICAgIHN0cm9rZTogI2IxYjJiMjsKICAgICAgfQogICAgPC9zdHlsZT4KICA8L2RlZnM+CiAgPHRleHQgY2xhc3M9ImNscy0yIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0OS4xMyA2MCkiPjx0c3BhbiB4PSIwIiB5PSIwIj5QPC90c3Bhbj48dHNwYW4gY2xhc3M9ImNscy02IiB4PSI3LjQ2IiB5PSIwIj5yPC90c3Bhbj48dHNwYW4geD0iMTEuNyIgeT0iMCI+b2ZpbDwvdHNwYW4+PC90ZXh0PgogIDxwYXRoIGNsYXNzPSJjbHMtMyIgZD0iTTY0Ljc1LDM5LjMyYzMuODcsMCw3LjM0LTEuNjYsOS43Ny00LjI5LTEuMzktNC4wNy01LjIzLTctOS43Ny03cy04LjM5LDIuOTMtOS43Nyw3YzIuNDMsMi42Myw1LjksNC4yOSw5Ljc3LDQuMjlaIi8+CiAgPGNpcmNsZSBjbGFzcz0iY2xzLTMiIGN4PSI2NC43NSIgY3k9IjIxLjU0IiByPSI0Ljg0Ii8+CiAgPGNpcmNsZSBjbGFzcz0iY2xzLTQiIGN4PSI2NC43NSIgY3k9IjI1Ljk5IiByPSIxMy4xIi8+CiAgPHBhdGggY2xhc3M9ImNscy01IiBkPSJNNjQuNzUsOC40YzcuMjksMCwxMy41NCw0LjQzLDE2LjIxLDEwLjc0Ii8+CiAgPGNpcmNsZSBjbGFzcz0iY2xzLTEiIGN4PSI4MS40NSIgY3k9IjIyLjYyIiByPSIxLjA5Ii8+Cjwvc3ZnPg=="
ICON_PROFIL_PASSIV   = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgewogICAgICAgIGZpbGw6ICMzYzU3N2E7CiAgICAgIH0KCiAgICAgIC5jbHMtMiB7CiAgICAgICAgZmlsbDogIzZmNzA2ZjsKICAgICAgICBmb250LWZhbWlseTogQWxiZXJ0U2Fuc1JvbWFuLU1lZGl1bSwgJ0FsYmVydCBTYW5zJzsKICAgICAgICBmb250LXNpemU6IDEycHg7CiAgICAgICAgZm9udC12YXJpYXRpb24tc2V0dGluZ3M6ICd3Z2h0JyA1MDA7CiAgICAgICAgZm9udC13ZWlnaHQ6IDUwMDsKICAgICAgfQoKICAgICAgLmNscy0zIHsKICAgICAgICBmaWxsOiAjYjFiMmIyOwogICAgICB9CgogICAgICAuY2xzLTQgewogICAgICAgIHN0cm9rZTogIzNjNTc3YTsKICAgICAgfQoKICAgICAgLmNscy00LCAuY2xzLTUgewogICAgICAgIGZpbGw6IG5vbmU7CiAgICAgICAgc3Ryb2tlLWxpbmVjYXA6IHJvdW5kOwogICAgICAgIHN0cm9rZS1saW5lam9pbjogcm91bmQ7CiAgICAgICAgc3Ryb2tlLXdpZHRoOiAxLjdweDsKICAgICAgfQoKICAgICAgLmNscy02IHsKICAgICAgICBsZXR0ZXItc3BhY2luZzogLS4wMWVtOwogICAgICB9CgogICAgICAuY2xzLTUgewogICAgICAgIHN0cm9rZTogI2IxYjJiMjsKICAgICAgfQogICAgPC9zdHlsZT4KICA8L2RlZnM+CiAgPHRleHQgY2xhc3M9ImNscy0yIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0OS4xMyA2MCkiPjx0c3BhbiB4PSIwIiB5PSIwIj5QPC90c3Bhbj48dHNwYW4gY2xhc3M9ImNscy02IiB4PSI3LjQ2IiB5PSIwIj5yPC90c3Bhbj48dHNwYW4geD0iMTEuNyIgeT0iMCI+b2ZpbDwvdHNwYW4+PC90ZXh0PgogIDxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTY0Ljc1LDM5LjMyYzMuODcsMCw3LjM0LTEuNjYsOS43Ny00LjI5LTEuMzktNC4wNy01LjIzLTctOS43Ny03cy04LjM5LDIuOTMtOS43Nyw3YzIuNDMsMi42Myw1LjksNC4yOSw5Ljc3LDQuMjlaIi8+CiAgPGNpcmNsZSBjbGFzcz0iY2xzLTEiIGN4PSI2NC43NSIgY3k9IjIxLjU0IiByPSI0Ljg0Ii8+CiAgPGNpcmNsZSBjbGFzcz0iY2xzLTQiIGN4PSI2NC43NSIgY3k9IjI1Ljk5IiByPSIxMy4xIi8+CiAgPHBhdGggY2xhc3M9ImNscy01IiBkPSJNNjQuNzUsOC40YzcuMjksMCwxMy41NCw0LjQzLDE2LjIxLDEwLjc0Ii8+CiAgPGNpcmNsZSBjbGFzcz0iY2xzLTMiIGN4PSI4MS40NSIgY3k9IjIyLjYyIiByPSIxLjA5Ii8+Cjwvc3ZnPg=="
ICON_SCAN_AKTIV      = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgewogICAgICAgIGZpbGw6IG5vbmU7CiAgICAgICAgc3Ryb2tlOiAjYjc4NzE1OwogICAgICAgIHN0cm9rZS1saW5lY2FwOiByb3VuZDsKICAgICAgICBzdHJva2UtbWl0ZXJsaW1pdDogMTA7CiAgICAgICAgc3Ryb2tlLXdpZHRoOiAxLjdweDsKICAgICAgfQoKICAgICAgLmNscy0yIHsKICAgICAgICBmaWxsOiAjYjFiMmIyOwogICAgICB9CgogICAgICAuY2xzLTMgewogICAgICAgIGZpbGw6ICNiNzg3MTU7CiAgICAgICAgZm9udC1mYW1pbHk6IEFsYmVydFNhbnNSb21hbi1NZWRpdW0sICdBbGJlcnQgU2Fucyc7CiAgICAgICAgZm9udC1zaXplOiAxMnB4OwogICAgICAgIGZvbnQtdmFyaWF0aW9uLXNldHRpbmdzOiAnd2dodCcgNTAwOwogICAgICAgIGZvbnQtd2VpZ2h0OiA1MDA7CiAgICAgIH0KICAgIDwvc3R5bGU+CiAgPC9kZWZzPgogIDx0ZXh0IGNsYXNzPSJjbHMtMyIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNTQuODcgNjApIj48dHNwYW4geD0iMCIgeT0iMCI+U2NhbjwvdHNwYW4+PC90ZXh0PgogIDxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTQ2LjM3LDIwLjA5di0zLjA3YzAtMi4xNywxLjc2LTMuOTIsMy45Mi0zLjkyaDkuMDciLz4KICA8cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik00Ni4zNywzMi4zMnYzLjA3YzAsMi4xNywxLjc2LDMuOTIsMy45MiwzLjkyaDkuMDciLz4KICA8cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik05MS4wMywyMC4wOXYtMy4wN2MwLTIuMTctMS43Ni0zLjkyLTMuOTItMy45MmgtOS4wNyIvPgogIDxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTkxLjAzLDMyLjMydjMuMDdjMCwyLjE3LTEuNzYsMy45Mi0zLjkyLDMuOTJoLTkuMDciLz4KPC9zdmc+"
ICON_SCAN_PASSIV     = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgewogICAgICAgIGZpbGw6ICM2ZjcwNmY7CiAgICAgICAgZm9udC1mYW1pbHk6IEFsYmVydFNhbnNSb21hbi1NZWRpdW0sICdBbGJlcnQgU2Fucyc7CiAgICAgICAgZm9udC1zaXplOiAxMnB4OwogICAgICAgIGZvbnQtdmFyaWF0aW9uLXNldHRpbmdzOiAnd2dodCcgNTAwOwogICAgICAgIGZvbnQtd2VpZ2h0OiA1MDA7CiAgICAgIH0KCiAgICAgIC5jbHMtMiB7CiAgICAgICAgZmlsbDogbm9uZTsKICAgICAgICBzdHJva2U6ICMzYzU3N2E7CiAgICAgICAgc3Ryb2tlLWxpbmVjYXA6IHJvdW5kOwogICAgICAgIHN0cm9rZS1taXRlcmxpbWl0OiAxMDsKICAgICAgICBzdHJva2Utd2lkdGg6IDEuN3B4OwogICAgICB9CgogICAgICAuY2xzLTMgewogICAgICAgIGZpbGw6ICNiMWIyYjI7CiAgICAgIH0KICAgIDwvc3R5bGU+CiAgPC9kZWZzPgogIDx0ZXh0IGNsYXNzPSJjbHMtMSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNTQuODcgNjApIj48dHNwYW4geD0iMCIgeT0iMCI+U2NhbjwvdHNwYW4+PC90ZXh0PgogIDxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTQ2LjM3LDIwLjA5di0zLjA3YzAtMi4xNywxLjc2LTMuOTIsMy45Mi0zLjkyaDkuMDciLz4KICA8cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik00Ni4zNywzMi4zMnYzLjA3YzAsMi4xNywxLjc2LDMuOTIsMy45MiwzLjkyaDkuMDciLz4KICA8cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik05MS4wMywyMC4wOXYtMy4wN2MwLTIuMTctMS43Ni0zLjkyLTMuOTItMy45MmgtOS4wNyIvPgogIDxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTkxLjAzLDMyLjMydjMuMDdjMCwyLjE3LTEuNzYsMy45Mi0zLjkyLDMuOTJoLTkuMDciLz4KPC9zdmc+"
ICON_REST_AKTIV      = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgewogICAgICAgIGZpbGw6ICNmZmY7CiAgICAgICAgc3Ryb2tlLXdpZHRoOiAxLjIxcHg7CiAgICAgIH0KCiAgICAgIC5jbHMtMSwgLmNscy0yIHsKICAgICAgICBzdHJva2U6ICNiNzg3MTU7CiAgICAgIH0KCiAgICAgIC5jbHMtMSwgLmNscy0yLCAuY2xzLTMgewogICAgICAgIHN0cm9rZS1saW5lY2FwOiByb3VuZDsKICAgICAgICBzdHJva2UtbGluZWpvaW46IHJvdW5kOwogICAgICB9CgogICAgICAuY2xzLTQgewogICAgICAgIGZpbGw6ICNlNGU0ZTQ7CiAgICAgIH0KCiAgICAgIC5jbHMtNSB7CiAgICAgICAgZmlsbDogI2IxYjJiMjsKICAgICAgfQoKICAgICAgLmNscy02IHsKICAgICAgICBmaWxsOiAjYjc4NzE1OwogICAgICAgIGZvbnQtZmFtaWx5OiBBbGJlcnRTYW5zUm9tYW4tTWVkaXVtLCAnQWxiZXJ0IFNhbnMnOwogICAgICAgIGZvbnQtc2l6ZTogMTJweDsKICAgICAgICBmb250LXZhcmlhdGlvbi1zZXR0aW5nczogJ3dnaHQnIDUwMDsKICAgICAgICBmb250LXdlaWdodDogNTAwOwogICAgICB9CgogICAgICAuY2xzLTIsIC5jbHMtMyB7CiAgICAgICAgZmlsbDogbm9uZTsKICAgICAgICBzdHJva2Utd2lkdGg6IDEuN3B4OwogICAgICB9CgogICAgICAuY2xzLTMgewogICAgICAgIHN0cm9rZTogI2IxYjJiMjsKICAgICAgfQogICAgPC9zdHlsZT4KICA8L2RlZnM+CiAgPHBhdGggY2xhc3M9ImNscy00IiBkPSJNNzUuOTgsMzIuNzhWMTQuOThjMC0xLjE0LS45My0yLjA3LTIuMDctMi4wN2gtMTUuNjNjLTEuMTQsMC0yLjA3LjkzLTIuMDcsMi4wN3YzLjU5YzkuMDkuMjUsMTYuNzksNi4wOSwxOS43NywxNC4yMVoiLz4KICA8cmVjdCBjbGFzcz0iY2xzLTIiIHg9IjU2LjIiIHk9IjEyLjkxIiB3aWR0aD0iMTkuNzciIGhlaWdodD0iMjYuMTkiIHJ4PSIzLjU0IiByeT0iMy41NCIvPgogIDx0ZXh0IGNsYXNzPSJjbHMtNiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMzMuMDEgNjApIj48dHNwYW4geD0iMCIgeT0iMCI+UmVzdGF1cmFudHM8L3RzcGFuPjwvdGV4dD4KICA8cGF0aCBjbGFzcz0iY2xzLTMiIGQ9Ik02OS44Myw4LjQ2aDUuMjRjMi45MSwwLDUuMjcsMi4zNiw1LjI3LDUuMjd2NS41MiIvPgogIDxjaXJjbGUgY2xhc3M9ImNscy01IiBjeD0iODAuMzQiIGN5PSIyMi42MiIgcj0iMS4wOSIvPgo8L3N2Zz4="
ICON_REST_PASSIV     = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMzEgODQiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgewogICAgICAgIGZpbGw6ICNlNGU0ZTQ7CiAgICAgIH0KCiAgICAgIC5jbHMtMiB7CiAgICAgICAgZmlsbDogIzZmNzA2ZjsKICAgICAgICBmb250LWZhbWlseTogQWxiZXJ0U2Fuc1JvbWFuLU1lZGl1bSwgJ0FsYmVydCBTYW5zJzsKICAgICAgICBmb250LXNpemU6IDEycHg7CiAgICAgICAgZm9udC12YXJpYXRpb24tc2V0dGluZ3M6ICd3Z2h0JyA1MDA7CiAgICAgICAgZm9udC13ZWlnaHQ6IDUwMDsKICAgICAgfQoKICAgICAgLmNscy0zIHsKICAgICAgICBmaWxsOiAjYjFiMmIyOwogICAgICB9CgogICAgICAuY2xzLTQsIC5jbHMtNSB7CiAgICAgICAgZmlsbDogbm9uZTsKICAgICAgICBzdHJva2Utd2lkdGg6IDEuN3B4OwogICAgICB9CgogICAgICAuY2xzLTQsIC5jbHMtNSwgLmNscy02IHsKICAgICAgICBzdHJva2UtbGluZWNhcDogcm91bmQ7CiAgICAgICAgc3Ryb2tlLWxpbmVqb2luOiByb3VuZDsKICAgICAgfQoKICAgICAgLmNscy00LCAuY2xzLTYgewogICAgICAgIHN0cm9rZTogIzNjNTc3YTsKICAgICAgfQoKICAgICAgLmNscy01IHsKICAgICAgICBzdHJva2U6ICNiMWIyYjI7CiAgICAgIH0KCiAgICAgIC5jbHMtNiB7CiAgICAgICAgZmlsbDogI2ZmZjsKICAgICAgICBzdHJva2Utd2lkdGg6IDEuMjFweDsKICAgICAgfQogICAgPC9zdHlsZT4KICA8L2RlZnM+CiAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJNNzUuOTgsMzIuNzhWMTQuOThjMC0xLjE0LS45My0yLjA3LTIuMDctMi4wN2gtMTUuNjNjLTEuMTQsMC0yLjA3LjkzLTIuMDcsMi4wN3YzLjU5YzkuMDkuMjUsMTYuNzksNi4wOSwxOS43NywxNC4yMVoiLz4KICA8cmVjdCBjbGFzcz0iY2xzLTQiIHg9IjU2LjIiIHk9IjEyLjkxIiB3aWR0aD0iMTkuNzciIGhlaWdodD0iMjYuMTkiIHJ4PSIzLjU0IiByeT0iMy41NCIvPgogIDx0ZXh0IGNsYXNzPSJjbHMtMiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMzMuMDEgNjApIj48dHNwYW4geD0iMCIgeT0iMCI+UmVzdGF1cmFudHM8L3RzcGFuPjwvdGV4dD4KICA8cGF0aCBjbGFzcz0iY2xzLTUiIGQ9Ik02OS44Myw4LjQ2aDUuMjRjMi45MSwwLDUuMjcsMi4zNiw1LjI3LDUuMjd2NS41MiIvPgogIDxjaXJjbGUgY2xhc3M9ImNscy0zIiBjeD0iODAuMzQiIGN5PSIyMi42MiIgcj0iMS4wOSIvPgo8L3N2Zz4="
ICON_FAV_AKTIV       = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNy44NSAxNi40NiI+CiAgPGRlZnM+CiAgICA8c3R5bGU+CiAgICAgIC5jbHMtMSB7CiAgICAgICAgZmlsbDogI2I3ODcxNTsKICAgICAgICBzdHJva2U6ICNiNzg3MTU7CiAgICAgICAgc3Ryb2tlLWxpbmVjYXA6IHJvdW5kOwogICAgICAgIHN0cm9rZS1saW5lam9pbjogcm91bmQ7CiAgICAgIH0KICAgIDwvc3R5bGU+CiAgPC9kZWZzPgogIDxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTguOTIsMTUuOTZDNS40NCwxMy4xNy41LDguMy41LDQuNDQuNSwyLjIxLDIuNC41LDQuNzUuNWMyLjAzLDAsMy40NiwxLjA1LDQuMTcsMy42My43Mi0yLjU4LDIuMTItMy42Myw0LjE3LTMuNjMsMi4zNSwwLDQuMjUsMS43MSw0LjI1LDMuOTQsMCwzLjg2LTQuOTQsOC43My04LjQyLDExLjUyWiIvPgo8L3N2Zz4="
ICON_FAV_PASSIV      = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNy44NSAxNi40NiI+CiAgPGRlZnM+CiAgICA8c3R5bGU+CiAgICAgIC5jbHMtMSB7CiAgICAgICAgZmlsbDogbm9uZTsKICAgICAgICBzdHJva2U6ICM5YjkyOGI7CiAgICAgICAgc3Ryb2tlLWxpbmVjYXA6IHJvdW5kOwogICAgICAgIHN0cm9rZS1saW5lam9pbjogcm91bmQ7CiAgICAgIH0KICAgIDwvc3R5bGU+CiAgPC9kZWZzPgogIDxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTguOTIsMTUuOTZDNS40NCwxMy4xNy41LDguMy41LDQuNDQuNSwyLjIxLDIuNC41LDQuNzUuNWMyLjAzLDAsMy40NiwxLjA1LDQuMTcsMy42My43Mi0yLjU4LDIuMTItMy42Myw0LjE3LTMuNjMsMi4zNSwwLDQuMjUsMS43MSw0LjI1LDMuOTQsMCwzLjg2LTQuOTQsOC43My04LjQyLDExLjUyWiIvPgo8L3N2Zz4="
ICON_HAKEN           = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMC42MSAxNi4zOSI+CiAgPGRlZnM+CiAgICA8c3R5bGU+CiAgICAgIC5jbHMtMSB7CiAgICAgICAgZmlsbDogbm9uZTsKICAgICAgICBzdHJva2U6ICM5YjkyOGI7CiAgICAgICAgc3Ryb2tlLW1pdGVybGltaXQ6IDEwOwogICAgICB9CiAgICA8L3N0eWxlPgogIDwvZGVmcz4KICA8cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik03LjE2LDE1Ljg5aDBjLS42NSwwLTEuMjctLjI2LTEuNzMtLjcyTDEuMjIsMTAuOTVjLS45Ni0uOTUtLjk2LTIuNSwwLTMuNDYuOTYtLjk1LDIuNS0uOTUsMy40NiwwbDIuNDksMi40OUwxNS45MywxLjIyYy45Ni0uOTYsMi41LS45NiwzLjQ2LDAsLjk2Ljk1Ljk2LDIuNSwwLDMuNDZsLTEwLjUsMTAuNWMtLjQ2LjQ2LTEuMDguNzItMS43My43MloiLz4KPC9zdmc+"
ICON_CB_AKTIV        = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNS41NCAxNS41Ij4KICA8ZGVmcz4KICAgIDxzdHlsZT4KICAgICAgLmNscy0xIHsKICAgICAgICBmaWxsOiAjYjc4NzE1OwogICAgICB9CiAgICA8L3N0eWxlPgogIDwvZGVmcz4KICA8cGF0aCBkPSJNMTUuNTIsMi45NWwuMDIsOC45OGMwLC44Ni0uMzEsMS42NS0uOTIsMi4zNi0uNjEuNzEtMS4zMSwxLjEtMi4xMSwxLjE1aC0uNHMtLjMzLjA1LS4zMy4wNUgzLjc1Yy0xLjA3LS4wMS0xLjk3LS4zNC0yLjY4LS45OC0uNzEtLjY1LTEuMDctMS40Ni0xLjA3LTIuNDVWMy40M2MwLS44OS4zNC0xLjY4LDEuMDEtMi4zOEMxLjY5LjM1LDIuNDYsMCwzLjMyLDBoOC4yNGMuODMsMCwxLjQ4LjExLDEuOTQuMzIuNDMuMjEuODQuNTMsMS4yMi45Ni4zOC40My42MS44My42OCwxLjJsLjA1LjI3Yy4wNC4xMi4wNi4xOS4wNi4yMVpNMTEuNzMsMUgzLjYzYy0uNzUsMC0xLjM3LjIzLTEuODYuNy0uNDkuNDctLjc0LDEuMDYtLjc0LDEuNzh2OC40NnMtLjAxLjM0LS4wMS4zNGMwLC4yMy4xLjUxLjI5Ljg1LjE5LjM0LjQuNi42Mi43OC41LjM5LDEuMTEuNTksMS44My41OWw4LjA3LS4wNGguNTFzLjU5LS4xLjU5LS4xYy4zNy0uMTMuNzQtLjQxLDEuMDktLjg1LjM1LS40NC41My0uODIuNTMtMS4xNHYtLjMxbC0uMDctOS4wMWMwLS4xNy0uMDctLjM5LS4yLS42Ni0uMTMtLjI3LS4yOC0uNDgtLjQ0LS42Mi0uMzItLjMxLS42Mi0uNTItLjkxLS42Mi0uMjktLjExLS42OS0uMTYtMS4xOS0uMTZaIi8+CiAgPHBhdGggY2xhc3M9ImNscy0xIiBkPSJNNi4xNywxMi4zOWgwYy0uMzUsMC0uNjktLjE0LS45NC0uMzlsLTIuMjktMi4zYy0uNTItLjUyLS41Mi0xLjM2LDAtMS44OC41Mi0uNTIsMS4zNi0uNTIsMS44OCwwbDEuMzUsMS4zNSw0Ljc3LTQuNzdjLjUyLS41MiwxLjM2LS41MiwxLjg4LDAsLjUyLjUyLjUyLDEuMzYsMCwxLjg4bC01LjcxLDUuNzFjLS4yNS4yNS0uNTkuMzktLjk0LjM5WiIvPgo8L3N2Zz4="
ICON_CB_LEER         = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyBpZD0iRWJlbmVfMSIgZGF0YS1uYW1lPSJFYmVuZSAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNS41NCAxNS41Ij4KICA8cGF0aCBkPSJNMTUuNTIsMi45NWwuMDIsOC45OGMwLC44Ni0uMzEsMS42NS0uOTIsMi4zNi0uNjEuNzEtMS4zMSwxLjEtMi4xMSwxLjE1aC0uNHMtLjMzLjA1LS4zMy4wNUgzLjc1Yy0xLjA3LS4wMS0xLjk3LS4zNC0yLjY4LS45OC0uNzEtLjY1LTEuMDctMS40Ni0xLjA3LTIuNDVWMy40M2MwLS44OS4zNC0xLjY4LDEuMDEtMi4zOEMxLjY5LjM1LDIuNDYsMCwzLjMyLDBoOC4yNGMuODMsMCwxLjQ4LjExLDEuOTQuMzIuNDMuMjEuODQuNTMsMS4yMi45Ni4zOC40My42MS44My42OCwxLjJsLjA1LjI3Yy4wNC4xMi4wNi4xOS4wNi4yMVpNMTEuNzMsMUgzLjYzYy0uNzUsMC0xLjM3LjIzLTEuODYuNy0uNDkuNDctLjc0LDEuMDYtLjc0LDEuNzh2OC40NnMtLjAxLjM0LS4wMS4zNGMwLC4yMy4xLjUxLjI5Ljg1LjE5LjM0LjQuNi42Mi43OC41LjM5LDEuMTEuNTksMS44My41OWw4LjA3LS4wNGguNTFzLjU5LS4xLjU5LS4xYy4zNy0uMTMuNzQtLjQxLDEuMDktLjg1LjM1LS40NC41My0uODIuNTMtMS4xNHYtLjMxbC0uMDctOS4wMWMwLS4xNy0uMDctLjM5LS4yLS42Ni0uMTMtLjI3LS4yOC0uNDgtLjQ0LS42Mi0uMzItLjMxLS42Mi0uNTItLjkxLS42Mi0uMjktLjExLS42OS0uMTYtMS4xOS0uMTZaIi8+Cjwvc3ZnPg=="

def svg_img(b64: str, width: str = "100%") -> str:
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{width}" style="display:block"/>'

# ─────────────────────────────────────────────
# GLOBALES CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600;700&display=swap');

/* Basis */
html, body, [class*="css"] {
    font-family: 'Albert Sans', sans-serif !important;
    background-color: #ffffff;
    color: #1a1a1a;
}

/* Streamlit Grundelemente */
.stApp { background-color: #ffffff; }
.block-container { padding: 0 16px 100px 16px !important; max-width: 430px !important; }

/* Titel & Text */
h1 { font-family: 'Albert Sans', sans-serif !important; font-weight: 700 !important;
     font-size: 24px !important; color: #1a1a1a !important; margin-bottom: 4px !important; }
h2 { font-family: 'Albert Sans', sans-serif !important; font-weight: 600 !important;
     font-size: 18px !important; color: #1a1a1a !important; }
h3 { font-family: 'Albert Sans', sans-serif !important; font-weight: 500 !important;
     font-size: 16px !important; color: #1a1a1a !important; }
p, label, .stMarkdown { font-family: 'Albert Sans', sans-serif !important; }

/* Primär-Button */
.stButton > button[kind="primary"] {
    background-color: #b78715 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Albert Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 14px 24px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.88 !important; }
.stButton > button[kind="primary"]:disabled {
    background-color: #e0d5c0 !important;
    color: #a0906a !important;
}

/* Sekundär-Button */
.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: #3c577a !important;
    border: 1.5px solid #3c577a !important;
    border-radius: 12px !important;
    font-family: 'Albert Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    padding: 12px 20px !important;
    width: 100% !important;
}

/* Normaler Button (kein kind) */
.stButton > button:not([kind]) {
    background-color: transparent !important;
    color: #3c577a !important;
    border: none !important;
    font-family: 'Albert Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 8px 0 !important;
    text-align: left !important;
}

/* Inputs */
.stTextInput > div > div > input, .stTextArea textarea, .stNumberInput input {
    font-family: 'Albert Sans', sans-serif !important;
    border: 1.5px solid #e0e0e0 !important;
    border-radius: 10px !important;
    padding: 12px 14px !important;
    font-size: 15px !important;
    background: #f9f9f9 !important;
}
.stTextInput > div > div > input:focus, .stTextArea textarea:focus {
    border-color: #b78715 !important;
    box-shadow: 0 0 0 2px rgba(183,135,21,0.15) !important;
}

/* Multiselect */
.stMultiSelect > div > div {
    border: 1.5px solid #e0e0e0 !important;
    border-radius: 10px !important;
}

/* Checkbox */
.stCheckbox label { font-family: 'Albert Sans', sans-serif !important; font-size: 15px !important; }
.stCheckbox input[type="checkbox"]:checked { accent-color: #b78715 !important; }

/* Radio */
.stRadio label { font-family: 'Albert Sans', sans-serif !important; }
.stRadio input[type="radio"]:checked { accent-color: #b78715 !important; }

/* Info / Warning / Success */
.stAlert { border-radius: 12px !important; font-family: 'Albert Sans', sans-serif !important; }

/* Caption */
.stCaption { color: #9e9e9e !important; font-size: 13px !important; }

/* Divider */
hr { border: none !important; border-top: 1px solid #f0f0f0 !important; margin: 16px 0 !important; }

/* Tabs (Restaurant Karte/Liste/Lesezeichen) */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1.5px solid #f0f0f0 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Albert Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    color: #9e9e9e !important;
    border-bottom: 2px solid transparent !important;
    padding: 12px 20px !important;
    flex: 1 !important;
    justify-content: center !important;
}
.stTabs [aria-selected="true"] {
    color: #b78715 !important;
    border-bottom: 2px solid #b78715 !important;
    background: transparent !important;
}

/* Bottom Navigation */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 430px;
    background: #ffffff;
    border-top: 1px solid #f0f0f0;
    display: flex;
    z-index: 999;
    box-shadow: 0 -2px 12px rgba(0,0,0,0.06);
}
.nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 8px 0 10px;
    cursor: pointer;
    background: none;
    border: none;
    text-decoration: none;
}

/* Gericht-Card */
.gericht-card {
    background: #f9f9f9;
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 10px;
    border: 1px solid #f0f0f0;
}
.gericht-nr {
    font-family: 'Albert Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
    color: #9e9e9e;
    margin-bottom: 2px;
}
.gericht-name {
    font-family: 'Albert Sans', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: #1a1a1a;
}
.gericht-preis {
    font-family: 'Albert Sans', sans-serif;
    font-size: 14px;
    color: #b78715;
    font-weight: 500;
    margin-top: 4px;
}
.ampel-sicher { color: #2e7d32; font-size: 13px; font-weight: 500; }
.ampel-warnung { color: #c0392b; font-size: 13px; font-weight: 500; }

/* Profil-Zeile */
.profil-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 0;
    border-bottom: 1px solid #f5f5f5;
    cursor: pointer;
}
.profil-row-label {
    font-family: 'Albert Sans', sans-serif;
    font-size: 16px;
    font-weight: 500;
    color: #1a1a1a;
}
.profil-row-value {
    font-family: 'Albert Sans', sans-serif;
    font-size: 14px;
    color: #9e9e9e;
}

/* Upgrade Tabelle */
.upgrade-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Albert Sans', sans-serif;
    font-size: 15px;
    margin: 16px 0;
}
.upgrade-table th {
    text-align: left;
    padding: 10px 12px;
    font-weight: 600;
    color: #1a1a1a;
    border-bottom: 1.5px solid #f0f0f0;
}
.upgrade-table th.plan-col {
    text-align: center;
    width: 80px;
}
.upgrade-table th.plan-col.plus { color: #b78715; }
.upgrade-table td {
    padding: 12px 12px;
    border-bottom: 1px solid #f5f5f5;
    color: #1a1a1a;
}
.upgrade-table td.center { text-align: center; color: #9e9e9e; }
.upgrade-table td.center.ja { color: #b78715; }

/* Scan Limit Overlay */
.scan-limit-box {
    background: #fffbf0;
    border: 1.5px solid #b78715;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    margin: 24px 0;
}
.scan-limit-text {
    font-family: 'Albert Sans', sans-serif;
    font-size: 16px;
    color: #1a1a1a;
    line-height: 1.5;
    margin-bottom: 20px;
}

/* Disclaimer Box */
.disclaimer-box {
    background: #f9f9f9;
    border-radius: 14px;
    padding: 20px;
    margin: 20px 0;
    font-family: 'Albert Sans', sans-serif;
    font-size: 14px;
    line-height: 1.7;
    color: #444;
}

/* Logo / App Name */
.app-logo {
    font-family: 'Albert Sans', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #b78715;
    letter-spacing: -0.5px;
}

/* Zurück-Button */
.back-btn { color: #3c577a !important; font-size: 15px !important; }

/* Passwort Eye Icon Fix */
button[title="Show password text"] { color: #b78715 !important; }
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
defaults = {
    "page": "disclaimer",
    "user": None,
    "profile": None,
    "user_allergene": [],
    "disclaimer_accepted": False,
    "restaurant_logged_in": False,
    "restaurant_data": None,
    "active_tab": "scan",   # profil | scan | restaurants
}
for k, v in defaults.items():
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
        st.session_state.disclaimer_accepted = p.get("disclaimer_accepted", False)
        st.session_state.user_allergene = [k for k in ALLERGEN_LABELS if p.get(k, False)]

def save_allergene(selected):
    if not st.session_state.user:
        st.session_state.user_allergene = selected
        return
    upd = {k: (k in selected) for k in ALLERGEN_LABELS}
    supabase.table("user_profiles").update(upd).eq("id", st.session_state.user.id).execute()
    st.session_state.user_allergene = selected

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
        return st.session_state.get("local_scan_count", 0)
    res = supabase.table("scan_log").select("id", count="exact").eq("user_id", st.session_state.user.id).execute()
    return res.count or 0

def log_scan(scan_type):
    if not st.session_state.user:
        st.session_state["local_scan_count"] = st.session_state.get("local_scan_count", 0) + 1
        return
    supabase.table("scan_log").insert({"user_id": st.session_state.user.id, "scan_type": scan_type}).execute()

def is_premium():
    p = st.session_state.profile
    return p and p.get("plan") == "premium"

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
    p_icon = ICON_PROFIL_AKTIV if tab == "profil" else ICON_PROFIL_PASSIV
    s_icon = ICON_SCAN_AKTIV   if tab == "scan"   else ICON_SCAN_PASSIV
    r_icon = ICON_REST_AKTIV   if tab == "restaurants" else ICON_REST_PASSIV

    cols = st.columns(3)
    with cols[0]:
        if st.button(svg_img(p_icon, "60px"), key="nav_profil", help="Profil", use_container_width=True):
            st.session_state.active_tab = "profil"
            navigate("profil_uebersicht")
    with cols[1]:
        if st.button(svg_img(s_icon, "60px"), key="nav_scan", help="Scan", use_container_width=True):
            st.session_state.active_tab = "scan"
            navigate("scan")
    with cols[2]:
        if st.button(svg_img(r_icon, "60px"), key="nav_rest", help="Restaurants", use_container_width=True):
            st.session_state.active_tab = "restaurants"
            navigate("restaurants")

# ─────────────────────────────────────────────
# SEITE 1: DISCLAIMER
# ─────────────────────────────────────────────
def page_disclaimer():
    st.markdown('<div class="app-logo">🥜 Nuss-Checker</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Wichtiger Hinweis")
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
    is_onboarding = not st.session_state.disclaimer_accepted

    if not is_onboarding:
        if st.button("← Zurück"):
            navigate("profil_uebersicht")

    st.markdown("### Meine Allergene")
    st.markdown('<p style="color:#9e9e9e;font-size:14px;margin-bottom:16px">Welche Allergene soll die App für dich hervorheben?</p>', unsafe_allow_html=True)

    # Custom Checkbox Liste
    selected = []
    for key, label in ALLERGEN_LABELS.items():
        is_checked = key in st.session_state.user_allergene
        icon = ICON_CB_AKTIV if is_checked else ICON_CB_LEER
        col1, col2 = st.columns([1, 8])
        with col1:
            st.markdown(svg_img(icon, "22px"), unsafe_allow_html=True)
        with col2:
            cb = st.checkbox(f"**{key}** – {label}", value=is_checked, key=f"cb_{key}", label_visibility="visible")
        if cb:
            selected.append(key)

    st.markdown("---")
    btn_label = "Speichern und weiter →" if is_onboarding else "Speichern"

    def save_and_go():
        save_allergene(selected)
        navigate("scan")

    st.button(btn_label, on_click=save_and_go, type="primary")

# ─────────────────────────────────────────────
# SEITE 3: AUTH (Login / Registrieren)
# ─────────────────────────────────────────────
def page_auth():
    st.markdown('<div class="app-logo">🥜 Nuss-Checker</div>', unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2 = st.tabs(["Registrieren", "Einloggen"])

    with tab1:
        st.markdown("#### Neues Konto")
        reg_type = st.radio("", ["Ich bin Endkunde", "Ich registriere mich als Restaurant"], label_visibility="collapsed")
        email_r = st.text_input("E-Mail-Adresse", key="reg_email")
        pw_r = st.text_input("Passwort (mindestens 6 Zeichen)", type="password", key="reg_pw")
        pw_r2 = st.text_input("Passwort wiederholen", type="password", key="reg_pw2")

        is_restaurant = "Restaurant" in reg_type
        rest_name = rest_land = rest_plz = rest_adresse = rest_hnr = ""
        if is_restaurant:
            rest_name    = st.text_input("Restaurantname", key="rest_name")
            rest_land    = st.text_input("Land", key="rest_land")
            rest_plz     = st.text_input("Postleitzahl", key="rest_plz")
            rest_adresse = st.text_input("Adresse", key="rest_adresse")
            rest_hnr     = st.text_input("Hausnummer", key="rest_hnr")

        all_filled = email_r and pw_r and pw_r2
        if is_restaurant:
            all_filled = all_filled and rest_name and rest_land

        btn_label = "Registrieren" if is_restaurant else "Für 2,99 €/Monat registrieren"

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
                        "owner_id": res.user.id,
                        "name": rest_name,
                        "adresse": f"{rest_adresse} {rest_hnr}, {rest_plz} {rest_land}"
                    }).execute()
                navigate("disclaimer")
            except Exception as e:
                st.error(f"Registrierung fehlgeschlagen: {e}")

        st.button(btn_label, on_click=do_register, type="primary", disabled=not all_filled)
        st.caption("Nach der Registrierung bitte E-Mail bestätigen.")

    with tab2:
        st.markdown("#### Anmelden")
        email_l = st.text_input("E-Mail-Adresse", key="login_email")
        pw_l = st.text_input("Passwort", type="password", key="login_pw")
        st.markdown('<p style="color:#3c577a;font-size:13px;cursor:pointer">Passwort vergessen?</p>', unsafe_allow_html=True)

        def do_login():
            try:
                res = supabase.auth.sign_in_with_password({"email": email_l, "password": pw_l})
                st.session_state.user = res.user
                load_profile(res.user.id)
                if not st.session_state.disclaimer_accepted:
                    navigate("disclaimer")
                else:
                    navigate("scan")
            except Exception as e:
                st.error(f"Login fehlgeschlagen: {e}")

        st.button("Einloggen", on_click=do_login, type="primary")

# ─────────────────────────────────────────────
# SEITE 4: SCAN HAUPTBILDSCHIRM
# ─────────────────────────────────────────────
def page_scan():
    st.session_state.active_tab = "scan"
    scan_count = get_scan_count()

    if not is_premium() and scan_count >= FREEMIUM_SCAN_LIMIT:
        st.markdown(f"""
        <div class="scan-limit-box">
            <p class="scan-limit-text">
                Du hast heute schon<br>
                <strong>{FREEMIUM_SCAN_LIMIT}-mal geprüft.</strong><br>
                Unterstütze uns, um unbegrenzt zu scannen!
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Upgrade für 2,99 €/Monat", type="primary", on_click=lambda: navigate("upgrade"))
        bottom_nav()
        return

    st.markdown("### 📷 Scannen")
    if not is_premium():
        remaining = FREEMIUM_SCAN_LIMIT - scan_count
        st.caption(f"Noch {remaining} von {FREEMIUM_SCAN_LIMIT} heutigen Scans verfügbar")

    scan_mode = st.radio("Was möchtest du scannen?", [
        "🛒 Produktetikett (Supermarkt)",
        "🌍 Fremdsprachiges Etikett",
        "📋 Restaurant-Speisekarte (QR-Code)"
    ], label_visibility="collapsed")

    st.markdown("---")
    camera_image = st.camera_input("Kamera aktivieren")

    if camera_image:
        st.image(camera_image, use_column_width=True)
        st.markdown("---")

        if scan_mode == "🛒 Produktetikett (Supermarkt)":
            log_scan("produkt")
            st.markdown("#### Erkannte Allergene")
            st.info("⚙️ Texterkennung wird hier verarbeitet... *(OCR folgt in Phase 2)*")
            for a in st.session_state.user_allergene:
                st.markdown(f'<div class="ampel-warnung">⚠️ Enthält: {ALLERGEN_SHORT[a]}</div>', unsafe_allow_html=True)
            if st.session_state.user_allergene:
                st.markdown(" ")
                st.button("🔄 Sichere Alternativen anzeigen", type="primary", on_click=lambda: navigate("alternatives"))

        elif scan_mode == "🌍 Fremdsprachiges Etikett":
            log_scan("fremdsprache")
            st.markdown("#### Übersetzung & Allergene")
            st.info("⚙️ Sprache wird erkannt und übersetzt... *(Übersetzungs-API folgt in Phase 2)*")
            for a in st.session_state.user_allergene:
                st.markdown(f'<div class="ampel-warnung">⚠️ Enthält: {ALLERGEN_SHORT[a]}</div>', unsafe_allow_html=True)

        elif scan_mode == "📋 Restaurant-Speisekarte (QR-Code)":
            log_scan("qr_code")
            st.markdown("#### QR-Code erkannt")
            st.info("⚙️ QR-Code wird ausgelesen... *(QR-Decode folgt in Phase 2)*")
            st.button("🍽️ Gefilterte Speisekarte öffnen", type="primary",
                      on_click=lambda: navigate("restaurants"))

    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 5: RESTAURANTS (Karte / Liste / Lesezeichen)
# ─────────────────────────────────────────────
def page_restaurants():
    st.session_state.active_tab = "restaurants"
    st.markdown("### Restaurants")

    tab_karte, tab_liste, tab_lesezeichen = st.tabs(["Karte", "Liste", "Lesezeichen"])

    with tab_karte:
        st.info("⚙️ Kartenansicht folgt in Phase 2 (Google Maps / Mapbox)")
        st.markdown("Hier werden Restaurants in deiner Nähe angezeigt, die sichere Gerichte für dich haben.")

    with tab_liste:
        try:
            res = supabase.table("restaurants").select("id, name, adresse").eq("aktiv", True).execute()
            restaurants = res.data or []
        except:
            restaurants = []

        if not restaurants:
            st.markdown('<p style="color:#9e9e9e;font-size:15px">Noch keine Restaurants eingetragen.</p>', unsafe_allow_html=True)
        else:
            for r in restaurants:
                col1, col2 = st.columns([7, 1])
                with col1:
                    if st.button(f"**{r['name']}**\n{r.get('adresse','')}", key=f"rest_{r['id']}"):
                        st.session_state["selected_restaurant_id"] = r["id"]
                        st.session_state["selected_restaurant_name"] = r["name"]
                        navigate("speisekarte")
                with col2:
                    fav_icon = ICON_FAV_PASSIV
                    if is_premium():
                        if st.button(svg_img(fav_icon, "24px"), key=f"fav_{r['id']}", help="Lesezeichen"):
                            st.toast("Lesezeichen gespeichert ⭐")
                    else:
                        st.markdown(svg_img(ICON_FAV_PASSIV, "24px"), unsafe_allow_html=True)
                st.markdown('<hr style="margin:8px 0">', unsafe_allow_html=True)

    with tab_lesezeichen:
        if not is_premium():
            st.markdown("""
            <div class="disclaimer-box" style="text-align:center">
                <strong>Plus-Feature</strong><br>
                Lesezeichen sind im Plus-Tarif verfügbar.
            </div>
            """, unsafe_allow_html=True)
            st.button("Upgrade für 2,99 €/Monat", type="primary", on_click=lambda: navigate("upgrade"))
        else:
            st.info("Deine gespeicherten Restaurants erscheinen hier.")

    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 6: SPEISEKARTE
# ─────────────────────────────────────────────
def page_speisekarte():
    if st.button("← Zurück"):
        navigate("restaurants")

    rest_name = st.session_state.get("selected_restaurant_name", "Speisekarte")
    rest_id   = st.session_state.get("selected_restaurant_id")
    st.markdown(f"### {rest_name}")

    if st.session_state.user_allergene:
        tags = " · ".join([ALLERGEN_SHORT[a] for a in st.session_state.user_allergene])
        st.caption(f"Gefiltert nach: {tags}")
    else:
        st.caption("Alle Gerichte werden angezeigt (keine Allergene ausgewählt)")

    st.markdown("---")

    try:
        query = supabase.table("gerichte").select("*").eq("aktiv", True)
        if rest_id:
            query = query.eq("restaurant_id", rest_id)
        res = query.execute()
        gerichte = res.data or []
    except Exception as e:
        st.error(f"Fehler: {e}")
        gerichte = []

    if not gerichte:
        st.markdown('<p style="color:#9e9e9e">Noch keine Gerichte eingetragen.</p>', unsafe_allow_html=True)

    for g in gerichte:
        sicher, warnung = check_ampel(g, st.session_state.user_allergene)
        if st.session_state.user_allergene and not sicher:
            continue  # Nur sichere zeigen

        ampel_html = '<span class="ampel-sicher">✓ Laut Angaben verträglich</span>' if sicher else f'<span class="ampel-warnung">⚠️ Enthält {warnung}</span>'
        preis = f"{g.get('preis', '–')} €" if g.get("preis") else "–"

        st.markdown(f"""
        <div class="gericht-card">
            <div class="gericht-nr">Nr. {g.get('gericht_nummer','–')}</div>
            <div class="gericht-name">{g.get('name','')}</div>
            <div style="font-size:13px;color:#9e9e9e;margin:4px 0">{g.get('beschreibung','')}</div>
            <div class="gericht-preis">{preis}</div>
            <div style="margin-top:6px">{ampel_html}</div>
        </div>
        """, unsafe_allow_html=True)

    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 7: SICHERE ALTERNATIVEN
# ─────────────────────────────────────────────
def page_alternatives():
    if st.button("← Zurück"):
        navigate("scan")

    st.markdown("### ✅ Sichere Alternativen")
    if st.session_state.user_allergene:
        tags = " · ".join([ALLERGEN_SHORT[a] for a in st.session_state.user_allergene])
        st.caption(f"Gefiltert nach: {tags}")
    st.markdown("---")
    st.info("⚙️ Alternativen aus der Open Food Facts DB folgen in Phase 2.")

    import pandas as pd
    df = pd.DataFrame({
        "Produkt": ["Rote Linsen", "Kichererbsen", "Quinoa"],
        "Marke": ["Ja! Natürlich", "Spar Bio", "dm Bio"],
        "Allergene": ["Keine", "Keine", "Keine"],
        "Status": ["✅ Sicher", "✅ Sicher", "✅ Sicher"]
    })
    st.dataframe(df, use_container_width=True)
    st.caption("Platzhalterdaten · Quelle: Open Food Facts (folgt)")
    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 8: PROFIL ÜBERSICHT
# ─────────────────────────────────────────────
def page_profil_uebersicht():
    st.session_state.active_tab = "profil"
    st.markdown("### Profil")
    st.markdown("#### Konto")

    plan = "Plus" if is_premium() else "Gratistarif"

    # Abonnement
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown('<div class="profil-row-label">Abonnement</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="profil-row-value">{plan}</div>', unsafe_allow_html=True)
    if st.button("→", key="goto_upgrade"):
        navigate("upgrade")

    st.markdown('<hr style="margin:4px 0">', unsafe_allow_html=True)

    # Meine Allergene
    if st.button("Meine Allergene  →", key="goto_allergene"):
        navigate("allergen_settings")

    st.markdown('<hr style="margin:4px 0">', unsafe_allow_html=True)

    # Sprache
    if st.button("Sprache  →", key="goto_sprache"):
        st.toast("Mehrsprachigkeit folgt in Phase 2 ⚙️")

    st.markdown("---")

    # Restaurant Login Link
    st.caption("Du bist ein Restaurant?")
    if st.button("🏪 Restaurant-Login"):
        navigate("restaurant_admin")

    st.markdown("---")

    # Logout
    def do_logout():
        if st.session_state.user:
            supabase.auth.sign_out()
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    if st.session_state.user:
        st.button("🚪 Abmelden", on_click=do_logout)
    else:
        if st.button("🔑 Anmelden / Registrieren"):
            navigate("auth")

    bottom_nav()

# ─────────────────────────────────────────────
# SEITE 9: UPGRADE
# ─────────────────────────────────────────────
def page_upgrade():
    if st.button("← Zurück"):
        navigate("profil_uebersicht")

    st.markdown("### 🥜 Hol dir Nuss-Checker Plus")
    st.markdown('<p style="color:#9e9e9e;font-size:14px">Alle Funktionen, keine Limits.</p>', unsafe_allow_html=True)
    st.markdown("---")

    haken = svg_img(ICON_HAKEN, "18px")

    st.markdown(f"""
    <table class="upgrade-table">
        <thead>
            <tr>
                <th>Funktion</th>
                <th class="plan-col">Free</th>
                <th class="plan-col plus">Plus</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Tägliche Scans</td>
                <td class="center">3</td>
                <td class="center ja">∞</td>
            </tr>
            <tr>
                <td>Sichere Alternativen</td>
                <td class="center">–</td>
                <td class="center ja">{haken}</td>
            </tr>
            <tr>
                <td>Lesezeichen</td>
                <td class="center">–</td>
                <td class="center ja">{haken}</td>
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
    if st.button("← Zurück"):
        navigate("profil_uebersicht")

    st.markdown("### 🏪 Restaurant-Verwaltung")

    if not st.session_state.restaurant_logged_in:
        st.markdown("#### Login")
        email_r = st.text_input("E-Mail", key="rest_login_email")
        pw_r = st.text_input("Passwort", type="password", key="rest_login_pw")

        def do_rest_login():
            try:
                res = supabase.auth.sign_in_with_password({"email": email_r, "password": pw_r})
                user = res.user
                rr = supabase.table("restaurants").select("*").eq("owner_id", user.id).single().execute()
                if rr.data:
                    st.session_state.restaurant_logged_in = True
                    st.session_state.restaurant_data = rr.data
                    st.session_state.user = user
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
        st.markdown("#### Gericht hinzufügen")

        gericht_nr   = st.text_input("Gerichtnummer (z.B. 14 oder B2)")
        gericht_name = st.text_input("Name des Gerichts")
        beschreibung = st.text_area("Beschreibung")
        preis        = st.number_input("Preis (€)", min_value=0.0, step=0.5)

        st.markdown("**Enthaltene Allergene:**")
        cols = st.columns(4)
        allergen_sel = {}
        for i, (key, label) in enumerate(ALLERGEN_SHORT.items()):
            with cols[i % 4]:
                allergen_sel[key] = st.checkbox(f"{key} – {label}", key=f"adm_{key}")

        def save_gericht():
            try:
                supabase.table("gerichte").insert({
                    "restaurant_id": r["id"],
                    "gericht_nummer": gericht_nr,
                    "name": gericht_name,
                    "beschreibung": beschreibung,
                    "preis": preis,
                    **allergen_sel
                }).execute()
                st.success("✅ Gericht gespeichert!")
            except Exception as e:
                st.error(f"Fehler: {e}")

        st.button("💾 Gericht speichern", on_click=save_gericht, type="primary")
        st.markdown("---")

        def rest_logout():
            st.session_state.restaurant_logged_in = False
            st.session_state.restaurant_data = None
            navigate("profil_uebersicht")

        st.button("🚪 Ausloggen", on_click=rest_logout)

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
page = st.session_state.page

if page == "disclaimer":
    page_disclaimer()
elif page == "allergen_settings":
    page_allergen_settings()
elif page == "auth":
    page_auth()
elif page == "scan":
    page_scan()
elif page == "restaurants":
    page_restaurants()
elif page == "speisekarte":
    page_speisekarte()
elif page == "alternatives":
    page_alternatives()
elif page == "profil_uebersicht":
    page_profil_uebersicht()
elif page == "upgrade":
    page_upgrade()
elif page == "restaurant_admin":
    page_restaurant_admin()
else:
    # Fallback: nicht eingeloggte User → Scan (ohne Account nutzbar)
    if st.session_state.get("user"):
        navigate("scan")
    else:
        page_scan()
