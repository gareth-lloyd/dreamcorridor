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
    for _, _, filenames in os.walk_dir(IMG_DIR):
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

def get_dream(image, colour):
    #convert the image and other inputs into a "dream"
    r,g,bl = im.convert("RGB").resize((1,1), Image.ANTIALIAS).getpixel((0,0))
    dream = r+g+bl+colour_sensed #clever AI algorithm
    divisor = 780 / len(pbm_images)
    return dream / divisor

def do_dream():
    print "person detected at " + str(sample)+"cm"
    colour_sensed = Color20(b,PORT_3).get_color()

    print "LEGO Colour: "+colours[colour_sensed]
    im = get_image()

    dream = get_dream(im, colour_sensed)
    assert 0 <= dream < len(pbm_images)

    print "writing image %s to peggy" % pbm_images[dream]
    write_frame(pbm_lines(IMG_DIR + pbm_images[dream]))

    print "saving photo"
    im.save('test'+time.strftime('%H%M%S')+'.jpg','JPEG')

    highgui.cvReleaseCapture(camera)#reset camera
    camera = highgui.cvCreateCameraCapture(1)

    time.sleep(DISPLAY_TIME)
    write_frame()

    time.sleep(DEAD_TIME)

if __name__ == '__main__':
    while(True):
        sample = Ultrasonic(b, PORT_4).get_sample()
        if (sample + threshold) < baseline:
            do_dream()
