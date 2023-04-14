import time
import board
import pwmio
from adafruit_motor import motor

# init des broches A4 et A5 en tant que sortie
motorA4 = pwmio.PWMOut(board.D6)
motorA5 = pwmio.PWMOut(board.D5)

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