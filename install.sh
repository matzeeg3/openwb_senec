#!/bin/bash
echo "Erfassen der benötigten Daten:"
echo "Default Value in []"
read -p "IP Adresse des Senec Speichers eingeben: " -n 15 ipaddress
if [[ $ipaddress =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
  echo "test"
  # IP-Adresse ist gültig
else
  echo "Senec IP is not valid try again:"
  read -p "IP Adresse des Senec Speichers eingeben: " -n 15 ipaddress
fi
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
if [ $openwbv -eq 2 ]; then
  read -p "openWB Software 2 ENV ID [0]: " openwbenvid
  openwbenvid=${openwbenvid:-0}
  read -p "openWB Software 2 Battery ID [1]: " openwbbatid
  openwbbatid=${openwbbatid:-1}
  read -p "openWB Software 2 PV ID [2]: " openwbpvid
  openwbpvid=${openwbpvid:-2}
fi
echo ""
echo "Senec IP is: " $ipaddress
echo "Brocker IP is: " $broker_address
echo "EVU Data set to: " $evudata
echo "PV Data set to: " $pvdata
echo "WH Data set to: " $whcalc
echo "openWB Version is: " $openwbv
if [ $openwbv -eq 2 ]; then
echo "openWB Software 2 ENV ID is: " $openwbenvid
echo "openWB Software 2 Battery ID is: " $openwbbatid
echo "openWB Software 2 PV ID is: " $openwbpvid
fi


echo "script Ende"
# evudata = True  #True  oder False
# pvdata = True  #True oder False
# whcalc = True  #True oder False
# intervall = 5  #Intervall für WH Berechnung standard 5 Sec
# openwbv = "2"  #openwb version für mqtt topics
# openwbenvid = "0"  #nur openWB2 ID für ENV
# openwbpvid = "2"  #nur openWB2 ID für PV
# openwbbatid = "1"  #nur openWB2 ID für Batterie