import streamlit as st
from dashboard import run_dashboard
from asteroids import run_asteroids

st.title("Home Page")
st.write("Welcome! Choose an app to run:")

if st.button("Asteroid Dashboard"):
    st.session_state.current_app = "dashboard"

if st.button("Alien Asteroid Mission"):
    st.session_state.current_app = "asteroids"

if st.session_state.current_app == "dashboard":
    run_dashboard()

elif st.session_state.current_app == "asteroids":
    run_asteroids()

    if st.button("Back to Home"):
        st.session_state.current_app = "home"
