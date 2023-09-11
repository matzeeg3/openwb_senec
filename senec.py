import struct
import json
import urllib.request
import time
import ssl
import paho.mqtt.client as mqtt

ipaddress = "senecip"
broker_address = "openwbip or localhost"
broker_port = 1883
debug = False

#ipaddress = str(sys.argv[1])

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
#filePath:              Pfad und Dateiname in der der ein Wert geschrieben wird
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

#EVU Daten
reqdata = '{"PM1OBJ1":{"FREQ":"","U_AC":"","I_AC":"","P_AC":"","P_TOTAL":""}}'
reqdata = bytes(reqdata, 'utf-8')
response = urllib.request.urlopen('https://' + ipaddress + '/lala.cgi', data=reqdata, context=ssl._create_unverified_context())
jsondata = json.load(response)



#SENEC: Gesamtleistung (W) Werte -3000  >> 3000
if not (jsondata['PM1OBJ1'] ['P_TOTAL'] is None):
    topic = "openWB/set/evu/W"
    client.publish(topic, writeVal(jsondata['PM1OBJ1'] ['P_TOTAL'],0,0))


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
reqdata='{"ENERGY":{"GUI_BAT_DATA_FUEL_CHARGE":"","GUI_BAT_DATA_POWER":"","GUI_BAT_DATA_VOLTAGE":"","GUI_BAT_DATA_OA_CHARGING":"","GUI_INVERTER_POWER":""}}'
reqdata = bytes(reqdata, 'utf-8')
response = urllib.request.urlopen('https://' + ipaddress + '/lala.cgi', data=reqdata, context=ssl._create_unverified_context())
jsondata = json.load(response)

#SENEC: Batterieleistung (W) Werte -345 (Entladen) >> 1200 (laden)
if not (jsondata['ENERGY'] ['GUI_BAT_DATA_POWER'] is None):
    topic = "openWB/set/houseBattery/W"
    client.publish(topic, writeVal(jsondata['ENERGY'] ['GUI_BAT_DATA_POWER'],0,0))

#SENEC: Fuellmenge in Prozent Werte 10 >> 55 >> 100
if not (jsondata['ENERGY'] ['GUI_BAT_DATA_FUEL_CHARGE'] is None):
    topic = "openWB/set/houseBattery/%Soc"
    client.publish(topic, writeVal(jsondata['ENERGY'] ['GUI_BAT_DATA_FUEL_CHARGE'],0,0))

#SENEC: Leistung Wechselrichter in (W) Werte
if not (jsondata['ENERGY'] ['GUI_INVERTER_POWER'] is None):
    topic = "openWB/set/pv/1/W"
    client.publish(topic, writeVal(jsondata['ENERGY'] ['GUI_INVERTER_POWER'],0,0))

#warten 1 Sekunden da der Client sonst zu schnell disconnectet
time.sleep (1)
# Client beenden
client.disconnect()

