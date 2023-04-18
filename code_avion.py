# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_dht
from digitalio import DigitalInOut, Direction, Pull
import adafruit_hcsr04
import neopixel
import board

import pwmio
from adafruit_motor import motor

dht = adafruit_dht.DHT11(board.D5)

led1 = DigitalInOut(board.LED)
led1.direction = Direction.OUTPUT

rgb = neopixel.NeoPixel(board.NEOPIXEL,8 , auto_write=False)
# Création d'un objet pour le capteur de distance
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A5, echo_pin=board.A4)

#dictionnaire des couleur by Arthur
dictColor = {
    'ROUGE' : (255, 0, 0),
    'JAUNE' : (255, 255, 0),
    'VERT' : (0, 255, 0)
    }


while True:
    
    temperature = dht.temperature
    humidity = dht.humidity
    # Print what we got to the REPL
    print(temperature," " , humidity, " %")
        
    time.sleep(1)
    if temperature >=20 :
        led1.value = True
    else:
        led1.value = False
    """ if humidity >= 20:
        led2.value = True
    else:
        led2.value = False """
    
    try:
        distance = sonar.distance
        print("Distance en cm:", distance )
        if round(distance) > 15:
            rgb.fill(dictColor['VERT'])
            rgb.show()
        if round(distance) <= 15 and round(distance) >= 5:
            rgb.fill(dictColor['JAUNE'])
            rgb.show()
        if round(distance) < 5:
            rgb.fill(dictColor['ROUGE'])
            rgb.show()
        
    except RuntimeError:
        print("Erreur de mesure de distance")

    # Ajoutez un délai pour éviter de mesurer trop souvent
    time.sleep(1)
    
    # Pour voir si court-circuit : 0.009 amps
    # Pour faire fonctionner le moteur: 1.00 amps



    # init des broches A4 et A5 en tant que sortie
    motorA4 = pwmio.PWMOut(board.D9)
    motorA5 = pwmio.PWMOut(board.D11)

    # init du moteur sur les borche A4 et A5
    moteur = motor.DCMotor(motorA4, motorA5)

    while True:
        # 0% à 100% en 5 secondes
        timerStart = time.monotonic()
        while time.monotonic() - timerStart < 5:
            pourcentage = 100 * (time.monotonic() - timerStart) / 5
            moteur.throttle = pourcentage / 100
            

        # 100% à -100% en 10 secondes
        timerStart = time.monotonic()
        while time.monotonic() - timerStart < 10:
            pourcentage = 100 - 200 * (time.monotonic() - timerStart) / 10
            moteur.throttle = pourcentage / 100
            
        # -100% à 0% en 5 secondes
        timerStart = time.monotonic()
        while time.monotonic() - timerStart < 5:
            pourcentage = -100 * (time.monotonic() - timerStart) / 5
            moteur.throttle = pourcentage / 100
            print("fdp")
