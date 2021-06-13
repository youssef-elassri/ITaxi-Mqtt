import paho.mqtt.client as mqtt

import mysql.connector


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

def save_to_database(msg):
    if msg.startswith('client') : type= "Client"
    elif msg.startswith('taxi') : type= "Taxi"
    else : type= "Me"
    msg = msg.split(",")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="itaxi_db1"
        )
    mycursor = mydb.cursor()
    print(msg)
    sql = "SELECT * FROM Locations WHERE id = '" +  msg[0]+ "'" 
    mycursor.execute(sql)
    rslts=mycursor.fetchall()
    if len(rslts) == 0:
        sql = "INSERT INTO Locations (id, lon, lat, alt, etat, type) VALUES (%s, %s,%s, %s,%s, %s)"
        val = (msg[0], float(msg[1]), float(msg[2]), float(msg[3]), int(msg[4]), type)
        mycursor.execute(sql, val)
        mydb.commit()
        print("record inserted.")
    else :
        sql = "UPDATE Locations SET lon = %s, lat = %s WHERE id = %s "
        val = (float(msg[1]), float(msg[2]), msg[0])
        mycursor.execute(sql, val)
        mydb.commit()
        print("record updated.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    save_to_database(msg.payload.decode("utf-8"))

# create the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set("iot-5", "IOTteam-5")

# connect to HiveMQ Cloud on port 8883
client.connect("523cf4e3dbf94d4897558b235ee9eb92.s1.eu.hivemq.cloud", 8883)
# subscribe to the topic "my/test/topic"
client.subscribe("Taxis/Location")
client.publish("Taxis/Location","client-7,0,33.6938,-7.6876999999999995,-7.663000000000001, 0")
# publish "Hello" to the topic "my/test/topic"
# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_forever()