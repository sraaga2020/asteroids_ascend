import streamlit as st

# Initialize session state for navigation
if 'current_app' not in st.session_state:
    st.session_state.current_app = "home"

# Define navigation logic
if st.session_state.current_app == "home":
    st.title("Home Page")
    st.write("Welcome! Choose an app to run:")

    if st.button("Open Dashboard"):
        st.session_state.current_app = "dashboard"

    if st.button("Open Asteroid Tracker"):
        st.session_state.current_app = "asteroid"

elif st.session_state.current_app == "dashboard":
    # Dashboard app logic
    st.title("Dashboard")
    st.write("This is the dashboard app.")

    if st.button("Back to Home"):
        st.session_state.current_app = "home"

elif st.session_state.current_app == "asteroid":
    # Asteroid Tracker app logic
    st.title("Asteroid Tracker")
    st.write("This is the asteroid tracking app.")

    if st.button("Back to Home"):
        st.session_state.current_app = "home"
