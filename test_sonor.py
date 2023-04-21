import board
import time
import adafruit_hcsr04
from rainbowio import colorwheel
import neopixel

rgb = neopixel.NeoPixel(board.NEOPIXEL,8 , auto_write=False)
# Création d'un objet pour le capteur de distance
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A5, echo_pin=board.A4)
import board
import time
import adafruit_hcsr04
from rainbowio import colorwheel
import neopixel

rgb = neopixel.NeoPixel(board.NEOPIXEL,8 , auto_write=False)
# Création d'un objet pour le capteur de distance
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A1, echo_pin=board.A0)

#dictionnaire des couleur by Arthur
dictColor = {
    'ROUGE' : (255, 0, 0),
    'JAUNE' : (255, 255, 0),
    'VERT' : (0, 255, 0)
    }

# Boucle infinie pour lire en continu la distance mesurée
while True:
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
#dictionnaire des couleur by Arthur
dictColor = {
    'ROUGE' : (255, 0, 0),
    'JAUNE' : (255, 255, 0),
    'VERT' : (0, 255, 0)
    }

# Boucle infinie pour lire en continu la distance mesurée
while True:
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