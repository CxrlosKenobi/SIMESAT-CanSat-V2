import RPi.GPIO as GPIO
import board
import digitalio
import busio
import adafruit_rfm9x
from datetime import datetime
import datetime as dt
from time import *

from modules.BMP280 import BMP
from modules.MPU9250 import MPU
from modules.HDC1080 import HDC

MPU = MPU()
HDC = HDC()
BMP = BMP()

print(BMP.temp(3)) 
print(BMP.press(3))
print(BMP.alt())
print(BMP.comps_temp())
exit()

# MAIN PROGRAM
while True:
    try:
        # Current time
        now = datetime.now()

        # BUZZER
        # beep()
        #print("BUZZER SIGNAL READY")

        # NEO6M
        # neo6m_la, neo6m_lo = GPS()
        neo6m_la = "NO DATA"
        neo6m_lo = "NO DATA"

        #print("NEO6M SIGNAL READY")

        # BMP280
        bmp280_pr = round(BMP_press(), 2)
        bmp_al = round(BMP_alt(BMP_press()), 2)

        #print("BMP280 SIGNAL READY")
        
        payload = f"{now.strftime('%d/%m, %H:%M:%S')};{get_current_time()};{bmp280_pr},{bmp_al};{HDC.temp()},{HDC.hum()};{neo6m_la},{neo6m_lo};{MPU.accel()};{MPU.gyros()};{MPU.magnet()}"

        transmitPackets(payload)

        print("[ ok ] Payload sent...")

        sleep(1)

    except KeyboardInterrupt:
        print("[ ! ] Exiting")
        print()
        exit()
