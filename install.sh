#!/bin/bash

echo "Erfassen der benötigten Daten:"
echo "Default Value in []"
#read -p "IP Adresse des Senec Speichers eingeben: " -n 15 ipaddress
# if [[ ! $ipaddress =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
#   echo "Senec IP is not valid try again:"
#   goto start
# fi
while [[ ! $ipaddress =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; do
    read -p "IP Adresse des Senec Speichers eingeben: " -n 15 ipaddress
    done
#read -p "IP Adresse der openWB oder des MQTT Brokers eingeben: [127.0.0.1]" broker_address
while [[ ! $broker_address =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; do
    read -p "IP Adresse der openWB oder des MQTT Brokers eingeben: [127.0.0.1]" -n 15 broker_address
    broker_address=${broker_address:-127.0.0.1}
    done
while [[ $evudata != "True" && $evudata != "False" ]]; do
  read -p "Sollen EVU Daten erfasst werden?: (True/False)[True]" evudata
  evudata=${evudata:-True}
done
while [[ $pvdata != "True" && $pvdata != "False" ]]; do
  read -p "Sollen PV Daten erfasst werden?: (True/False) [True]" pvdata
  pvdata=${pvdata:-True}
done
while [[ $whcalc != "True" && $whcalc != "False" ]]; do
  read -p "Sollen WH Daten erfasst werden? (True/False) [True]" whcalc
  whcalc=${whcalc:-True}
done
while [[ $openwbv -ne 1 && $openwbv -ne 2 ]]; do
  read -p "openWB Version? (1/2) [1]: " openwbv
  openwbv=${openwbv:-1}
done
if [ $openwbv -eq 2 ]; then
  if [ $evudata = "True" ]; then
    read -p "openWB Software 2 ENV ID [0]: " openwbenvid
    openwbenvid=${openwbenvid:-0}
  fi
  read -p "openWB Software 2 Battery ID [1]: " openwbbatid
  openwbbatid=${openwbbatid:-1}
  if [ $pvdata = "True" ]; then
    read -p "openWB Software 2 PV ID [2]: " openwbpvid
    openwbpvid=${openwbpvid:-2}
  fi
fi
paho=$(python3 -m pip show paho-mqtt | grep Version)
if [[ $paho =~ "not found" ]]; then
  python3 -m pip install paho-mqtt
fi
echo $paho
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
