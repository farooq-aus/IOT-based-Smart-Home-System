

import time
import picamera

class Cam:
    def __init__(self, camera):    
    camera = picamera.PiCamera()
    camera.resolution = (480,480)
    camera.start_preview()
    time.sleep(10)
    camera.capture('img', 'jpeg')
    camera.stop_preview()
 

