#!/bin/bash
echo "Erfassen der benötigten Daten:"
echo "Default Value in []"
read -p "IP Adresse des Senec Speichers eingeben: " ipaddress
read -p "IP Adresse der openWB oder des MQTT Brokers eingeben: [127.0.0.1]" broker_address
broker_address=${broker_address:-127.0.0.1}
read -p "Sollen EVU Daten erfasst werden?: (True/False)[True]" evudata
evudata=${evudata:-True}
read -p "Sollen PV Daten erfasst werden?: (True/False) [True]" pvdata
pvdata=${pvdata:-True}
read -p "Sollen WH Daten erfasst werden? (True/False) [True]" whcalc
whcalc=${whcalc:-True}
read -p "openWB Version? (1/2) [1]: " openwbv
openwbv=${openwbv:-1}
echo ""
echo "Senec IP is: " $ipaddress
echo "Brocker IP is: " $broker_address
echo "EVU Data set to: " $evudata
echo "PV Data set to: " $pvdata
echo "WH Data set to: " $whcalc
echo "openWB Version is: " $openwbv


echo "script Ende"
# evudata = True  #True  oder False
# pvdata = True  #True oder False
# whcalc = True  #True oder False
# intervall = 5  #Intervall für WH Berechnung standard 5 Sec
# openwbv = "2"  #openwb version für mqtt topics
# openwbenvid = "0"  #nur openWB2 ID für ENV
# openwbpvid = "2"  #nur openWB2 ID für PV
# openwbbatid = "1"  #nur openWB2 ID für Batterie