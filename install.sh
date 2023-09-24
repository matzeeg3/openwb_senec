#!/bin/bash
echo "Erfassen der benötigten Daten:"
read -p "IP Adresse des Senec Speichers eingeben: " ipaddress
read -p "IP Adresse der openWB oder des MQTT Brokers eingeben: " broker_address
echo -p "Sollen EVU Daten erfasst werden?: (True/False)" evudata
echo -p "Sollen PV Daten erfasst werden?: (True/False)" pvdata
echo -p "Sollen WH Daten erfasst werden?: (True/False)" whcalc

# evudata = True  #True  oder False
# pvdata = True  #True oder False
# whcalc = True  #True oder False
# intervall = 5  #Intervall für WH Berechnung standard 5 Sec
# openwbv = "2"  #openwb version für mqtt topics
# openwbenvid = "0"  #nur openWB2 ID für ENV
# openwbpvid = "2"  #nur openWB2 ID für PV
# openwbbatid = "1"  #nur openWB2 ID für Batterie