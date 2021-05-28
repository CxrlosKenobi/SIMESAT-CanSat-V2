from datetime import datetime
import datetime as dt
from time import *

from modules.transceiver import transmitPackets
from modules.BMP280 import BMP
from modules.MPU9250 import MPU
from modules.HDC1080 import HDC

MPU = MPU() # MPU-9250
HDC = HDC() # HDC-1080
BMP = BMP() # BMP-280

while True:
    try:
        NEO_lo = "NO DATA"
        NEO_la = "NO DATA"

        now = datetime.now() # Current time
        payload = f"{now.strftime('%d/%m, %H:%M:%S')};{get_current_time()};{BMP.press(4)},{BMP.alt(4)};{HDC.temp()},{HDC.hum()};{NEO_la},{NEO_lo};{MPU.accel()};{MPU.gyros()};{MPU.magnet()}"

        transmitPackets(payload)

        print("[ ok ] Payload sent...")

        sleep(1)

    except KeyboardInterrupt:
        print("[ ! ] Exiting\n")
        exit()
