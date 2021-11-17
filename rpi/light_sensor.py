import time
import requests

class Light_sensor:
    def __init__(self, ADC):
        self.ADC = ADC
        self.curr = 0

    def start(self):
        while True:
            ADC_units = self.ADC.read(1)

            ADC_volts = (ADC_units/255) *3.3

            # sensor eq: 40mV / lux
            lux = ADC_volts/0.04

            new = abs(255 - ADC_units) # low light -> high LED brightness
            self.ADC.write(new)

            requests.get('https://api.thingspeak.com/update?api_key=36WELVGBQKL6YB1D&field2='+str(lux))
            self.curr = new
            time.sleep(1)
