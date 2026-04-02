import streamlit as st
import requests
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Gaming Lounge POS", layout="wide")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

st.title("🎮 Gaming Lounge Dashboard")

# =========================
# FETCH DATA
# =========================
def fetch_machines():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/machines", headers=HEADERS)
    return res.json()

def fetch_sessions():
    res = requests.get(f"{SUPABASE_URL}/rest/v1/sessions", headers=HEADERS)
    return res.json()

machines = fetch_machines()
sessions = fetch_sessions()

def get_active_session(machine_id):
    for s in sessions:
        if s["machine_id"] == machine_id and s["status"] == "active":
            return s
    return None

# =========================
# ACTIONS
# =========================
def start_session(machine_id):
    requests.post(
        f"{SUPABASE_URL}/rest/v1/sessions",
        headers=HEADERS,
        json={
            "machine_id": machine_id,
            "status": "active"
        }
    )

def end_session(session_id):
    requests.patch(
        f"{SUPABASE_URL}/rest/v1/sessions?id=eq.{session_id}",
        headers=HEADERS,
        json={
            "status": "completed",
            "end_time": datetime.now().isoformat()
        }
    )

# =========================
# UI GRID
# =========================
cols = st.columns(3)

for i, machine in enumerate(machines):
    with cols[i % 3]:
        st.subheader(machine["name"])
        st.caption(machine["type"])

        session = get_active_session(machine["id"])

        if session:
            start = datetime.fromisoformat(session["start_time"])
            mins = (datetime.now() - start).total_seconds() / 60

            st.success(f"🟢 Active: {round(mins,1)} mins")

            if st.button(f"End {machine['name']}", key=f"end_{machine['id']}"):
                end_session(session["id"])
                st.rerun()
        else:
            if st.button(f"Start {machine['name']}", key=f"start_{machine['id']}"):
                start_session(machine["id"])
                st.rerun()
