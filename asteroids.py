import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import streamlit as st
import time

# Load and preprocess data
df = pd.read_csv('nasa.csv')

@st.cache_data
def train_models(df):
    """Train the decision tree models."""
    label_encoder = LabelEncoder()
    df.apply(LabelEncoder().fit_transform)

    X = df[['Relative Velocity km per hr', 'Inclination', 'Eccentricity']]

    # Miss Distance Model
    y_miss = df[['Miss Dist.(kilometers)']].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y_miss, test_size=0.4, random_state=0)
    dtree_missdist = DecisionTreeClassifier()
    dtree_missdist.fit(X_train, y_train)

    # Absolute Magnitude Model
    y_mag = df[['Absolute Magnitude']].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y_mag, test_size=0.4, random_state=0)
    dtree_mag = DecisionTreeClassifier()
    dtree_mag.fit(X_train, y_train)

    return dtree_missdist, dtree_mag

# Train models
dtree_missdist, dtree_mag = train_models(df)

def run_asteroids():
    # Initialize session state for navigation
    '''if 'section' not in st.session_state:
        st.session_state = 'story'''

    # Page: Story
    st.session_state = 'story'
    if st.session_state == 'story':
        st.title("Asteroid Attack")
        st.write("""
        Welcome evil alien scientist! You are from the planet Zorkon-9, and your goal is to destroy Earth.
        Using your advanced alien technology, you can launch asteroids toward Earth by setting their
        relative velocity, inclination, and eccentricity. But beware—Earth's defenses are monitoring
        these parameters, and you must carefully aim to hit Earth and maximize destruction.
        """)

        st.write("""
        Choose your asteroid's parameters carefully:
        - **Relative Velocity**: The speed at which the asteroid travels.
        - **Inclination**: The angle of the asteroid's trajectory relative to Earth's equatorial plane.
        - **Eccentricity**: How elongated the asteroid's orbit is.
        """)

        
        st.session_state = 'asteroids'

    # Page: Asteroids Info
    if st.session_state == 'asteroids':
        st.title("Asteroid Parameters")
        st.markdown("""
        ### Relative Velocity
        - Affects the trajectory of the asteroid and the time it takes to pass Earth.
        - Higher relative velocity generally results in shorter interaction times, reducing gravitational deflection.
        """)
        st.markdown("""
        ### Eccentricity
        - Describes the shape of the orbit.
        - e = 0: Circular orbit
        - 0 < e < 1: Elliptical orbit
        - e = 1: Parabolic orbit
        - e > 1: Hyperbolic escape trajectory
        """)
        st.markdown("""
        ### Inclination
        - The angle between the asteroid's orbital plane and Earth's orbital plane.
        - Higher inclination generally means the asteroid is less likely to cross Earth's path, increasing miss distance.
        """)

        if st.button("Create Asteroid!"):
            st.session_state = 'inputs'

    # Page: Inputs and Launch
    
        st.title("Launch Your Asteroid")
        relative_velocity = st.number_input("Relative Velocity (km/hr): ", value=0.0, step=0.1)
        inclination = st.number_input("Inclination (degrees): ", value=0.0, step=0.1)
        eccentricity = st.number_input("Eccentricity (0 to 1): ", value=0.0, step=0.1)

        
        if relative_velocity > 0 and inclination > 0 and eccentricity > 0:
            X_user = [[relative_velocity, inclination, eccentricity]]
            abs_mag = dtree_mag.predict(X_user)[0]
            miss_dist = dtree_missdist.predict(X_user)[0]

            st.write("Launching . . .")
            time.sleep(2)

            st.write(f"Your asteroid was {miss_dist} km away from Earth.")
            st.write("Calculating destruction . . .")
            time.sleep(2)

            # Classify the asteroid impact
            if abs_mag > 0 and miss_dist < 1000000:
                st.write("Critical Hit! Earth is shattered!")
            elif abs_mag > 1000000 and miss_dist < 3000000:
                st.write("Severe Hit! Massive destruction!")
            elif abs_mag > 3000000 and miss_dist < 6000000:
                st.write("Moderate Hit! Earth survives, but damage is done.")
            else:
                st.write("Missed! The asteroid sailed harmlessly past Earth.")
    
  
