#!/usr/bin/env python
from datetime import datetime
import os, sys
import serial
import time
import random
from pbm import pbm_lines

SLEEPY_TIME = 1
START_FRAME = '^'
END_LINE = '+'
INPUT_DIFFERENCE = 10
HEIGHT = 25
BLANK_FRAME = ['\x00\x00\x00\x00' for _ in range(HEIGHT)]

ser = serial.Serial('/dev/tty.usbserial-A60049W8', 28800)
time.sleep(1)

def write_frame(lines=None):
    if not lines:
        lines = BLANK_FRAME
    ser.write(START_FRAME)
    for line in lines:
        for byte in line:
            ser.write(byte)
        ser.write(END_LINE)

def write_random():
    write_lines([''.join([chr(random.randint(0,255)) for x in range(4)]) for y in range(25)])

if __name__ == '__main__':
    try:
        while(True):
            img_dir = '../images/'
            for dirname, dirnames, filenames in os.walk(img_dir):
                random.shuffle(filenames)
                if not filenames[0].startswith('.'):
                    write_frame(pbm_lines(img_dir + filenames[0]))
            time.sleep(2)
    except Exception, e:
        print e
    finally:
        ser.close()
