import time
import requests
from env import ANIMATION_SERVER_IP

class Ultrasonic:
    def __init__(self,GPIO):
        self.GPIO = GPIO
        self.TRIG=18
        self.ECHO=16
        self.GPIO.setup(self.TRIG, self.GPIO.OUT)
        self.GPIO.setup(self.ECHO, self.GPIO.IN)
        
    def distance(self):
        self.GPIO.output(self.TRIG, self.GPIO.LOW) 
        time.sleep(0.000002)
        self.GPIO.output(self.TRIG, 1)
        time.sleep(0.00001)
        self.GPIO.output(self.TRIG, 0)

        while self.GPIO.input(self.ECHO) == 0:
            a = 0                                          
        time1 = time.time()                        
        while self.GPIO.input(self.ECHO) == 1:
            a = 0                                                  
        time2 = time.time()                        
        duration = time2 - time1
        return duration*1000000/58
    
    def garage_door(self, garage):
        while True:
            if self.distance() < 5:
                if not garage[0]:
                    print('Garage door opened')
                    requests.get("http://"+ANIMATION_SERVER_IP+"/garage_door")
                garage[0] = True
                time.sleep(5)
            elif self.distance() > 5 and garage[0]:
                garage[0] = False
                print('Garage door closed')
                requests.get("http://"+ANIMATION_SERVER_IP+"/garage_door")
                time.sleep(1)

                
            
