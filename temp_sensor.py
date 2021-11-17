import time
import requests

class Temp_sensor:
    def __init__(self, ADC):
        self.ADC = ADC

    def start(self, trigger):
        alerted = False
        while True:
            ADC_units = self.ADC.read(0)
            temp = (ADC_units/255) *200
            requests.get('https://api.thingspeak.com/update?api_key=36WELVGBQKL6YB1D&field1='+str(temp))
            if temp > 100:
                trigger[0] = True
                print('Fire! Room temperature =', temp, 'C')
                if not alerted:
                    requests.get('http://localhost:5555/fire/'+str(temp))
                    alerted = True
                time.sleep(5)
            else:
                alerted = False
                trigger[0] = False
            time.sleep(1)

