# OLEDtext.py

# This Python code is meant for use with the Raspberry Pi and Adafruit's monochrome displays!

# This program is the simplest in the whole repo. All it does is print 3 'Hello!'s in various forms on the OLED display.
import board
import adafruit_ssd1306
import digitalio
from PIL import Image, ImageDraw, ImageFont
i2c = board.I2C()

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
image = Image.new("1",(oled.width, oled.height))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

text = "Hello World"
draw.text((0,0), text, font=font, fill = 255)
oled.image(image)
oled.show()
