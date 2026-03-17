import board
import busio
import displayio
from fourwire import FourWire
import time
import digitalio
import adafruit_gc9a01a
import math
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text import label
import adafruit_cst8xx
import terminalio

### SETUP STUFF ###

time.sleep(1)

displayio.release_displays()

spi = board.SPI()

display_bus = FourWire(spi,command=board.D6,chip_select=board.D7,reset=board.D2,)

display = adafruit_gc9a01a.GC9A01A(display_bus,width=240,height=240,rotation=0)

i2c = busio.I2C(board.D5, board.D4)

rst = digitalio.DigitalInOut(board.D3)
rst.direction = digitalio.Direction.OUTPUT

rst.value = False
time.sleep(0.02)
rst.value = True
time.sleep(0.3)

ctp = adafruit_cst8xx.Adafruit_CST8XX(i2c)

events = adafruit_cst8xx.EVENTS

screen = 'normal'

### END SETUP STUFF ###

### BACKGROUND PIC ###
group = displayio.Group()

background = displayio.Group()

bg = displayio.Bitmap(240, 240, 1)
palette = displayio.Palette(1)
palette[0] = 0x000000

tile_bg = displayio.TileGrid(bg,pixel_shader=palette)

background_pic = displayio.OnDiskBitmap("/lebanana.bmp")
tile_background_pic = displayio.TileGrid(background_pic, pixel_shader=background_pic.pixel_shader)

center = Circle(120,120,5,fill=0x0000FF,outline=0xFF00FF,stroke=3)
l = Circle(0,120,5,fill=0x0000FF,outline=0xFF00FF,stroke=3)
r = Circle(240,120,5,fill=0x0000FF,outline=0xFF00FF,stroke=3)
u = Circle(120,0,5,fill=0x0000FF,outline=0xFF00FF,stroke=3)
d = Circle(120,240,5,fill=0x0000FF,outline=0xFF00FF,stroke=3)

font = terminalio.FONT
color = 0xFF0000

background.append(tile_bg)
background.append(tile_background_pic)

### END BACKGROUND PIC ###

### TIME ###

normal = displayio.Group()
timer = displayio.Group()

timer_y = 120

mins = 59
hr = 11
apm = 'PM' #or PM

new_day = False

display_min = str(mins)
display_hr = str(hr)

last_time = time.time() - 57

date_scale = 2
date_y = 65

day = 31
month = 12

day_threshold_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
day_threshold_index = 0
day_threshold = day_threshold_list[day_threshold_index]

year = 2026

weekday_list = ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']
weekday_index = 3
weekday = weekday_list[weekday_index]

display_day = str(day)
display_month = str(month)

min_tile = label.Label(font, text="  ", color=color, anchor_point = (0,0), scale=6)
min_tile.x = 130
min_tile.y = timer_y

hr_tile = label.Label(font, text="  ", color=color, anchor_point = (0,0), scale=6)
hr_tile.x = 80
hr_tile.y = timer_y

colon = label.Label(font, text=":", color=color, anchor_point = (0,0), scale=6)
colon.x = 105
colon.y = timer_y - 8

apm_tile = label.Label(font, text=apm, color=color, anchor_point = (0,0), scale=2)
apm_tile.x = 180
apm_tile.y = timer_y + 40

day_tile = label.Label(font, text="  ", color=color, anchor_point = (0,0), scale=date_scale)
day_tile.x = 70
day_tile.y = date_y

month_tile = label.Label(font, text="  ", color=color, anchor_point = (0,0), scale=date_scale)
month_tile.x = 30
month_tile.y = date_y

slash = label.Label(font, text="/", color=color, anchor_point = (0,0), scale=date_scale)
slash.x = 55
slash.y = date_y

weekday_tile = label.Label(font, text=weekday, color=color, anchor_point = (0,0), scale=date_scale)
weekday_tile.x = 175
weekday_tile.y = date_y

timer.append(min_tile)
timer.append(hr_tile)
timer.append(colon)
timer.append(apm_tile)
timer.append(day_tile)
timer.append(month_tile)
timer.append(slash)
timer.append(weekday_tile)

min_test = None
hr_test = None
apm_test = None
day_test = None
month_test = None
weekday_test = None

hitbox_x = [121, 40, 165, 46, 0, 140]
hitbox_y = [90, 90, 151, 45, 45, 45]
hitbox_x2 = [210, 119, 215, 75, 44, 240]
hitbox_y2 = [150, 150, 175, 80, 80, 80]

hitbox_widths = []
hitbox_heights = []

for i in range(0,6):
    hitbox_widths.append(hitbox_x2[i] - hitbox_x[i])
    hitbox_heights.append(hitbox_y2[i] - hitbox_y[i])

hitbox_tiles = [min_tile, hr_tile, apm_tile, day_tile, month_tile, weekday_tile]
hitbox_tests = [min_test, hr_test, apm_test, day_test, month_test, weekday_test]

def updateTime():
    global mins, display_min, hr, display_hr, new_day, day, display_day, apm, weekday, weekday_index, weekday_list, \
        weekday_tile, new_day, new_time, day, day_threshold, day_threshold, day_threshold_index, \
        day_threshold_list, month, display_month, year, current_time, last_time
    current_time = time.time()
    new_time = False
    if current_time - last_time >= 60:
        mins += 1
        last_time = current_time
    if mins > 59:
        mins = 0
        hr += 1
        new_time = True
    if hr > 12:
        hr = 1
    if hr == 12 and new_time == True:
        if apm == 'AM':
            apm = 'PM'
        else:
            apm = 'AM'
            new_day = True
    if new_day == True:
        new_day = False
        day += 1
        weekday_index += 1
        if weekday_index > 6:
            weekday_index = 0

    if day > day_threshold:
        day = 1
        month += 1
        day_threshold_index += 1
        if day_threshold_index > 11:
            day_threshold_index = 0
        day_threshold = day_threshold_list[day_threshold_index]
        if year % 4 == 0 and day_threshold_index == 1:
            day_threshold = 29
    if month > 12:
        month = 1
        year += 1

def updateTimeLabels():
    global mins, display_min, hr, display_hr, new_day, day, display_day, apm, weekday, weekday_index, weekday_list, \
        weekday_tile, new_day, new_time, day, day_threshold, day_threshold, day_threshold_index, \
        day_threshold_list, month, display_month, year, current_time, last_time

    display_min = str(mins)
    if len(display_min) == 1:
        display_min = '0' + display_min

    display_hr = str(hr)
    if len(display_hr) == 2:
        hr_tile.x = 45
    else:
        hr_tile.x = 80

    display_day = str(day)
    display_month = str(month)
    if len(display_month) == 1:
        slash.x = 40
        day_tile.x = 55
        hitbox_x2[4] = 44

    else:
        slash.x = 55
        day_tile.x = 70
        hitbox_x2[4] = 69


        
    weekday = weekday_list[weekday_index]
    if len(weekday) == 3:
        weekday_tile.x = 183
    elif len(weekday) == 4:
        weekday_tile.x = 171
    else:
        weekday_tile.x = 160

    min_tile.text = display_min
    hr_tile.text = display_hr
    apm_tile.text = apm
    day_tile.text = display_day
    month_tile.text = display_month
    weekday_tile.text = weekday


### END TIME ###

### EVENTS ###

hold_counter = 0
swipe_x = 0
swipe_y = 0
comp_x = 0
comp_y = 0
initial_x = 120
initial_y = 120
magnitude = 0

x = None
y = None
magnitude = 0

def checkevent():
    global hold_counter, swipe_x, swipe_y, event, comp_x, comp_y, x, y, initial_x, initial_y, pointer, ogx, ogy, magnitude
    event = 'NOTHING'
    result = None
    if ctp.touched:
        for touch_id, touch in enumerate(ctp.touches):
            x = touch["x"]
            y = touch["y"]
            event = events[touch["event_id"]]
            #print(f"touch_id: {touch_id}, x: {x}, y: {y}, event: {event}")
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
        magnitude = math.sqrt((comp_x ** 2) + (comp_y ** 2))
    else:
        if hold_counter >= 3 and (magnitude > 4):
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
    if result != None:
        print(result, x, y, 'resultttt')
    return result, x, y, magnitude

### END EVENTS ###

normal.append(timer)
group.append(background)
group.append(normal)

display.root_group = group

clicker = 0

while True:
    updateTime()
    updateTimeLabels()
    time.sleep(0.0001)
