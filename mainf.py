import RPi.GPIO as GPIO
import SDL_Pi_HDC1080
import sys
import os
import serial
import board
import digitalio
import busio
import adafruit_rfm9x
import csv
from datetime import datetime
import datetime as dt
from time import *

from modules.MPU9250 import MPU
from modules.HDC1080 import HDC

MPU = MPU()
HCD = HDC()

print(HDC.temp(3), HDC.hum(3))
exit()

# CSV
class cansat_csv:
    def __init__(self, file_name="", headers=[], data=[]):
        self.file_name = file_name  # File name
        self.headers = headers  # This need to be a list

    def csv_header(file_name, headers):
        with open(self.file_name, 'w', newline='') as file:
            write = csv.writer(file)
            write.writerow(self.headers)

    def csv_writer(file_name, data):
        with open(self.filename, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.data)



# MAIN PROGRAM
while True:
    try:
        # Current time
        now = datetime.now()

        # BUZZER
        # beep()
        #print("BUZZER SIGNAL READY")

        # HDC1080
        hdc1080_te, hdc1080_hu = HDC1080()

        #print("HDC1080 SIGNAL READY")

        # NEO6M
        # neo6m_la, neo6m_lo = GPS()
        neo6m_la = "NO DATA"
        neo6m_lo = "NO DATA"

        #print("NEO6M SIGNAL READY")

        # BMP280
        bmp280_pr = round(BMP_press(), 2)
        bmp_al = round(BMP_alt(BMP_press()), 2)

        #print("BMP280 SIGNAL READY")
        
        payload = f"{now.strftime('%d/%m, %H:%M:%S')};{get_current_time()};{bmp280_pr},{bmp_al};{hdc1080_te},{hdc1080_hu};{neo6m_la},{neo6m_lo};{MPU.accel()};{MPU.gyros()};{MPU.magnet()}"

        transmitPackets(payload)

        print("[ ok ] Payload sent...")

        sleep(1)

    except KeyboardInterrupt:
        print("[ ! ] Exiting")
        print()
        exit()
