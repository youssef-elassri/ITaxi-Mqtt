from faker import Faker
import csv
import time

fake=Faker()

def init_taxis(x):
    taxi_data=[]
    for i in range(0,x):
        taxi={}
        taxi["id"] = "taxi-" + str(i)
        taxi['lon']=round((fake.random_int(min=5731,max=5900) / 10000) + 33, 5)
        taxi['lat']=round(((fake.random_int(min=5898,max=6000) / 10000) + 7) * -1, 5)
        taxi['alt']=round(((fake.random_int(min=5500,max=8400) / 10000) + 7) * -1, 5)
        taxi['Etat']= fake.random_element(elements=(0,1))
        taxi_data.append(taxi)
    return taxi_data

def send(x):
    return x["id"]+","+str(x["lon"])+","+str(x["lat"])+","+str(x["alt"])+","+str(x['Etat'])

def publish(x, mqttc, topic):
    for y in x:
        mqttc.publish(topic, send(y))
        print("published...", send(y))
        time.sleep(0.5)


def update_taxi_locations(taxis):
    for taxi in taxis:
        taxi['lon'] += round(fake.random_int(min=10, max=50) / 10000, 5) 
        taxi['lat']  += round(fake.random_int(min=10, max=50) / 10000, 5) 
        taxi['alt']  += round(fake.random_int(min=10, max=50) / 10000, 5) 
    return taxis

def init_clients(x):
    client_data=[]
    for i in range(0,x):
        client={}
        client["id"] = "client-" + str(i)
        client['Gender']= fake.random_element(elements=('Homme','Femme','Enfant'))
        client['lon']=round((fake.random_int(min=5731,max=5900) / 10000) + 33, 5)
        client['lat']=round(((fake.random_int(min=5898,max=6000) / 10000) + 7) * -1, 5)
        client['alt']=round(((fake.random_int(min=5500,max=8400) / 10000) + 7) * -1, 5)
        client['Etat']=fake.random_element(elements=(0,1))
        client_data.append(client)
    return client_data   

def update_client_locations(clients):
    for client in clients:
        client['lon'] += round(fake.random_int(min=10, max=20) / 10000, 5) 
        client['lat']  += round(fake.random_int(min=10, max=20) / 10000, 5) 
        client['alt']  += round(fake.random_int(min=10, max=20) / 10000, 5) 
    return clients


