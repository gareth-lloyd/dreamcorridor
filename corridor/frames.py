#!/usr/bin/env python
from datetime import datetime
import sys
import serial
import time
from random import randint

SLEEPY_TIME = 1
START_FRAME = '^'
END_LINE = '+'
INPUT_DIFFERENCE = 10

ser = serial.Serial('/dev/tty.usbserial-A60049W8', 28800)
time.sleep(1)

def write_frame(lines):
    ser.write(START_FRAME)
    for line in lines:
        for byte in line:
            ser.write(byte)
        ser.write(END_LINE)

def write_random():
    write_lines([''.join([chr(randint(0,255)) for x in range(4)]) for y in range(25)])

if __name__ == '__main__':
    try:
        while(True):
            write_random()
            time.sleep(0.1)
    except Exception, e:
        print e
    finally:
        ser.close()
