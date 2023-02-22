import numpy as np
import pandas as pd
import mongoengine as me
from models import Article_request
import datetime, time
import json
from collections import Counter
from geopy.geocoders import Nominatim
import requests

try:
    me.connect('fmk_assignment', host='localhost', port=27017)
except Exception as err:
    print(f'Error during connection to db {err}')


today = datetime.datetime.today().strftime ('%d-%m-%Y')

d = {}

import requests
import json
geolocator = Nominatim(user_agent="MyApp")
Latitude = None
Longitude = None
#Creates a dictionary { Country: Search frequency}
for a_req in Article_request.objects():
    city = a_req["city"]
    location = geolocator.geocode(city)
    Latitude = str(location.latitude)
    Longitude = str(location.longitude)
    location = geolocator.reverse(Latitude+","+Longitude)
    #print(location.raw["address"])
    city = location.raw["address"].get("country_code", '')
    r = requests.get('https://restcountries.com/v3.1/alpha/' + city)
    j = json.loads(r.text)
    city = j[0].get("name").get("common")

    dt = time.strftime('%d-%m-%Y', time.localtime(float(a_req["timestamp"])))
    if(dt == today):
        if city not in d.keys():
            d.update({city: [1]})
        else:
            n = d.get(city)
            print(n)
            n = n[0]+1
            d.update({city: [n]})
    
data = pd.DataFrame(d).T.reset_index()
data.columns=['country', 'count']

import plotly.express as px

database = px.data.gapminder().query('year == 2007')

df = pd.merge(database, data, how='inner', on='country')
url = (
    "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
)

fig = px.choropleth(df,
                    locations="country",#"iso_alpha",
                    locationmode="country names",#"ISO-3",
                    geojson = f"{url}/world-countries.json",
                    color="count"
                   )

fig.show()