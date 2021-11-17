import time

class Buzzer:
    
    def __init__(self, GPIO):
        self.GPIO = GPIO
        buzz_pin = 12
        self.GPIO.setup(buzz_pin, self.GPIO.OUT)
        self.buzz = self.GPIO.PWM(buzz_pin, 500)
        self.buzz.start(0)


    def alarm(self, trigger):
        while True:
            if trigger[0]:
                for i in range(5):
                    self.buzz.ChangeDutyCycle(75)
                    self.buzz.ChangeFrequency(500)
                    time.sleep(0.4)
                    self.buzz.ChangeDutyCycle(0)
                    time.sleep(0.15)
                    
                trigger[0] = False
                self.buzz.ChangeDutyCycle(0)
                
