import streamlit as st
from supabase import create_client
from datetime import datetime

# 🔑 Supabase Config
url = "https://ycfnyceqluruxyodknwf.supabase.co"
key = "YOUR_NEW_ANON_KEY"  # replace after regenerating
supabase = create_client(url, key)

st.set_page_config(page_title="Gaming Lounge POS", layout="wide")

st.title("🎮 Gaming Lounge Dashboard")

# ========================
# FETCH DATA
# ========================
machines = supabase.table("machines").select("*").execute().data
sessions = supabase.table("sessions").select("*").execute().data

def get_active_session(machine_id):
    for s in sessions:
        if s["machine_id"] == machine_id and s["status"] == "active":
            return s
    return None

# ========================
# UI GRID
# ========================
cols = st.columns(3)

for i, machine in enumerate(machines):
    with cols[i % 3]:
        st.subheader(machine["name"])
        st.caption(machine["type"])

        session = get_active_session(machine["id"])

        if session:
            start = datetime.fromisoformat(session["start_time"])
            mins = (datetime.now() - start).total_seconds() / 60

            st.success(f"Active: {round(mins,1)} mins")

            if st.button(f"End {machine['name']}"):
                supabase.table("sessions").update({
                    "status": "completed",
                    "end_time": datetime.now().isoformat()
                }).eq("id", session["id"]).execute()
                st.rerun()
        else:
            if st.button(f"Start {machine['name']}"):
                supabase.table("sessions").insert({
                    "machine_id": machine["id"],
                    "status": "active"
                }).execute()
                st.rerun()
