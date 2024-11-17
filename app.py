# In app.py
import streamlit as st
from dashboard import run_dashboard
from asteroids import run_asteroid_tracker

if 'current_app' not in st.session_state:
    st.session_state.current_app = "home"

if st.session_state.current_app == "home":
    st.title("Home Page")
    if st.button("Open Dashboard"):
        st.session_state.current_app = "dashboard"
    if st.button("Open Asteroid Tracker"):
        st.session_state.current_app = "asteroid"

elif st.session_state.current_app == "dashboard":
    run_dashboard()

elif st.session_state.current_app == "asteroid":
    run_asteroid_tracker()
