# Senec to openWB or MQTT Broker Tool
Reads Data from Senec (new Version with https) and sends the Data to openWB(via MQTT can be any Broker)  
Installation Steps:  
1. Install Python3 (sudo apt install python3, python3-pip -y)
2. Install Python3 Paho MQTT (pip install paho-mqtt
3. create a folder (example: mkdir senec)
4. clone the git reposetory (git clone --branch main https://github.com/matzeeg3/openwb_senec.git)
5. edit the variable for broker and senecip to fits your needs and whcalc for statistic data also you can switch from openwb software 1 to openwb software 2
6. typ pwd to copy your path
7. change the path in this table and add it to your crontab via crontab -e
   ```
   * * * * * python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 5 && python /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 10 && python /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 15 && python /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 20 && python /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 25 && python /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 30 && python /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 35 && python /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 40 && python /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 45 && python /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 50 && python /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 55 && python /path-to-script/senec.py >/dev/null 2>&1
   ```
8. in openWB set Battery, ENV (if enabled), PV (if enabled) to MQTT.

9. Enjoy


## Next Steps
- Better Error Handling
- Script Optimisazion (Threading)
- Add Docker Container for easy deployment via Enviroment Variables
