import board
import adafruit_cst8xx
import busio
import terminalio
from adafruit_display_text import label
import displayio
import adafruit_gc9a01a
from fourwire import FourWire
import digitalio
import time
import math
from adafruit_display_shapes.triangle import Triangle as Tri

height = 100

displayio.release_displays()

vib = digitalio.DigitalInOut(board.D0)
vib.direction = digitalio.Direction.OUTPUT

spi = board.SPI()

display_bus = FourWire(spi,command=board.D6,chip_select=board.D7,reset=board.D2,)

display = adafruit_gc9a01a.GC9A01A(display_bus,width=240,height=240,rotation=0)

# Set text, font, and color
sec = 00
minutes = 00
display_sec = str(sec)
display_min = str(minutes)
font = terminalio.FONT
color = 0xFF0000

sec_tile = label.Label(font, text=display_sec, color=color, anchor_point = (0.5,0.5), scale=6)
min_tile = label.Label(font, text=display_min, color=color, anchor_point = (0.5,0.5), scale=6)

colon = label.Label(font, text=":", color=color, anchor_point = (0.5,0.5), scale=6)

group = displayio.Group()

# Set the location
sec_tile.x = 125
sec_tile.y = height

min_tile.x = 75
min_tile.y = height

colon.x = 100
colon.y = height

bg = displayio.Bitmap(240, 240, 1)
palette = displayio.Palette(1)
palette[0] = 0x000000
tile_bg1 = displayio.TileGrid(bg,pixel_shader=palette)
lebanana = displayio.OnDiskBitmap("/lebanana.bmp")
tile_lebanana = displayio.TileGrid(lebanana, pixel_shader=lebanana.pixel_shader)
group_lebanana = displayio.Group(scale=1)
group_lebanana.append(tile_bg1)
group_lebanana.append(tile_lebanana)

group.append(group_lebanana)

group.append(sec_tile)
group.append(min_tile)
group.append(colon)

# Show it



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
misec = 0
last_time = time.time()
hold_counter = 0
swipe_x = 0
swipe_y = 0
comp_x = 0
comp_y = 0
pointer = Tri(120,120,120,120,150,150,fill=0x0000FF)
group.append(pointer)
display.root_group = group
initial_x = 120
initial_y = 120
print(len(group))
#print(pointer.x,pointer.y,pointer.x2,pointer.y2)



while True:
    current_time = time.time()
    event = 'NOTHING'
    if ctp.touched:
        for touch_id, touch in enumerate(ctp.touches):
            x = touch["x"]
            y = touch["y"]
            event = events[touch["event_id"]]
            #print(f"touch_id: {touch_id}, x: {x}, y: {y}, event: {event}")

    if event == 'PRESS':
        initial_x = x
        initial_y = y
    elif event == 'TOUCHING':
        hold_counter += 1
        comp_x =  initial_x - x
        comp_y = initial_y - y
        swipe_x = abs(comp_x)
        swipe_y = abs(comp_y)
    else:
        if hold_counter >= 5 and (swipe_x > 2 or swipe_y > 2):
            print('swipe', comp_x, comp_y)
            group.remove(pointer)
            pointer = Tri(120,120,120,120,(120-comp_x), (120-comp_y),fill=0x0000FF)
            group.append(pointer)

        elif 0 < hold_counter <= 20:
           print('clicked')
        elif 20 < hold_counter <= 300000:
           print('held')

        hold_counter = 0

    if current_time - last_time >= 1:
        last_time = current_time
        sec += 1
    if sec >= 60:
        sec = 0
        minutes += 1
    if minutes >= 10:
        min_tile.x = 40
    display_sec = str(sec)
    display_min = str(minutes)
    sec_tile.text = display_sec
    min_tile.text = display_min
    time.sleep(0.00001)

