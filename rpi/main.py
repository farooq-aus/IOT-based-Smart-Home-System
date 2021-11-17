import RPi.GPIO as GPIO
import LCD1602 as LCD
from keypad import Keypad
from rfid import RFID
from buzzer import Buzzer
from pir import PIR
from ultrasonic import Ultrasonic
from light_sensor import Light_sensor
from temp_sensor import Temp_sensor

import server

import PCF8591 as ADC
import requests
import threading
import time
import picamera
from env import ANIMATION_SERVER_IP

camera = picamera.PiCamera()
camera.resolution = (640, 480)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LCD.init(0x27, 1)


ADC.setup(0x48)

power_button = 17
GPIO.setup(power_button, GPIO.IN)


if __name__ == '__main__':
    
    print('<< Push button to Power ON >>')
    while not GPIO.input(17):
        pass
    
    access = [False]
    trigger = [False]
    garage = [False]

    
    keypad = Keypad(GPIO, LCD, camera)
    keypad_thread = threading.Thread(target=keypad.enter_pass, args=(access,trigger))
    
    rfid = RFID()
    rfid_thread = threading.Thread(target=rfid.scanRFID, args=(access,))
    
    buzzer = Buzzer(GPIO)
    buzzer_thread = threading.Thread(target=buzzer.alarm, args=(trigger,))
    
    pir = PIR(GPIO, camera)
    pir_thread = threading.Thread(target=pir.start)
    
    ultrasonic = Ultrasonic(GPIO)
    ultrasonic_thread = threading.Thread(target=ultrasonic.garage_door, args=(garage,))
    
    light_sensor =  Light_sensor(ADC)
    light_sensor_thread = threading.Thread(target=light_sensor.start)
    
    temp_sensor =  Temp_sensor(ADC)
    temp_sensor_thread = threading.Thread(target=temp_sensor.start, args=(trigger,))

    server_thread = threading.Thread(target=server.start_server)
    
    server_thread.start()
    keypad_thread.start()
    rfid_thread.start()
    buzzer_thread.start()
    pir_thread.start()
    ultrasonic_thread.start()
    light_sensor_thread.start()
    temp_sensor_thread.start()
    

    
    while True:
        pass
#        if access[0]:
#            # requests.get("http://"+ANIMATION_SERVER_IP+"/door")
#            print('Door opened')
#            access[0] = False
            
#        if garage[0]:
            # requests.get("http://"+ANIMATION_SERVER_IP+"/door")
#            print('Garage door opened')
#            garage[0] = False
