
"""
Example of reading from a card using the ``mfrc522`` module.
"""

# 3rd party
import board

# this package
import mfrc522
import analogio
import math
import pwmio
from adafruit_motor import servo ,motor
import adafruit_dht
import time
import adafruit_hcsr04
from digitalio import DigitalInOut, Direction, Pull
import neopixel
from adafruit_tca8418 import TCA8418
from adafruit_display_text import bitmap_label
import terminalio

#####################################
#				RFID				#
#####################################

lecteur = mfrc522.MFRC522(board.D12, board.D11, board.D13, board.D9, board.D10)
lecteur.set_antenna_gain(0x07 << 4)

#####################################
#			joystick				#
#####################################

AxeX = analogio.AnalogIn(board.A3)         #Max=52825
AxeY = analogio.AnalogIn(board.A5)         #Max=54116
AxeZ = analogio.AnalogIn(board.A4)

#####################################
#			Moteur et servo			#
#####################################
pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

pin2 = board.D5
pin7 = board.D6

pwm1 = pwmio.PWMOut(pin2, frequency=5000, duty_cycle=0)
pwm2 = pwmio.PWMOut(pin7, frequency=5000, duty_cycle=0)

motor1 = motor.DCMotor(pwm1, pwm2)
motor1.throttle = 0

def defAngle(pot_value): 
        rangeValue = range(31000, 35000)
        #print(pot_value)
        if pot_value in rangeValue:
            return 90
        else:
            pot_value = (pot_value / 52447) * 180
            return pot_value

#####################################
#			NEOPIXEL				#
#####################################

rgb = neopixel.NeoPixel(board.NEOPIXEL,8 , auto_write=False)
couleurs = {'rouge':(255, 0, 0), 'jaune':(255, 150, 0), 'vert':(0, 255, 0)}

#####################################
#			aeroport				#
#####################################

aeroports = {
    101: 'YUL Montreal',
    111: 'ATL Atlanta',
    222: 'HND Tokyo',
    764: 'LHR London',
    492: 'CAN Baiyun',
    174: 'CDG Paris',
    523: 'AMS Amsterdam'
}
#####################################
#				KEYMAP				#
#####################################

# set up all R0-R2 pins and C0-C3 pins as keypads
KEYPADPINS = (
    TCA8418.R0,
    TCA8418.R1,
    TCA8418.R2,
    TCA8418.R3,
    TCA8418.C0,
    TCA8418.C1,
    TCA8418.C2,
    TCA8418.C3,

)
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
tca = TCA8418(i2c)
tca.key_intenable = True
keymap = (("*", "0", "#","D"), 
          ("7", "8", "9","C"), 
          ("4", "5", "6","B"), 
          ("1", "2", "3","A"))

for pin in KEYPADPINS:
    tca.keypad_mode[pin] = True
    # make sure the key pins generate FIFO events
    tca.enable_int[pin] = True
    # we will stick events into the FIFO queue
    tca.event_mode_fifo[pin] = True

#####################################
#				sonar				#
#####################################

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.TX, echo_pin=board.A0)

#####################################
#			Button Switch			#
#####################################

btn = tca.get_pin(TCA8418.C8)
btn.switch_to_input(pull=Pull.UP)


#####################################
#				DHT11				#
#####################################

dht = adafruit_dht.DHT11(board.A1)
temp = []
hum = [10] 
val_temp = 0 
val_hum = 0 

#####################################
#	Initialisation de variable		#
#####################################

scale = 1
badgeValide = False

debutTemps= time.monotonic()
destination = " "
tempAeroport = ""
temp_str =""
tempAeroport= ""
Number=""
aeroport = []
garderCap = False

rgb.fill(couleurs['rouge'])
rgb.show()
while True:

	#####################################
	#			Etape 1 RFID			#
	#####################################

	AttenteCard = "En Attente de Carte"
	text_area = bitmap_label.Label(terminalio.FONT, text=AttenteCard, scale=2)
	text_area.x = 10
	text_area.y = 40
	board.DISPLAY.show(text_area)
	(stat, tag_type) = lecteur.request(lecteur.REQIDL)
	
	if stat == lecteur.OK:

		(stat, raw_uid) = lecteur.anticoll()

		if stat == lecteur.OK:
			
			print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
			collectRfid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
			codeCard = "Bienvenue !"
			text_area = bitmap_label.Label(terminalio.FONT, text=codeCard , scale=2)
			text_area.x = 10
			text_area.y = 40
			board.DISPLAY.show(text_area)
			idAutoriser =  "0x9331c692"
			print(collectRfid)	

				#####################################
				#		Etape 2 Destination			#
				#####################################

			if idAutoriser == collectRfid:
				badgeValide = True
				while badgeValide == True:
					rgb.fill(couleurs['jaune'])
					rgb.show()
					if tca.key_int:
				# first figure out how big the queue is
						events = tca.events_count
						# now print keyevent, row, column & key name
						for _ in range(events):
							keyevent = tca.next_event
							#  strip keyevent
							event = keyevent & 0x7F
							event -= 1
							#  figure out row
							row = event // 10
							#  figure out column
							col = event % 10
							#  print event type first
							
							#  use row & column coordinates to print key name
							
							if keyevent & 0x80:
								print("Row %d, Column %d, Key %s" % (row, col, keymap[col][row]))
								if str(keymap[col][row]) == "#" :
									badgeValide = False
									aeroport = []
								else:
									aeroport.append(str(keymap[col][row]))
									Number = str(Number) + keymap[col][row]
									text_area = bitmap_label.Label(terminalio.FONT, text=Number , scale=2)
									text_area.x = 10
									text_area.y = 40
									board.DISPLAY.show(text_area)
									if len(aeroport) == 3:
										print(aeroport)
							
										
										tempAeroport = aeroport[0] + aeroport[1] + aeroport[2]
										if int(tempAeroport) in aeroports :
											print(aeroports[int(tempAeroport)])
											temp_str += "Destination : {}".format(aeroports[int(tempAeroport)])
											aeroportFind = "Destination : "+"\n {}".format(aeroports[int(tempAeroport)])
											text_area = bitmap_label.Label(terminalio.FONT, text=aeroportFind , scale=2)
											text_area.x = 10
											text_area.y = 40
											board.DISPLAY.show(text_area)
										else:
											badgeValide = False
											inco = "Aéroport inconnue"
											text_area = bitmap_label.Label(terminalio.FONT, text=inco , scale=2)
											text_area.x = 10
											text_area.y = 40
											board.DISPLAY.show(text_area)
											time.sleep(2)
											
											rgb.fill(couleurs['rouge'])
											rgb.show()
											tempAeroport = 0
											aeroport = []
										time.sleep(5)
										

						tca.key_int = True  # clear the IRQ by writing 1 to it
						time.sleep(0.01)
			#print(garderCap)
					distance = 15 

									#####################################
									#			Etape 3 Vole			#
									#####################################

					while btn.value == True and badgeValide == True and len(aeroport) == 3 and round(distance) > 10:

						#destination = aeroports[int(tempAeroport)]

						rgb.fill(couleurs['vert'])
						rgb.show()
						angle = defAngle(AxeX.value)
						my_servo.angle = angle 
						print(my_servo.angle)
						
						#distance = sonar.distance
						print("Distance en cm:", distance )
						if round(distance) < 10:
							rgb.fill(couleurs['rouge'])
							rgb.show()
							badgeValide = False

					
						VitesseNul = range(32000, 35000)
						Vitesse = 0
						# Pin pour L293D --> Moteur
						if AxeY.value in VitesseNul:
							motor1.throttle = 0
							print(0)
						elif(AxeY.value >= 35000):
							throttleV = ((AxeY.value - 26084.5) / 26084.5)
							motor1.throttle = throttleV
							Vitesse = throttleV * 100 
						else:
							throttleV = ((-26084.5 + AxeY.value) / 26084.5)
							motor1.throttle = throttleV
							print(throttleV * 100,"%")
							Vitesse = throttleV * 100

						if AxeZ.value < 480:
							garderCap = not garderCap
							time.sleep(0.5)
							print(garderCap)
						
						temperature = dht.temperature
						humidity = dht.humidity
						# Print what we got to the REPL
						print(temperature," " , humidity, " %")
						
						InfoEtat3 = temp_str + "\n" + "Température : {:.1f}C".format(temperature) + " \n " + "Humidité : {:.1f}%".format(humidity) + " \n " + "Angle : {:.1f}".format(my_servo.angle) + " \n " + "Vitesse : {:.1f}% \n \n \n \n \n ".format(Vitesse) 
						# Crée un objet bitmap_label pour afficher les deux valeurs
						text_area = bitmap_label.Label(terminalio.FONT, text=InfoEtat3 , scale=scale)
						text_area.x = 10
						text_area.y = 40
						print(InfoEtat3)
						if time.monotonic() - debutTemps > 0.1:

							board.DISPLAY.show(text_area)
							debutTemps = time.monotonic()

			else:
				print("Carte incorrect !")
						
    
        

	