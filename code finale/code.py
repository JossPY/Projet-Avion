
import board
import analogio
import math
import pwmio
from adafruit_motor import servo , motor
import time

# Init du joystick
AxeX = analogio.AnalogIn(board.A3)         #Max=52825
AxeY = analogio.AnalogIn(board.A5)         #Max=54116
AxeZ = analogio.AnalogIn(board.A4)

pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)


my_servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

pin2 = board.D6
pin7 = board.D9

pwm1 = pwmio.PWMOut(pin2, frequency=5000, duty_cycle=0)
pwm2 = pwmio.PWMOut(pin7, frequency=5000, duty_cycle=0)

motor1 = motor.DCMotor(pwm1, pwm2)
motor1.throttle = 1



def defAngle(pot_value): 
        rangeValue = range(32000, 35000)
        #print(pot_value)
        if pot_value in rangeValue:
            return 90
        else:
            pot_value = (pot_value / 52447) * 180
            return pot_value
garderCap = False
while True:
    
    if AxeZ.value < 600:
        garderCap = not garderCap
        time.sleep(0.5)
        print(garderCap)

    if garderCap == False:
        angle = defAngle(AxeX.value)
        #print(AxeX.value)
        my_servo.angle = angle
        print(my_servo.angle)
        


        VitesseNul = range(32000, 35000)
        
        # Pin pour L293D --> Moteur
        if AxeY.value in VitesseNul:
            motor1.throttle = 0
            print(0)
        elif(AxeY.value >= 26084.5):
            throttleV = ((AxeY.value - 26084.5) / 26084.5)
            motor1.throttle = throttleV
            print(throttleV * 100 ,"%")
        else:
            throttleV = ((-26084.5 + AxeY.value) / 26084.5)
            motor1.throttle = throttleV
            print(throttleV * 100,"%")

    
    
        