import requests
import time
import os

class PIR:
    def __init__(self, GPIO, camera):
        self.GPIO = GPIO
        self.camera = camera
        self.PIR_PIN=27
        self.button = 4
        
        self.enable = False
        
        self.GPIO.setup(self.button, self.GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)
        self.GPIO.add_event_detect(self.button, self.GPIO.RISING, callback=self.set_enable, bouncetime=1000)
        

        self.GPIO.setup(self.PIR_PIN, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        self.ts = time.time()
        self.GPIO.add_event_detect(self.PIR_PIN, self.GPIO.FALLING, callback=self.action, bouncetime=200)
        self.alerted = False
        
    def set_enable(self, *args):
        self.enable = not self.enable
        print('Motion detection: ', 'Enabled' if self.enable else 'Disabled')


    
    def action(self, *args):
        curr = time.time()
        diff = curr - self.ts
        #print(diff)
        self.ts = curr
        
        if diff < 1.5 and self.enable:
            print('Motion detected')
            os.system('rm motion.h264 static/motion.mp4') 
            self.camera.annotate_text = time.ctime()
            self.camera.start_recording('motion.h264')
            self.camera.wait_recording(5)
#            time.sleep(5)
            self.camera.stop_recording()
            print('recorded')
#            self.convert()
            time.sleep(2)
            os.system('MP4Box -quiet -add motion.h264 static/motion.mp4 &> /dev/null')
#            if not self.alerted:
            requests.get('http://localhost:5555/motiond')
#                self.alerted=True
    
    def start(self):
        while True:
            pass # keep thread alive
