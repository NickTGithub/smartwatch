import board
import busio
import displayio
from fourwire import FourWire
import time
import digitalio
import adafruit_gc9a01a

time.sleep(1)

displayio.release_displays()

vib = digitalio.DigitalInOut(board.D0)
vib.direction = digitalio.Direction.OUTPUT
vib.value = True

spi = board.SPI()

display_bus = FourWire(spi,command=board.D6,chip_select=board.D7,reset=board.D2,)

display = adafruit_gc9a01a.GC9A01A(display_bus,width=240,height=240,rotation=0)

bitmap = displayio.OnDiskBitmap("/lebanana.bmp") #put file path in parenthesis. Ex. image.bmp -->"/image.bmp"

tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

group = displayio.Group()
group.append(tile_grid)

print('show')
vib.value = False
display.root_group = group

while True:
    pass
