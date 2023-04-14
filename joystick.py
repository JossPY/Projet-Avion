#calcule --> tan = opp/ adj
#cadran 1 = 90 - tan
#cadran 2 = 90 + tan
#cadran 3 = 180 + tan
#cadran 4 = 270 + tan

#joystick repos == x --> 25500, y --> 25500(moitié de 51000 --> valeur tot du pot): joystick = value - 25500 (pour simplifier)

import board
import analogio
import math

# Init du joystick
joystickX = analogio.AnalogIn(board.A5)         #Max=52825
joystickY = analogio.AnalogIn(board.A4)         #Max=54116
joystickZ = analogio.AnalogIn(board.A3)

def calculeAngle(x, y):
    valX = (x - 26412.5) / 26412.5
    valY = (y - 27058) / 27058

    rangeX = range(31000, 33000)
    rangeY = range(30000, 32000)

    angle =  math.degrees(math.atan2(valY, valX))

    if valX>=0 and valY<=0:         #cadran 1
        angle+=90
    elif valX>=0 and valY>=0:         #cadran 2
        angle+=90
    elif valX<=0 and valY>=0:         #cadran 3
        angle+=90
    elif valX<=0 and valY<=0:         #cadran 4
        angle+=450

    #Si le joystick est au repos angle=0
    if(x in rangeX and y in rangeY):
        angle=0

    print("\nAngle="+str(round(angle)))

while True:
    calculeAngle(joystickX.value, joystickY.value)



""" import board
import analogio
import math
import time

# Configurer les broches pour le joystick


# Initialiser les objets AnalogIn pour lire les valeurs des broches
x_axis = analogio.AnalogIn(board.D9)
y_axis = analogio.AnalogIn(board.D6)

# Définir une fonction pour lire la valeur d'une broche et la convertir en une valeur entre -1.0 et 1.0
def read_axis(axis_x , axis_y):
    x = (axis_x - 26084.5 ) / 26084.5
    y = (axis_y - 26223.5) / 26223.5
    
    pos = math.degrees(math.atan2(y,x))

    if y > 50000 and x > 50000:
        pos += 90
    
    print(pos)
 
# Boucle principale pour lire les valeurs des broches et afficher les résultats
while True:
    read_axis(x_axis.value,y_axis.value)
    print(y_axis.value)
    time.sleep(0.5)
     """


    