# OLEDtext.py

# This Python code is meant for use with the Raspberry Pi and Adafruit's monochrome displays!

# This program is the simplest in the whole repo. All it does is print 3 'Hello!'s in various forms on the OLED display.
import board
import adafruit_ssd1306
import digitalio
import cv2
from PIL import Image, ImageDraw, ImageFont
import os
i2c = board.I2C()

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
image = Image.new("1",(oled.width, oled.height))
draw = ImageDraw.Draw(image)

font_path = os.path.join(cv2.__path__[0], 'qt', 'fonts','DejaVuSans.ttf')
font = ImageFont.truetype(font_path, size = 17)
text = "Hello World"
draw.text((0,0), text, font=font, fill = 255)
oled.image(image)
oled.show()
