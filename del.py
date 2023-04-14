#Code by jos
import board
import analogio
from digitalio import DigitalInOut, Direction, Pull


Del = DigitalInOut(board.A1)
Del.direction = Direction.OUTPUT

while True:
    Del.value = True