import struct
import json
import urllib.request
import time
import ssl
import paho.mqtt.client as mqtt

ipaddress = "10.10.10.5"
broker_address = "127.0.0.1"
broker_port = 1883
debug = True #True  oder False
evudata = True #True  oder False
pvdata = True #True oder False
whcalc = False #True oder False
openwbv = "1"
intervall = 5

if debug == True: start_time = time.time()

client = mqtt.Client()
# Verbinden mit dem Broker
client.connect(broker_address, broker_port)

def myDecode(stringValue):
# Parameter:
# stringValue:  String Wert, im Format Typ_Wert
#
# Rueckgabe:
# result:               Floatzahl
    splitValue = stringValue.split('_')

    if splitValue[0] == 'fl':
        #Hex >> Float
        result = struct.unpack('f',struct.pack('I',int('0x'+splitValue[1],0)))[0]
    elif splitValue[0] == 'u3':
        pass #TBD
    elif splitValue[0] == 'u8':
        pass #TBD

    return result

def writeVal(stringValue, multiplier, decimalpoints):

#Parameter
#stringValue:   Wert der nach dem knonvertieren in die Datei geschrieben wird
#multiplier:    Wert mit dem die Zahl vor der Rundung multipliziert wird
#decimalpoints: Anzahl Kommastellen
#
#Rueckgabe: nichts


    val= myDecode(stringValue)

        # Format anpassen
    if multiplier != 0:
        val = val * multiplier

    #auf 2 Ziffern runden
    if decimalpoints == 0:
        val = int(val)
    elif decimalpoints != 0:
        val = round(val,decimalpoints)

    if val is None:
        val = 0

    return val
  
subreturn=0
def on_message(client, userdata, message):
    global subreturn
    if debug == True: print("message topic " ,str(message.topic)," message received " ,str(message.payload.decode("utf-8")))
    subreturn = (message.payload.decode("utf-8"))


client.on_message=on_message

reqdata = '{"PM1OBJ1": {"FREQ":"","U_AC":"","I_AC":"","P_AC":"","P_TOTAL":""},"ENERGY": {"GUI_BAT_DATA_FUEL_CHARGE":"","GUI_BAT_DATA_POWER":"","GUI_INVERTER_POWER":""}}'
reqdata = bytes(reqdata, 'utf-8')
response = urllib.request.urlopen('https://' + ipaddress + '/lala.cgi', data=reqdata, context=ssl._create_unverified_context())
jsondata = json.load(response)

if whcalc == True:
  client.loop_start()
  client.subscribe("data/gridwhout", qos=0)
  time.sleep(0.15)
  gridwhoutstore=float(subreturn)
  client.subscribe("data/gridwhin", qos=0)
  time.sleep(0.15)
  gridwhinstore=float(subreturn)
  client.subscribe("data/batwhout", qos=0)
  time.sleep(0.15)
  batwhoutstore=float(subreturn)
  client.subscribe("data/batwhin", qos=0)
  time.sleep(0.15)
  batwhintstore=float(subreturn)
  client.subscribe("data/pvwh", qos=0)
  time.sleep(0.15)
  pvwhstore=float(subreturn)
  client.loop_stop()
  if debug == True:print("gridwhoutstore: ", gridwhoutstore)
  if debug == True:print("gridwhinstore: ", gridwhinstore)
  if debug == True:print("batwhoutstore: ", batwhoutstore)
  if debug == True:print("batwhintstore: ", batwhintstore)
  if debug == True:print("pvwhstore: ", pvwhstore)

if evudata == True:
  #EVU Daten
    
  #SENEC: Gesamtleistung (W) Werte -3000  >> 3000
  if not (jsondata['PM1OBJ1'] ['P_TOTAL'] is None):
      topic = "openWB/set/evu/W"
      gridwatt = writeVal(jsondata['PM1OBJ1'] ['P_TOTAL'],0,0)
      client.publish(topic, gridwatt, qos=0)
      if whcalc == True:
        if gridwatt < 0:
          gridwatt = abs(gridwatt)
          gridwhout = gridwatt * intervall / 3600
          if debug == True: print("gridwhout: ", gridwhout)
          ggridwhout = gridwhout + gridwhoutstore
          client.publish("data/gridwhout", ggridwhout, retain=True)  
          client.publish("openWB/set/evu/WhExported", ggridwhout, qos=0)
        else:
          gridwatt = abs(gridwatt)
          gridwhin = gridwatt * intervall / 3600
          if debug == True: print("gridwhin: ", gridwhin)
          ggridwhin = gridwhin + gridwhinstore
          client.publish("data/gridwhin", ggridwhin, retain=True)
        client.publish("openWB/set/evu/WhImported", ggridwhin, qos=0)
  
  
  #SENEC: Frequenz(Hz) Werte 49.00 >> 50.00
  if not (jsondata['PM1OBJ1'] ['FREQ'] is None):
      topic = "openWB/set/evu/HzFrequenz"
      client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['FREQ'],0,2))
  
  #SENEC: Spannung (V) Werte 219.12 >> 223.43
  if not (jsondata['PM1OBJ1'] ['U_AC'] [0] is None):
      topic = "openWB/set/evu/VPhase1"
      client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['U_AC'] [0],0,2))
  if not (jsondata['PM1OBJ1'] ['U_AC'] [1] is None):
      topic = "openWB/set/evu/VPhase2"
      client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['U_AC'] [1],0,2))
  if not (jsondata['PM1OBJ1'] ['U_AC'] [2] is None):
      topic = "openWB/set/evu/VPhase3"
      client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['U_AC'] [2],0,2))
  
  #SENEC: Leistung (W) Werte -2345 >> 3000
  if not (jsondata['PM1OBJ1'] ['P_AC'] [0] is None):
      topic = "openWB/set/evu/WPhase1"
      client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['P_AC'] [0],0,0))
  if not (jsondata['PM1OBJ1'] ['P_AC'] [1] is None):
      topic = "openWB/set/evu/WPhase2"
      client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['P_AC'] [1],0,0))
  if not (jsondata['PM1OBJ1'] ['P_AC'] [2] is None):
      topic = "openWB/set/evu/WPhase3"
      client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['P_AC'] [2],0,0))
  
  
  #SENEC: Strom (A) Werte 0.88 >> 1.67
  if not (jsondata['PM1OBJ1'] ['I_AC'] [0] is None):
      topic = "openWB/set/evu/APhase1"
      client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['I_AC'] [0],0,2))
  if not (jsondata['PM1OBJ1'] ['I_AC'] [1] is None):
      topic = "openWB/set/evu/APhase2"
      client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['I_AC'] [1],0,2))
  if not (jsondata['PM1OBJ1'] ['I_AC'] [2] is None):
      topic = "openWB/set/evu/APhase3"
      client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['I_AC'] [2],0,2))

#Batteriedaten:

#SENEC: Batterieleistung (W) Werte -345 (Entladen) >> 1200 (laden)
if not (jsondata['ENERGY'] ['GUI_BAT_DATA_POWER'] is None):
    topic = "openWB/set/houseBattery/W"
    batwatt = writeVal(jsondata['ENERGY'] ['GUI_BAT_DATA_POWER'],0,0)
    client.publish(topic, batwatt, qos=0)
    if whcalc == True:
      if batwatt < 0:
        batwatt = abs(batwatt)
        batwhout = batwatt * intervall / 3600
        if debug == True: print("batwhout: ", batwhout)
        gbatwhout = batwhout + batwhoutstore
        client.publish("data/batwhout", gbatwhout, retain=True)
        client.publish("openWB/set/houseBattery/WhExported", gbatwhout, qos=0) 
      else:
        batwatt = abs(batwatt)
        batwhin = batwatt * intervall / 3600
        if debug == True: print("batwhin: ", batwhintstore)
        gbatwhin = batwhin + batwhintstore
        client.publish("data/batwhin", gbatwhin, retain=True)
        client.publish("openWB/set/houseBattery/WhImported", gbatwhin, qos=0)  

#SENEC: Fuellmenge in Prozent Werte 10 >> 55 >> 100
if not (jsondata['ENERGY'] ['GUI_BAT_DATA_FUEL_CHARGE'] is None):
    topic = "openWB/set/houseBattery/%Soc"
    client.publish(topic, writeVal(jsondata['ENERGY'] ['GUI_BAT_DATA_FUEL_CHARGE'],0,0))



## PV Daten
if pvdata == True:
  #SENEC: Leistung Wechselrichter in (W) Werte
  if not (jsondata['ENERGY'] ['GUI_INVERTER_POWER'] is None):
      topic = "openWB/set/pv/1/W"
      client.publish(topic, writeVal(jsondata['ENERGY'] ['GUI_INVERTER_POWER'],0,0))
      if whcalc == True:
        pvwatt = writeVal(jsondata['ENERGY'] ['GUI_INVERTER_POWER'],0,0)
        pvwh = pvwatt * intervall / 3600
        if debug == True: print("pvwh: ", pvwh)
        gpvwh = pvwh + pvwhstore
        client.publish("data/pvwh", gpvwh, retain=True)
        client.publish("openWB/set/pv/1/WhCounter", gpvwh, qos=0)




#warten 1 Sekunden da der Client sonst zu schnell disconnectet
time.sleep (0.2)
# Client beenden
client.disconnect()
if debug == True: end_time = time.time()
# Die Gesamtdauer in Sekunden berechnen
if debug == True: execution_time = end_time - start_time

# Die Ausführungszeit in Sekunden ausgeben
if debug == True: print(f"Das Skript wurde in {execution_time:.2f} Sekunden ausgeführt.")
