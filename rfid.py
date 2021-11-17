import serial
import requests
import time
from env import ANIMATION_SERVER_IP


SERIAL_PORT = '/dev/ttyS0'

class RFID:
    def __init__(self):
        self.ser = serial.Serial(baudrate = 2400,
                    bytesize = serial.EIGHTBITS,
                    parity   = serial.PARITY_NONE,
                    port     = SERIAL_PORT,
                    stopbits = serial.STOPBITS_ONE,
                    timeout  = 10)
    
    def validate_rfid(self, code):
        s = code.decode("ascii")
        if (len(s) == 12) and (s[0] == "\n") and (s[11] == "\r"):
            return s[1:-1]
        else:
            return False

    def scanRFID(self, access):
#        print("Scan RFID")
        while True:
            data = self.ser.read(12)
            code = self.validate_rfid(data)

            if code in ["5300C81225", "1200926B22"]: # Rectangle or Blue
                print('Door opened') 
                access[0] = True
                code = ''
                requests.get("http://"+ANIMATION_SERVER_IP+"/door")
                time.sleep(5)
                print('Door closed')
                requests.get("http://"+ANIMATION_SERVER_IP+"/door")
            # 46003BB124 is circle
            else:
                access[0] = False
        

