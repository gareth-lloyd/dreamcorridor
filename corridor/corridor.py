import nxt.locator
import time
from nxt.sensor import *

from frames import write_frame
from pbm import pbm_lines

from opencv import highgui
import opencv
import Image
import os

colours = ["black","blue","green","yellow","red","white"]
IMG_DIR = '../images/'

def image_names():
    for _, _, filenames in os.walk(IMG_DIR):
        return [filename for filename in filenames if not filename.startswith('.')]
pbm_images = image_names()

b = nxt.locator.find_one_brick()
camera = highgui.cvCreateCameraCapture(1)#initial camera setup, presuming it is the 2nd (i.e. pos 1) camera
threshold = 5 #amount of difference to trigger event
DEAD_TIME = 3 #sleep time to prevent multiple images
DISPLAY_TIME = 2
baseline = Ultrasonic(b, PORT_4).get_sample() #get baseline distance measurement from sensor.
print "baseline sampled at "+str(baseline)+"cm"

def get_image():
    print "taking photo"
    im = highgui.cvQueryFrame(camera)
    return opencv.adaptors.Ipl2PIL(im)

def get_dream(im, colour):
    #convert the image and other inputs into a "dream"
    r,g,bl = im.convert("RGB").resize((1,1), Image.ANTIALIAS).getpixel((0,0))
    print get_main_colour(im)
    dream = r+g+bl+colour #clever AI algorithm
    divisor = 780 / len(pbm_images)
    print 'dream %s, divisor %s, r %s, g %s, b %s, lego colour %s' % (dream, divisor, r, g, bl, colour)
    return dream / divisor

def do_dream():
    colour_sensed = Color20(b,PORT_3).get_color()

    print "LEGO Colour: "+colours[colour_sensed]
    im = get_image()

    dream = get_dream(im, colour_sensed)
    assert 0 <= dream < len(pbm_images)

    print "writing image %s to peggy" % pbm_images[dream]
    write_frame(pbm_lines(IMG_DIR + pbm_images[dream]))

    im.save('dream' + time.strftime('%H%M%S') + '.jpg', 'JPEG')

    print "saving photo"
    highgui.cvReleaseCapture(camera)#reset camera
    global camera
    camera = highgui.cvCreateCameraCapture(1)

    time.sleep(DISPLAY_TIME)
    write_frame()

def get_main_color(img):
    colors = img.getcolors(256) #put a higher value if there are many colors in your image
    max_occurence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
        return most_present
    except TypeError:
        return 255, 255, 255

if __name__ == '__main__':
    while(True):
        sample = Ultrasonic(b, PORT_4).get_sample()
        if (sample + threshold) < baseline:
            do_dream()
	    time.sleep(DEAD_TIME)
