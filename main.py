import datetime as dt
from time import *

from modules.lora import transmitPackets
from modules.BMP280 import BMP
from modules.MPU9250 import MPU
from modules.HDC1080 import HDC

MPU = MPU() # MPU-9250
HDC = HDC() # HDC-1080
BMP = BMP() # BMP-280

def get_current_time():
    now = dt.datetime.now()
    total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)

    return total_time

def main():
    NEO_lo = "NO DATA"
    NEO_la = "NO DATA"
    # NEO_al = "NO DATA"

    now = dt.datetime.now()
    payload = f"{now.strftime('%d/%m, %H:%M:%S')};{get_current_time()};{BMP.press(4)},{BMP.alt(4)};{HDC.temp(4)},{HDC.hum(4)};{NEO_la},{NEO_lo};{MPU.accel()};{MPU.gyros()};{MPU.magnet()}"

    transmitPackets(payload)
    print("[ OK ] Payload sent ...")

    sleep(1)


if __name__ == '__main__':
    while True:
        try:
            main()
        except OSError:
            print('\n[ ! ] Warning: OSError, running anyways :).\n')
        except KeyboardInterrupt:
            print("\n[ ! ] Exiting\n")
            exit()
