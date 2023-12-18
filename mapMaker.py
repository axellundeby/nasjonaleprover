import folium
import pandas as pd

# Load data from the CSV file
data = pd.read_csv("/Users/axellundeby/Desktop/hobbyprosjekter/skoleKart/skole/dataWithCords.csv", encoding='iso-8859-1')

# Replace non-numeric values in 'Engelsk', 'Matte', and 'Norsk' columns with 50
data['Engelsk'] = pd.to_numeric(data['Engelsk'], errors='coerce').fillna(50)
data['Matte'] = pd.to_numeric(data['Matte'], errors='coerce').fillna(50)
data['Norsk'] = pd.to_numeric(data['Norsk'], errors='coerce').fillna(50)

# Create a map centered based on average latitude and longitude
map = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=12)

# Function to adjust marker color
def color_based_on_score(english, math, norwegian):
    average_score = (english + math + norwegian) / 3
    if average_score > 50:
        return 'green'
    else:
        return 'red'

# Find the best school in each county
best_schools_per_county = data.groupby('Fylke').apply(lambda df: df.loc[df[['Engelsk', 'Matte', 'Norsk']].mean(axis=1).idxmax()])

# Add markers for each school
for index, row in data.iterrows():
    school_name = row['School Name']
    latitude = row['Latitude']
    longitude = row['Longitude']
    english_score = row['Engelsk']
    math_score = row['Matte']
    norwegian_score = row['Norsk']

    # Check if the school is the best in its county
    is_best_in_county = row['School Name'] == best_schools_per_county.loc[row['Fylke']]['School Name']

    # Marker color
    color = 'blue' if is_best_in_county else color_based_on_score(english_score, math_score, norwegian_score)

    # Popup text
    popup_text = f"School: {school_name}<br>English: {english_score}<br>Math: {math_score}<br>Norwegian: {norwegian_score}"

    # Add marker to the map
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(html=popup_text),
        icon=folium.Icon(color=color)
    ).add_to(map)

# Save the map
map.save("schools_with_scores_popup.html")

print("Map is saved as schools_with_scores_popup.html")
