# pip install gtfs-realtime-bindings pandas requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
from requests import get
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
 
# Sample GTFS-R URL from Malaysia's Open API
URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/ktmb'
 
# Parse the GTFS Realtime feed
feed = gtfs_realtime_pb2.FeedMessage()
response = get(URL)
feed.ParseFromString(response.content)
 
# Extract and print vehicle position information
vehicle_positions = [MessageToDict(entity.vehicle) for entity in feed.entity]
print(f'Total vehicles: {len(vehicle_positions)}')
df = pd.json_normalize(vehicle_positions)
#print(df)

df_geo = gpd.GeoDataFrame(df, geometry= gpd.points_from_xy(df['position.longitude'], df['position.latitude']))
print(df_geo)

#get built in dataset
world_data = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#plot malayisa map

axis = world_data[world_data.name == 'Malaysia'].plot(color = 'lightblue', edgecolor = 'black')

df_geo.plot(ax = axis, color = 'black')
plt.show()
