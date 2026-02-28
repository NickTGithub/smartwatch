import board
import adafruit_cst8xx
import digitalio
import busio
import time

i2c = busio.I2C(board.D5, board.D4)

rst = digitalio.DigitalInOut(board.D3)
rst.direction = digitalio.Direction.OUTPUT

rst.value = False
time.sleep(0.02)
rst.value = True
time.sleep(0.3)

ctp = adafruit_cst8xx.Adafruit_CST8XX(i2c)

events = adafruit_cst8xx.EVENTS

print("go")

while True:
    if ctp.touched:
        for touch_id, touch in enumerate(ctp.touches):
            x = touch["x"]
            y = touch["y"]
            event = events[touch["event_id"]]
            print(f"touch_id: {touch_id}, x: {x}, y: {y}, event: {event}")
