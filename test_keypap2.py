
import time
import digitalio
import board
import adafruit_matrixkeypad

# Membrane 3x4 matrix keypad - https://www.adafruit.com/product/419
cols = [digitalio.DigitalInOut(x) for x in (board.D10, board.D9, board.D6, board.D5)]
rows = [digitalio.DigitalInOut(x) for x in (board.A2, board.A3, board.A4, board.A5)]


# 3x4 matrix keypad - Rows and columns are mixed up for https://www.adafruit.com/product/3845
# Use the same wiring as in the guide with the following setup lines:
# cols = [digitalio.DigitalInOut(x) for x in (board.D11, board.D13, board.D9)]
# rows = [digitalio.DigitalInOut(x) for x in (board.D12, board.D5, board.D6, board.D10)]

keys = ((1, 2, 3, "A"), (4, 5, 6, "B"), (7, 8, 9,"C"), ("*", 0, "#", "D"))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
num = "0"
while True:
    key = keypad.pressed_keys
    if keys != '#':
      num += key[1]
      print(num)
    elif keys == '#':
       numFin = num * num
       print("Result ", numFin)
    time.sleep(0.1)

 