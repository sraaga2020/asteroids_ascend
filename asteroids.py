import numpy as np 
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('Desktop/asteroids/nasa.csv')

label_encoder = LabelEncoder()
df.apply(LabelEncoder().fit_transform)

X = df[['Relative Velocity km per hr', 'Inclination', 'Eccentricity']]

y = df[['Miss Dist.(kilometers)']].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
dtree_missdist = DecisionTreeClassifier()
dtree_missdist.fit(X_train,y_train)

y = df[['Absolute Magnitude']].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
dtree_mag = DecisionTreeClassifier()
dtree_mag.fit(X_train,y_train)

relative_velocity = input("Relative Velocity: ")
inclination = input("Inclination: ")
eccentricity = input("Eccentricity: ")

X_user = [[relative_velocity, inclination, eccentricity]]
y_user = dtree_mag.predict(X_user)
y_user2 = dtree_missdist.predict(X_user)

print(y_user, y_user2)

if y_user <= 75000000:
    print("Potentially Hazardous Object (PHO)")
elif y_user <= 200000000 and y_user >= 75000000:
    print("Near-Earth Asteroid (NEA)")
elif y_user <= 10000:
    print("Critical")
