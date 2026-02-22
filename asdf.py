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

print('show')
vib.value = False

while True:
    display.root_group = group_nando
    time.sleep(3)
    display.root_group = group_lebanana
    time.sleep(3)
    display.root_group = group_sidstappen
    time.sleep(3)
