# Senec to openWB or MQTT Broker Tool
##English
Reads Data from Senec (new Version with https) and sends the Data to openWB(via MQTT can be any Broker)  
Installation Steps:  
1. Install Python3 (sudo apt install python3, python3-pip -y)
2. Install Python3 Paho MQTT (pip install paho-mqtt)
3. create a folder (example: mkdir senec)
4. clone the git reposetory (git clone --branch main https://github.com/matzeeg3/openwb_senec.git)
5. edit the variable for broker and senecip to fits your needs and whcalc for statistic data also you can switch from openwb software 1 to openwb software 2
6. typ pwd to copy your path
7. change the path in this table and add it to your crontab via crontab -e
   ```
   * * * * * python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 5 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 10 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 15 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 20 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 25 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 30 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 35 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 40 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 45 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 50 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 55 && python3 /path-to-script/senec.py >/dev/null 2>&1
   ```
8. in openWB set Battery, ENV (if enabled), PV (if enabled) to MQTT.
9. Enjoy
##German
Liest Daten vom Senec (neue Version mit https) und sendet diese Daten an openWB Software 1 oder 2 oder an jeden anderen MQTT Broker  
Installations Schritte:  
1. Python3 Installieren (sudo apt install python3, python3-pip -y)
2. Installieren von Python3 Paho MQTT(pip install paho-mqtt)
3. Erstellen eines Ordners für das Script (example: mkdir senec)
4. Das Git Reposetory Clonen(git clone https://github.com/matzeeg3/openwb_senec.git)
5. Die Variablen am Anfang des Scriptes Editieren (BrokerIP, Senec IP, whcalc ob Wh berechnet werden sollen und die Option für openWB Software 1 oder openWB Software 2)
6. Den aktuellen Pfad auslesen: (pwd)
7. Ändern des Phades in der unten stehenden Tabelle und diese dann via crontab -e in die Crontab eintragen:
   ```
   * * * * * python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 5 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 10 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 15 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 20 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 25 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 30 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 35 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 40 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 45 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 50 && python3 /path-to-script/senec.py >/dev/null 2>&1
   * * * * * sleep 55 && python3 /path-to-script/senec.py >/dev/null 2>&1
   ```
8. in der openWB muss für ENV (wenn aktuv), PV (wenn aktiv) und Speicher noch auf MQTT umgestellt werden.
9. Spaß haben


## Next Steps
- Better Error Handling
- Script Optimisazion (Threading)
- Add Docker Container for easy deployment via Enviroment Variables
