import mysql.connector
import folium
from time import sleep
from folium import plugins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn=mysql.connector.connect(host= "localhost",
                       user ="root",
                        password ="",
                        database ="itaxi_db1"   
                       )
curs=conn.cursor()
data=dict()
data["id"]=[]
data["lat"]=[]
data["lon"]=[]
data["alt"]=[]
data["type"]=[]
data["etat"]=[]

m = folium.Map(width=900,height=500,location=[33.5731,-7.5898], zoom_start=12)


sql=" SELECT * FROM Locations "
curs.execute(sql)
rslts=curs.fetchall()
print('here 1')
for row in rslts:

        data["id"].append(row[0])
        data["lat"].append(float(row[1]))
        data["lon"].append(float(row[2]))
        data["alt"].append(row[3])
        data["etat"].append(int(row[4]))
        data["type"].append(row[5])
        
df=pd.DataFrame(data)

taxis_libre = df[df['type'] == 'Taxi'].query("etat == 0").to_dict('records')
taxis_occ = df[df['type'] == 'Taxi'].query("etat == 1").to_dict('records')
client_urg = df[df['type'] != 'Taxi'].query("etat == 1").to_dict('records')
client_noturg = df[df['type'] != 'Taxi'].query("etat == 0").to_dict('records')

for tax in taxis_occ:
        folium.Marker([tax['lat'], tax['lon']],
                    popup=tax['id'],
                    icon=folium.features.CustomIcon(r'C:\Users\Youssef\Desktop\IOT\IOTvisualisation\red.png', icon_size=(30,30))
                    ).add_to(m)
for tax in taxis_libre:
        folium.Marker([tax['lat'], tax['lon']],
                    popup=tax['id'],
                    icon=folium.features.CustomIcon(r'C:\Users\Youssef\Desktop\IOT\IOTvisualisation\yellow.png', icon_size=(30,30))
                    ).add_to(m)
for cl in client_urg:
        folium.Marker([cl['lat'], cl['lon']],
                    popup=cl['id'],
                    icon=folium.features.CustomIcon(r'C:\Users\Youssef\Desktop\IOT\IOTvisualisation\black.png', icon_size=(30,30))
                    ).add_to(m)
for cl in client_noturg:
        folium.Marker([cl['lat'], cl['lon']],
                    popup=cl['id'],
                    icon=folium.features.CustomIcon(r'C:\Users\Youssef\Desktop\IOT\IOTvisualisation\bleu.png', icon_size=(30,30))
                    ).add_to(m)

display(m)