from geopy.geocoders import Nominatim
import pycountry
import pandas as pd
import folium

def get_coordinates(country):
    try:
        country_obj = pycountry.countries.get(name=country)
        geolocator = Nominatim(user_agent="sC")
        location = geolocator.geocode(country_obj.name)
        return location.latitude, location.longitude
    except AttributeError:
        return None, None

def make_map(df, country_column):
    df[['latitude', 'longitude']] = df[country_column].apply(get_coordinates).apply(pd.Series)
    m = folium.Map(tiles="OpenStreetMap", zoom_start=10)
    for i in range(0,len(df)):
        folium.Marker([df.iloc[i]['latitude'], df.iloc[i]['longitude']], popup=df.iloc[i][country_column]).add_to(m)
    return m

m.save("index.html")
print(df)