import nxt.locator
import time
from nxt.sensor import *

from opencv import highgui
import opencv
import Image

b = nxt.locator.find_one_brick()
camera = highgui.cvCreateCameraCapture(1)
threshold = 5
baseline = Ultrasonic(b, PORT_4).get_sample()
print "baseline sampled at "+str(baseline)+"cm"
def get_image():
    print "taking photo"
    #camera = highgui.cvCreateCameraCapture(1)
    im = highgui.cvQueryFrame(camera)
    #im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    #highgui.cvReleaseCapture(camera)
    #camera = highgui.cvCreateCameraCapture(1)
    return opencv.adaptors.Ipl2PIL(im)


while(True):
    sample = Ultrasonic(b, PORT_4).get_sample()
    if (sample+threshold)<baseline:
        print "person detected at " + str(sample)+"cm"
        im = get_image()
	highgui.cvReleaseCapture(camera)
	camera = highgui.cvCreateCameraCapture(1)
	print "saving photo"
        im.save('test'+time.strftime('%H%M%S')+'.jpg','JPEG')
    	time.sleep(10)

