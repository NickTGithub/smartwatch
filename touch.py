import board
import adafruit_cst8xx
import digitalio
import busio

i2c = board.I2C()

print(i2c.scan())

rst = digitalio.DigitalInOut(board.D3)
rst.direction = digitalio.Direction.OUTPUT

inter = digitalio.DigitalInOut(board.D9)
inter.direction = digitalio.Direction.INPUT

#rst.value = True

ctp = adafruit_cst8xx.Adafruit_CST8XX(i2c)

events = adafruit_cst8xx.EVENTS

print('go')

while True:
    if ctp.touched:
        for touch_id, touch in enumerate(ctp.touches):
            x = touch["x"]
            y = touch["y"]
            event = events[touch["event_id"]]
            print(f"touch_id: {touch_id}, x: {x}, y: {y}, event: {event}")
