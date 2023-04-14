import board
import time
import analogio
from digitalio import DigitalInOut, Direction, Pull
import pwmio
from adafruit_motor import servo


analog_pin = analogio.AnalogIn(board.D5)

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)

def defAngle(pot_value): 
    return (pot_value / 52169) * 180


while True:
    angle = defAngle(analog_pin.value)
    my_servo.angle = angle
    time.sleep(0.01)