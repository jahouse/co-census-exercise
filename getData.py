"""""
Filename: getData.py
Owner: Jada A. Houser
Description: pull data on vegetarian-friendly restaurants in Atlanta, GA from Yelp API,
             write data to json file, clean json data received from Yelp API, 
             write to csv file 
"""""

import requests
import json
import pandas as pd

"""""Retrieve Data"""""
# create header to store authorization credentials
my_header = {"Authorization": "Bearer 7u204lcHbjKWjmMFJuUfgmz0xpUQYI1uRTzKtnfb8mIYQnyWcRh_MUO6WZ_GSjI-n1ug7J0b9a6Lu2GnRI8Kca-HOoTAvZm-L5K65UrGKbOpNIi4TvOOZrDGRaOaYXYx"}
# create query dictionary to store API queries
query = {"term": "vegetarian restaurants", "location": "Atlanta", "price": "1, 2, 3, 4", "limit": "50"}
# GET call to Yelp API, returns query results
data = requests.get("https://api.yelp.com/v3/businesses/search", params=query, headers=my_header)

# get data into json format
jdata = data.json()

# write json data to json file
with open("data/veg_rest_j.json", "w") as f:
    json.dump(jdata, f)

"""""Clean Data"""""
# read json data and
with open("data/veg_rest_j.json", "r") as j:
    jdata_r = json.load(j)

# access nested json data and assign to pandas dataframe
jdata_df = pd.json_normalize(jdata_r["businesses"])
# drop unneeded columns
jdata_df = jdata_df.drop(columns=["alias","is_closed","review_count","categories","transactions","phone","distance","location.address3","location.display_address"])
# keep only where location.city is "Atlanta"
jdata_df = jdata_df.loc[jdata_df["location.city"] == "Atlanta"]
# convert longitude and latitude to floats from strings
jdata_df["coordinates.latitude"] = pd.to_numeric(jdata_df["coordinates.latitude"])
jdata_df["coordinates.longitude"] = pd.to_numeric(jdata_df["coordinates.longitude"])
# pass dataframe to csv
jdata_df.to_csv("data/veg_rest.csv", mode="w", index=False)
