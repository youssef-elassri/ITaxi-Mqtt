import json
import re
import socket
import traceback
from datetime import datetime
from time import sleep

from generator import init_clients, init_taxis, publish, send, update_client_locations, update_taxi_locations

import paho.mqtt.client as mqtt
from pynput import keyboard


def on_press(key):
    global break_program
    print(key)
    if key == keyboard.Key.esc:
        print('end pressed')
        break_program = True
        return False


def mapMsgToJson(lst):
    dic = {}
    dic['id'] = 'Me'
    dic['lon'] = lst[3].strip()
    dic['lat'] = lst[4].strip()
    dic['alt'] = lst[5].strip()
    dic['Etat'] = 0
    return send(dic)


def on_connect(client, userdata, rc):
    if rc != 0:
        pass
        print("Unable to connect to MQTT Broker...")
    else:
        print("Connected with MQTT Broker: " + str(MQTT_Broker))


def on_publish(client, userdata, rc):
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass


def publish_To_Topic(topic, message):
    mqttc.publish(topic, message)

syntax = {
  1:  ['gps', 'lat', 'lon', 'alt'],     # deg, deg, meters MSL WGS84
  3:  ['accel', 'x', 'y', 'z'],         # m/s/s
  4:  ['gyro', 'x', 'y', 'z'],          # rad/s
  5:  ['mag', 'x', 'y', 'z'],           # microTesla
  6:  ['gpscart', 'x', 'y', 'z'],       # (Cartesian XYZ) meters
  7:  ['gpsv', 'x', 'y', 'z'],          # m/s
  8:  ['gpstime', ''],                  # ms
  81: ['orientation', 'x', 'y', 'z'],   # degrees
  82: ['lin_acc',     'x', 'y', 'z'],
  83: ['gravity',     'x', 'y', 'z'],   # m/s/s
  84: ['rotation',    'x', 'y', 'z'],   # radians
  85: ['pressure',    ''],              # ???
  86: ['battemp', ''],                  # centigrade

# Not exactly sensors, but still useful data channels:
 -10: ['systime', ''],
 -11: ['from', 'IP', 'port'],
}


# MQTT Settings
MQTT_Broker = "523cf4e3dbf94d4897558b235ee9eb92.s1.eu.hivemq.cloud"
MQTT_Port = 8883
Keep_Alive_Interval = 30
MQTT_Topic_GPS = "Taxis/Location"
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish

mqttc.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
mqttc.username_pw_set("iot-5", "IOTteam-5")

mqttc.connect(MQTT_Broker, int(MQTT_Port))

break_program = False
host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

s.bind((socket.gethostname(), port))
print(s)

with keyboard.Listener(on_press=on_press) as listener:
    taxis = init_taxis(25)
    clients = init_clients(100)
    while break_program == False:
        try:
            message, (peerIP, peerport) = s.recvfrom(8192)
            lst = re.split("[,\'']", str(message))
            publish(taxis, mqttc=mqttc, topic= MQTT_Topic_GPS)
            publish(clients, mqttc=mqttc, topic= MQTT_Topic_GPS)
            if int(lst[2])==1:
                message_Json_Data = mapMsgToJson(lst)
                print(message_Json_Data)
                publish_To_Topic(MQTT_Topic_GPS, str(message_Json_Data))
                sleep(2)  # make a pause
            taxis = update_taxi_locations(taxis)
            clients = update_taxi_locations(clients)
        except:
            traceback.print_exc()
    listener.join()
print("salina")