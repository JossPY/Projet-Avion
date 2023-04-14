# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time

import adafruit_dht
import board

dht = adafruit_dht.DHT11(board.D5)
temp = []
hum = [10] 
val_temp = 0 
val_hum = 0
while True:
    for i in range (10):
        temperature = dht.temperature
        humidity = dht.humidity
        # Print what we got to the REPL
        print(i," ",temperature," " , humidity, " %")
        temp.append(temperature)
        hum.append(humidity)
        time.sleep(1)
    for i in range (10):
        val_temp = temp[i] + val_temp
        val_hum = hum[i] + val_hum
    val_temp = val_temp / 10
    val_hum = val_hum / 10
    print("Moyenne de temperature : ", val_temp , "Moyenne d'humidité : ", val_hum )