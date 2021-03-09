from colorama import init, Fore, Back, Style
from numpy import pi
import board
import digitalio
import busio
import adafruit_rfm9x
import time as t
import random
import csv
init(autoreset=True)

TRAN_INTERVAL = 2.2
BAUDRATE = 1000000
Payload = 'Lat: - 33.446017833333336  |  Lon: - 70.6661478333333 | X: 95,234 | Y: 192,3392 | Z: 9234923,2 | C: 35.1'

try:
    RADIO_FREQ_MHZ = 915.0
    CS = digitalio.DigitalInOut(board.CE1)
    RESET = digitalio.DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=BAUDRATE)
    rfm9x.enable_crc = True
    rfm9x.ack_delay = .1
    rfm9x.node = 1
    rfm9x.destination = 2
    rfm9x.tx_power = 23

    while True:
        # t.sleep(1)
        rfm9x.send(bytes(Payload, "UTF-8"))
        print(Fore.GREEN + '[ ok ]' + Fore.WHITE + ' Sending packets over bytes...' + Style.RESET_ALL)
except KeyboardInterrupt:
    print('\nStopped')
finally:
    print('Finally out at exception in pass...')
    pass

