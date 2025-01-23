# -*- coding: utf-8 -*-
from .StreamDock import StreamDock
from PIL import Image
import ctypes
import ctypes.util
import os, io
from ..ImageHelpers.PILHelper import *
import random

class StreamDock293s(StreamDock):
    KEY_MAP = True
    def __init__(self, transport1, devInfo):
        super().__init__(transport1, devInfo)

    # 设置设备的屏幕亮度
    def set_brightness(self, percent):
        return self.transport.setBrightness(percent)
    

    # 设置设备的背景图片  854 * 480
    def set_touchscreen_image(self, image):
        image = Image.open(image)
        image = to_native_touchscreen_format(self, image)
        width, height = image.size
        bgr_data = []
    
        for x in range(width):
            for y in range(height):
                r,g,b = image.getpixel((x,y))
                bgr_data.extend([b,g,r])
        arr_type = ctypes.c_char * len(bgr_data)
        arr_ctypes = arr_type(*bgr_data)

        return self.transport.setBackgroundImg(ctypes.cast(arr_ctypes, ctypes.POINTER(ctypes.c_ubyte)),width * height * 3)
    
    # 设置设备的按键图标 85 * 85
    def set_key_image(self, key, path):
        image = Image.open(path)
        rotated_image = to_native_key_format(self, image)

        rotated_image.save("Temporary.jpg", "JPEG", subsampling=0, quality=100)
        returnvalue = self.transport.setKeyImg(bytes("Temporary.jpg",'utf-8'), key)
        os.remove("Temporary.jpg")
        return returnvalue
    
    def get_serial_number(self,lenth):
        return self.transport.getInputReport(lenth)
    
    def key_image_format(self):
        return {
            'size': (85, 85),
            'format': "JPEG",
            'rotation': 90,
            'flip': (False, False)
        }
    
    def touchscreen_image_format(self):
        return {
            'size': (854, 480),
            'format': "JPEG",
            'rotation': 0,
            'flip': (True, False)
        }
    