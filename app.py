import streamlit as st

# Title and navigation buttons
st.title("Home Page")
st.write("Welcome! Choose an app to run:")

if st.button("Open Dashboard"):
    st.session_state.current_app = "dashboard"
    st.experimental_rerun()

if st.button("Open Asteroid Tracker"):
    st.session_state.current_app = "asteroid"
    st.experimental_rerun()

# Handle navigation
if 'current_app' in st.session_state:
    if st.session_state.current_app == "dashboard":
        exec(open("dashboard.py").read())  # Run `dashboard.py` code
    elif st.session_state.current_app == "asteroid":
        exec(open("asteroids.py").read())  # Run `asteroid.py` code
