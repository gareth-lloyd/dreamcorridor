#!/usr/bin/env python
from datetime import datetime
import serial
import time
from random import randint

SLEEPY_TIME = 1
TERMINATOR = ';'

ser = serial.Serial('/dev/tty.usbserial-A60049W8', 9600)

def set_row(row, val=None):
    if not val:
        val = randint(1, 15)

    ser.write(chr(row))
    for col in range(25):
        ser.write(chr(val))
    ser.write(TERMINATOR)

def update():
    for row in range(1, 25):
        set_row(row)

if __name__ == '__main__':
    try:
        print 'updating'
        update()
    except Exception as e:
        print e
    # time.sleep(SLEEPY_TIME)
