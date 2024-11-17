import numpy as np 
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import streamlit as st
import time

df = pd.read_csv('nasa.csv')
@st.cache
def train_models(df):

    label_encoder = LabelEncoder()
    df.apply(LabelEncoder().fit_transform)

    X = df[['Relative Velocity km per hr', 'Inclination', 'Eccentricity']]
    
    # miss distance (km) decision tree
    y = df[['Miss Dist.(kilometers)']].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    dtree_missdist = DecisionTreeClassifier()
    dtree_missdist.fit(X_train,y_train)

    # absolute magnitude (km) decision tree
    y = df[['Absolute Magnitude']].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    dtree_mag = DecisionTreeClassifier()
    dtree_mag.fit(X_train,y_train)

    return dtree_missdist, dtree_mag

dtree_missdist, dtree_mag = train_models(df)

if 'section' not in st.session_state:
    st.session_state.section = 'story'

# story
if st.session_state.section == 'story':
    st.title("Asteroid Attack")
    
    # Story Section 1
    st.write("""
    Welcome evil alien scientist! You are from the planet Zorkon-9, and your goal is to destroy Earth.
    Using your advanced alien technology, you can launch asteroids toward Earth by setting their
    relative velocity, inclination, and eccentricity. But beware—Earth's defenses are monitoring
    these parameters, and you must carefully aim to hit Earth and maximize destruction.
    """)

    # Story Section 2
    st.write("""
    Choose your asteroid's parameters carefully:
    - **Relative Velocity**: The speed at which the asteroid travels.
    - **Inclination**: The angle of the asteroid's trajectory relative to Earth's equatorial plane.
    - **Eccentricity**: How elongated the asteroid's orbit is.
    """)

    # Launch Prompt
    st.write("""
    Are you ready to unleash destruction on Earth? Press the button below to learn more about asteroid parameters!
    """)

  
    

    if st.button("Asteroids 101"):
        st.session_state.section = 'asteroids'
    
    
elif st.session_state.section == 'asteroids':
    st.title("Relative Velocity")
    st.markdown("""
- **Affects the trajectory of the asteroid and the time it takes to pass Earth.**
- **Higher relative velocity generally results in shorter interaction times, reducing gravitational deflection.**
-**Suggested range: 15 - 90 km/hr**
""")
    st.title("Eccentricity")
    st.markdown("""
- **Describes the shape of the orbit.**
- **e = 0 : Circular orbit**
- **0 < e < 1 : Elliptical orbit**
- **e = 1 : Parabolic orbit**
- **e > 1 : Hyperbolic escape trajectory**
    """)
    st.title("Inclination")
    st.markdown("""
- **The angle between the asteroid's orbital plane and Earth's orbital plane.**
- **Higher inclination generally means the asteroid is less likely to cross Earth's path, increasing miss distance.**
- **Suggested range: 0 - 20**
""")
    if st.button("Create Asteroid!"):
        st.session_state.section = 'inputs'
        
elif st.session_state.section == 'inputs':
    if st.button("Asteroids 101"):
        st.session_state.section = 'asteroids'
    # user inputs
    relative_velocity = st.number_input("Relative Velocity: ")
    inclination = st.number_input("Inclination: ")
    eccentricity = st.number_input("Eccentricity: ")

    st.button("Launch!")

    if relative_velocity != 0 and inclination != 0 and eccentricity != 0:
        # model predictions
        X_user = [[relative_velocity, inclination, eccentricity]]
        abs_mag = dtree_mag.predict(X_user)
        miss_dist = dtree_missdist.predict(X_user)

        st.write("Launching . . .")
        time.sleep(2)

        st.write("Your asteroid was this far from the Earth: ", str(miss_dist[0]), " km")
        st.write("Calculating destruction . . .")
        time.sleep(2)

        # classify asteroid risk
        if abs_mag > 0 and miss_dist < 1000000:
            st.write("You have accomplished your mission evil scientist! Your asteroid was on point and shattered the Earth into pieces! You are crowned emporer of the alien race!")
            st.image("https://dailygalaxy.com/wp-content/uploads/2024/09/Could-a-Nuclear-Explosion-Redirect-an-Asteroid-New-Research-Says-Yes.jpg")
        elif abs_mag > 1000000 and miss_dist < 3000000:
            st.write("Impressive evil scientist! Your asteroid has caused mass destruction throughout the North American continent! It is a blow the humans will never recover from!")
            st.image("https://idsb.tmgrup.com.tr/ly/uploads/images/2020/03/04/thumbs/800x531/23480.jpg?v=1583322397")
        elif 16 <= abs_mag > 3000000 and miss_dist < 6000000:
            st.write("Hmmf. Not too bad evil scientist. But, your asteroid has only scared the little humans and sailed through Earth's orbit. DO BETTER.")
            st.image("https://i0.wp.com/newspaceeconomy.ca/wp-content/uploads/2024/06/newspaceeconomy_picture_of_an_asteroid_striking_earth_cinematic_66f0fde4-b492-478a-8815-e063ac2ec0dd-1.png?fit=1024%2C1024&quality=80&ssl=1")
        elif abs_mag >= 6000000 and miss_dist < 15000000: 
            st.write("You have failed your mission evil scientist! The asteroid you launched has barely touched Earth's orbit.")
            st.image("https://files.oaiusercontent.com/file-RrTrnENQD64kAqJ9UDmRkYyK?se=2024-11-17T04%3A01%3A58Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D12760535-6149-4fd2-b4d1-83790538f5d3.webp&sig=VlqjYzVewlK6VUXkWoBlyMY19aeYPBSW5yHejHy9aoI%3D")
        elif abs_mag >= 15000000 or miss_dist >= 25000000:
            st.write("You have failed your mission evil scientist! The asteroid you launched has harmlessly sailed past Earth.")
            st.image("https://files.oaiusercontent.com/file-RrTrnENQD64kAqJ9UDmRkYyK?se=2024-11-17T04%3A01%3A58Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D12760535-6149-4fd2-b4d1-83790538f5d3.webp&sig=VlqjYzVewlK6VUXkWoBlyMY19aeYPBSW5yHejHy9aoI%3D")
        else:
            st.write("You have failed your mission evil scientist! The asteroid you launched has harmlessly sailed past Earth.")
            st.image("https://files.oaiusercontent.com/file-RrTrnENQD64kAqJ9UDmRkYyK?se=2024-11-17T04%3A01%3A58Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D12760535-6149-4fd2-b4d1-83790538f5d3.webp&sig=VlqjYzVewlK6VUXkWoBlyMY19aeYPBSW5yHejHy9aoI%3D")

import plotly.graph_objs as go
import streamlit as st
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
# Define NASA API key and endpoint
API_KEY = "rb2YlKiDL61HAOxF394nFFWbA8bDxSal10d1Cr8y"
API_ENDPOINT = "https://api.nasa.gov/neo/rest/v1/feed"

# Fetch Asteroid Data using NASA API
@st.cache_data
def fetch_asteroid_data(start_date, end_date):
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': API_KEY
    }
    response = requests.get(API_ENDPOINT, params=params)
    data = response.json()
    
    asteroids = []
    for date in data['near_earth_objects']:
        for asteroid in data['near_earth_objects'][date]:
            asteroids.append({
                'name': asteroid['name'],
                'diameter_m': asteroid['estimated_diameter']['meters']['estimated_diameter_max'],
                'speed_kmh': float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
                'distance_km': float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']),
                'orbiting_body': asteroid['close_approach_data'][0]['orbiting_body'],
                'hazardous': asteroid['is_potentially_hazardous_asteroid']
            })
    
    return pd.DataFrame(asteroids)

# Fetch data for the next 7 days (simulating real-time data)
start_date = datetime.now().strftime('%Y-%m-%d')
end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
asteroid_df = fetch_asteroid_data(start_date, end_date)

# Layout the Streamlit App
st.markdown(
    "<h1 style='text-align: center; color: #CFCFCF;'>Asteroid Impact Simulator 🚀</h1>",
    unsafe_allow_html=True
)

# Display Data Metrics
st.markdown("---")
st.subheader("Asteroid Metrics Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Asteroids", len(asteroid_df))
col2.metric("Average Diameter (m)", f"{asteroid_df['diameter_m'].mean():.2f}")
col3.metric("Average Speed (km/h)", f"{asteroid_df['speed_kmh'].mean():.2f}")

# Select an Asteroid for Detailed Analysis
st.subheader("Select an Asteroid for Detailed Analysis")
selected_asteroid = st.selectbox("Choose an Asteroid", asteroid_df['name'].unique())
selected_data = asteroid_df[asteroid_df['name'] == selected_asteroid]

# Display Selected Asteroid Details
st.markdown(f"### Asteroid Details: {selected_asteroid}")
st.write(f"Diameter: {selected_data['diameter_m'].values[0]} meters")
st.write(f"Speed: {selected_data['speed_kmh'].values[0]} km/h")
st.write(f"Distance from Earth: {selected_data['distance_km'].values[0]} km")
st.write(f"Orbiting Body: {selected_data['orbiting_body'].values[0]}")
st.write(f"Potentially Hazardous: {selected_data['hazardous'].values[0]}")

diameter = selected_data['diameter_m'].values[0]
speed = selected_data['speed_kmh'].values[0]  # Speed in km/h
distance = selected_data['distance_km'].values[0]  # Distance from Earth in km

# Let's assume that a larger diameter and speed leads to a bigger impact radius
impact_radius = np.log(diameter) * 10  # Scale impact radius by the diameter
impact_speed = np.log(speed) * 10  # Speed factor on impact

# Simulate the impact location based on distance and speed (for simplicity)
impact_location = [20 + np.random.uniform(-5, 5), 0 + np.random.uniform(-5, 5)]  # Random location on Earth map

# Create a Scatter Plot for the asteroid impact
trace = go.Scattergeo(
    lon=[impact_location[1]],
    lat=[impact_location[0]],
    text=[f"Impact! \nDiameter: {diameter} m\nSpeed: {speed} km/h\nImpact Radius: {impact_radius} km"],
    mode="markers+text",
    marker=dict(
        size=impact_radius,  # Impact radius
        color='red',
        opacity=0.7,
        line=dict(width=1, color='black')
    ),
    textposition="bottom center"
)

layout = go.Layout(
    geo=dict(
        scope='world',
        projection_type='equirectangular',
        showland=True,
        landcolor='white',
        subunitwidth=1,
        countrywidth=1,
        coastlinewidth=1,
        projection_scale=2.0
    ),
    title="Asteroid Impact Simulation",
    showlegend=False,
    geo_showcoastlines=True
)

fig = go.Figure(data=[trace], layout=layout)

# Display the impact animation in the app
st.plotly_chart(fig, use_container_width=True)

# Add a brief caption about the impact
st.markdown(
    """
    ### Impact Simulation
    Based on the asteroid's size, speed, and distance from Earth, the above simulation shows the impact location and potential damage.
    Larger asteroids with greater speeds will have more significant impacts and wider radii.
    """
)
