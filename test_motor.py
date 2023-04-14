import board
import pwmio
import time
import math
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motor import motor
import analogio

""" in1Pin=pwmio.PWMOut(board.D6)
in2Pin=pwmio.PWMOut(board.D5)

moteur = motor.DCMotor(in1Pin,in2Pin)
analog_pin = analogio.AnalogIn(board.D9) """


# Potentiomètre
puissance = analogio.AnalogIn(board.D9)

# Pin pour L293D --> Moteur
pin2 = board.D6
pin7 = board.D5

pwm1 = pwmio.PWMOut(pin2, frequency=5000, duty_cycle=0)
pwm2 = pwmio.PWMOut(pin7, frequency=5000, duty_cycle=0)

motor1 = motor.DCMotor(pwm1, pwm2)
motor1.throttle = 1

while True:

    if(puissance.value >= 26084):
        throttleV = ((puissance.value - 26084) / 26084)
    else:
        throttleV = ((-26084 + puissance.value) / 26084)

    motor1.throttle = throttleV



""" def sensMotor(dir, speedVal):
    if dir:
        in1Pin.duty_cycle = int(speedVal / 100 * 52169)
        alumer.duty_cycle = int(speedVal / 100 * 52169)
        in2Pin.duty_cycle = 0
    else:
        in1Pin.duty_cycle = 0
        alumer.duty_cycle = int(speedVal / 100 * 52169)
        in2Pin.duty_cycle = int(speedVal / 100 * 52169)

while True:
    potenVal = analog_pin.value / 52169 * 200 - 100
    print(analog_pin.value )
    rotationDir = potenVal >= 0
    sensMotor(rotationDir, potenVal)
    time.sleep(0.01)
 """
