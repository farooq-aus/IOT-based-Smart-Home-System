import time
import requests

class Light_sensor:
    def __init__(self, ADC):
        self.ADC = ADC
        self.curr = 0

    def start(self):
        while True:
            ADC_units = self.ADC.read(1)

            new = abs(255 - ADC_units)
            self.ADC.write(new)
            requests.get('https://api.thingspeak.com/update?api_key=36WELVGBQKL6YB1D&field2='+str(ADC_units//255))
            self.curr = new
            time.sleep(1)
