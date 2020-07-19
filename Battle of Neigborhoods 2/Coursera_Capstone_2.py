#!/usr/bin/env python
# coding: utf-8

# # This Jupyter Notebook will be used for the Coursera Python for Data Analysis final. 

# # Import Libraries 

# In[3]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

get_ipython().system('pip install geopy')
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot  as plt

# import k-means from clustering stage
from sklearn.cluster import KMeans

#!conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab
import folium # map rendering library
import requests

print('Libraries imported.')


# In[4]:


#Geocode


# In[5]:


address='1535 Broadway, New York, NY 10036'
print('Done')


# In[6]:


address = '1535 Broadway, New York, NY'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# In[7]:


CLIENT_ID = 'UGVUZN2V5GGFR2X520DBTUD0KLD3AJ5PUSQPDT5L3LFHALMT'# your Foursquare ID
CLIENT_SECRET = 'UUPEWJ4UHDQFZENLEVDE0BNQPVVNKDPSZLJXSTP3Y4SYMWZK' # your Foursquare Secret
VERSION = '20200711'
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# In[8]:


#API


# In[9]:


search_query = 'resturants'
print(search_query + ' .... OK!')


# In[10]:


LIMIT = 900 # limit of number of venues returned by Foursquare API
radius = 10000 # define radius
# create URL
url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    latitude, 
    longitude, 
    VERSION, 
    search_query, 
    radius, 
    LIMIT)
url # display URL


# In[11]:


results = requests.get(url).json()


# In[12]:


items = results['response']['groups'][0]['items']
items[0]


# In[ ]:





# In[13]:


dataframe = pd.json_normalize(items) # flatten JSON

# filter columns
filtered_columns = ['venue.name', 'venue.categories'] + [col for col in dataframe.columns if col.startswith('venue.location.')] + ['venue.id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered['venue.categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean columns
dataframe_filtered.columns = [col.split('.')[-1] for col in dataframe_filtered.columns]

dataframe_filtered.head(10)


# # Data Cleaning

# In[14]:


dataframe_filtered.categories


# In[15]:


dataframe_filtered.groupby('categories').count()


# In[ ]:





# # Data Visualization

# In[16]:


plt.style.use('ggplot')

plt.figure(figsize=(9,5), dpi = 80)
# title
plt.title('Resturants in Midtown Manhattan')
#On x-axis
plt.xlabel('Types of Resturants', fontsize = 15)
#On y-axis
plt.ylabel('Number of Resturants', fontsize=15)
#giving a bar plot
dataframe_filtered.groupby('categories')['id'].count().plot(kind='bar')
#legend
plt.legend()
plt.show()


# # Map

# In[28]:


venues_map = folium.Map(location=[latitude, longitude], zoom_start=13) # generate map centred around the Conrad Hotel

for lat, lng, label in zip(dataframe_filtered.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(venues_map)
    


venues_map


# In[ ]:




