#import RPi.GPIO as GPIO
#import LCD1602 as LCD
#LCD.init(0x27, 1)

import time
import requests
from env import ANIMATION_SERVER_IP



class Keypad:
    def __init__(self, GPIO, LCD, camera):
        
        self.GPIO = GPIO
        self.LCD = LCD
        self.camera = camera
        self.button = 17
        
        self.alarm_LED = 5
        self.GPIO.setup(self.alarm_LED, self.GPIO.OUT)

        self.GPIO.setup(19, self.GPIO.IN, pull_up_down = self.GPIO.PUD_UP) 
        self.GPIO.setup(20, self.GPIO.IN, pull_up_down = self.GPIO.PUD_UP) 
        self.GPIO.setup(21, self.GPIO.IN, pull_up_down = self.GPIO.PUD_UP) 
        self.GPIO.setup(22, self.GPIO.IN, pull_up_down = self.GPIO.PUD_UP) 

        self.GPIO.setup(self.button, self.GPIO.IN) # button
        self.GPIO.setup(23, self.GPIO.OUT) 
        self.GPIO.setup(24, self.GPIO.OUT) 
        self.GPIO.setup(25, self.GPIO.OUT) 
        self.GPIO.setup(26, self.GPIO.OUT)

    def keypad(self): 
        while(True): 

            self.GPIO.output(26, self.GPIO.LOW)
            self.GPIO.output(25, self.GPIO.HIGH)
            self.GPIO.output(24, self.GPIO.HIGH)
            self.GPIO.output(23, self.GPIO.HIGH)

            if (self.GPIO.input(22)==0):
                return(1, '!')
                break

            if (self.GPIO.input(21)==0):
                return(4, '$')
                break

            if (self.GPIO.input(20)==0):
                return(7, '&')
                break

            if (self.GPIO.input(19)==0):
                return(0xE)
                break

            self.GPIO.output(26, self.GPIO.HIGH)
            self.GPIO.output(25, self.GPIO.LOW)
            self.GPIO.output(24, self.GPIO.HIGH)
            self.GPIO.output(23, self.GPIO.HIGH)

            if (self.GPIO.input(22)==0):
                return(2, '@')
                break

            if (self.GPIO.input(21)==0):
                return(5, '%')
                break

            if (self.GPIO.input(20)==0):
                return(8, '*')
                break
     
            if (self.GPIO.input(19)==0):
                return(0, ')')
                break


            self.GPIO.output(26, self.GPIO.HIGH)
            self.GPIO.output(25, self.GPIO.HIGH)
            self.GPIO.output(24, self.GPIO.LOW)
            self.GPIO.output(23, self.GPIO.HIGH)

            if (self.GPIO.input(22)==0):
                return(3, '#')
                break

            if (self.GPIO.input(21)==0):
                return(6, '^')
                break
            #Scan row 2
            if (self.GPIO.input(20)==0):
                return(9,'(')
                break
     
            if (self.GPIO.input(19)==0):
                return(0XF)
                break

            self.GPIO.output(26, self.GPIO.HIGH)
            self.GPIO.output(25, self.GPIO.HIGH)
            self.GPIO.output(24, self.GPIO.HIGH)
            self.GPIO.output(23, self.GPIO.LOW)

            if (self.GPIO.input(22)==0):
                return(0XA)
                break

            if (self.GPIO.input(21)==0):
                return(0XB)
                break

            if (self.GPIO.input(20)==0):
                return(0XC)
                break

            if (self.GPIO.input(19)==0):
                return(0XD)
                break


    def flash_LED(self):
        for i in range(3):
            self.GPIO.output(self.alarm_LED, self.GPIO.HIGH)
            time.sleep(0.5)
            self.GPIO.output(self.alarm_LED, self.GPIO.LOW)
            time.sleep(0.5)

    def enter_pass(self, access, trigger):
        
        wrong_count = 0
        while True:
            self.LCD.print(0, "Enter password: ")
            
            pin = []
            
            for i in range(4):
                key, _ = self.keypad()
                self.LCD.write(i, 1, str(key))
                pin.append(key)
                time.sleep(0.20)

            pin = "".join(map(str,pin))
            
            
            password= "1234"
            if (pin == password):
                self.LCD.print(0, "Access granted!")
                wrong_count = 0 # reset
                access[0] = True # open door
                requests.get("http://"+ANIMATION_SERVER_IP+"/door")
                
            else:
                self.LCD.print(0, "Access denied!")
                wrong_count += 1
                if wrong_count == 3:
                    wrong_count = 0
                    self.camera.annotate_text = time.ctime()
                    self.camera.capture('static/intruder.jpeg', 'jpeg')
                    requests.get('http://localhost:5555/intruder') # send alert
                    trigger[0] = True # sound alarm
                    self.flash_LED()
                    
                access[0] = False # keep door closed
                
            time.sleep(1) # to make msg visible
                
            

