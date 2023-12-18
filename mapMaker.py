import folium
import pandas as pd

# Load data from the updated CSV file

data = pd.read_csv("/Users/axellundeby/Desktop/hobbyprosjekter/skoleKart/skole/dataWithCords.csv", encoding='iso-8859-1')

# Replace non-numeric values in 'Engelsk', 'Matte', and 'Norsk' columns with 50
data['Engelsk'] = pd.to_numeric(data['Engelsk'], errors='coerce').fillna(50)
data['Matte'] = pd.to_numeric(data['Matte'], errors='coerce').fillna(50)
data['Norsk'] = pd.to_numeric(data['Norsk'], errors='coerce').fillna(50)

# Create a map centered based on average latitude and longitude
map = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=12)

# Define a function to adjust marker color based on the average score in the three subjects
def color_based_on_score(english, math, norwegian, best_school, worst_school):
    average_score = (english + math + norwegian) / 3
    if school_name == best_school:
        return 'darkgreen'
    elif school_name == worst_school:
        return 'darkred'
    elif average_score > 50:
        return 'green'
    else:
        return 'red'

# Find the best and worst school based on average score
best_school_index = (data['Engelsk'] + data['Matte'] + data['Norsk']).idxmax()
worst_school_index = (data['Engelsk'] + data['Matte'] + data['Norsk']).idxmin()
best_school = data.at[best_school_index, 'School Name']
worst_school = data.at[worst_school_index, 'School Name']

# Add markers for each school with a customized color and score popup
for index, row in data.iterrows():
    school_name = row['School Name']
    latitude = row['Latitude']
    longitude = row['Longitude']
    english_score = row['Engelsk']
    math_score = row['Matte']
    norwegian_score = row['Norsk']
    average_score = (english_score + math_score + norwegian_score) / 3

    popup_text = f"School: {school_name}<br>English: {english_score}<br>Math: {math_score}<br>Norwegian: {norwegian_score}<br>Average Score: {average_score}"

    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(html=popup_text),
        icon=folium.Icon(color=color_based_on_score(english_score, math_score, norwegian_score, best_school, worst_school))
    ).add_to(map)

# Save the map
map.save("schools_with_scores_popup.html")

print("Map is saved as schools_with_scores_popup.html")
