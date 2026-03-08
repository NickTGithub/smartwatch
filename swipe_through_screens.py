import board
import busio
import displayio
from fourwire import FourWire
import time
import digitalio
import adafruit_gc9a01a
import math
from adafruit_display_shapes.triangle import Triangle as Tri
from adafruit_display_text import label
import adafruit_cst8xx

time.sleep(1)

displayio.release_displays()

vib = digitalio.DigitalInOut(board.D0)
vib.direction = digitalio.Direction.OUTPUT
vib.value = True

spi = board.SPI()

display_bus = FourWire(spi,command=board.D6,chip_select=board.D7,reset=board.D2,)

display = adafruit_gc9a01a.GC9A01A(display_bus,width=240,height=240,rotation=0)

bg = displayio.Bitmap(240, 240, 1)
palette = displayio.Palette(1)
palette[0] = 0x000000

tile_bg0 = displayio.TileGrid(bg,pixel_shader=palette)
tile_bg1 = displayio.TileGrid(bg,pixel_shader=palette)
tile_bg2 = displayio.TileGrid(bg,pixel_shader=palette)

nando = displayio.OnDiskBitmap("/nando.bmp")
tile_nando = displayio.TileGrid(nando, pixel_shader=nando.pixel_shader)
group_nando = displayio.Group()
group_nando.append(tile_bg0)
group_nando.append(tile_nando)

lebanana = displayio.OnDiskBitmap("/lebanana.bmp")
tile_lebanana = displayio.TileGrid(lebanana, pixel_shader=lebanana.pixel_shader)
group_lebanana = displayio.Group()
group_lebanana.append(tile_bg1)
group_lebanana.append(tile_lebanana)

sidstappen = displayio.OnDiskBitmap("/sidstappen.bmp")
tile_sidstappen = displayio.TileGrid(sidstappen, pixel_shader=sidstappen.pixel_shader)
group_sidstappen = displayio.Group()
group_sidstappen.append(tile_bg2)
group_sidstappen.append(tile_sidstappen)

biggroup = displayio.Group()

print('show')
vib.value = False
biggroup.append(group_nando)
biggroup.append(group_sidstappen)
biggroup.append(group_lebanana)

display.root_group = biggroup


i2c = busio.I2C(board.D5, board.D4)

rst = digitalio.DigitalInOut(board.D3)
rst.direction = digitalio.Direction.OUTPUT

rst.value = False
time.sleep(0.02)
rst.value = True
time.sleep(0.3)

ctp = adafruit_cst8xx.Adafruit_CST8XX(i2c)

events = adafruit_cst8xx.EVENTS

misec = 0
last_time = time.time()
hold_counter = 0
swipe_x = 0
swipe_y = 0
comp_x = 0
comp_y = 0
display.root_group = biggroup
initial_x = 120
initial_y = 120

def checkevent():
    global hold_counter, swipe_x, swipe_y, event, comp_x, comp_y, x, y, initial_x, initial_y, pointer, ogx, ogy
    event = 'NOTHING'
    result = None
    if ctp.touched:
        for touch_id, touch in enumerate(ctp.touches):
            x = touch["x"]
            y = touch["y"]
            event = events[touch["event_id"]]
            x -= 120
            y -= 120
            y *= -1
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
        if hold_counter >= 3 and (swipe_x > 2 or swipe_y > 2):
            angle = math.degrees(math.atan2(comp_y, comp_x))
            angle -= 180
            if angle < 0:
                angle += 360
            if 0 <= angle < 45 or 315 < angle <= 360:
                result = 'swipe right'
            elif 45 < angle < 135:
                result = 'swipe up'
            elif 135 < angle < 225: 
                result = 'swipe left'
            elif 225 < angle < 315: 
                result = 'swipe down'
        elif 0 < hold_counter <= 20:
           result = 'clicked'
        elif 15 < hold_counter <= 300000:
           result = 'held'
        hold_counter = 0
    return result

while True:
    event_result = checkevent()
    if event_result == 'swipe down':
        biggroup.remove(group_nando)
        biggroup.append(group_nando)
    elif event_result == 'clicked':
        biggroup.remove(group_lebanana)
        biggroup.append(group_lebanana)
    elif event_result == 'held':
        biggroup.remove(group_sidstappen)
        biggroup.append(group_sidstappen)
    time.sleep(0.00001)

