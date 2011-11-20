import nxt.locator
import time
from nxt.sensor import *

from frames import write_frame
from pbm import pbm_lines

from opencv import highgui
import opencv
import Image

colours = ["black","blue","green","yellow","red","white"]
pbm_images = ["cloud","lightning","face","sun-cloud","rain","stripe","sun","test","cloud","lightning","face","sun-cloud","rain","stripe","sun","test","cloud","lightning","face","sun-cloud"]

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

def analyse_data(image,colour):
    #convert the image and other inputs into a "dream"
    r,g,b = image.convert("RGB").resize((1,1), Image.ANTIALIAS).getpixel((0,0))

while(True):
    sample = Ultrasonic(b, PORT_4).get_sample()
    if (sample+threshold)<baseline:
        
        print "person detected at " + str(sample)+"cm"
        colour_sensed = Color20(b,PORT_3).get_color()
        print "LEGO Colour: "+colours[colour_sensed]
        im = get_image()
        r,g,b = im.convert("RGB").resize((1,1), Image.ANTIALIAS).getpixel((0,0))
        pic = r+g+b+colour_sensed #clever AI algorithm
        #write to peggy
        divisor = 780 / len(pbm_images)
        print "writing image "+pbm_images[pic/divisor]+" to peggy"
        write_frame(pbm_lines('../images/'+pbm_images[pic / divisor]+'.pbm'))
        
        print "saving photo"
        im.save('test'+time.strftime('%H%M%S')+'.jpg','JPEG')
        
        highgui.cvReleaseCapture(camera)#reset camera
        camera = highgui.cvCreateCameraCapture(1)
       
    	time.sleep(sleeptime)

