import nxt.locator
import time
from nxt.sensor import *

from opencv import highgui
import opencv
import Image

colours = ["black","blue","green","yellow","red","white"]
b = nxt.locator.find_one_brick()
camera = highgui.cvCreateCameraCapture(1)#initial camera setup, presuming it is the 2nd (i.e. pos 1) camera
threshold = 5 #amount of difference to trigger event
sleeptime = 5 #sleep time to prevent multiple images
baseline = Ultrasonic(b, PORT_4).get_sample() #get baseline distance measurement from sensor.
print "baseline sampled at "+str(baseline)+"cm"
def get_image():
    print "taking photo"
    im = highgui.cvQueryFrame(camera)
    
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im)


while(True):
    sample = Ultrasonic(b, PORT_4).get_sample()
    if (sample+threshold)<baseline:
        print "person detected at " + str(sample)+"cm"
        im = get_image()
        print colours[Color20(b,PORT_3).get_color()]
    	print "saving photo"
        im.save('test'+time.strftime('%H%M%S')+'.jpg','JPEG')
        highgui.cvReleaseCapture(camera)#reset camera
        camera = highgui.cvCreateCameraCapture(1)
    	time.sleep(sleeptime)

