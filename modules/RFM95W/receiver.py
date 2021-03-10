from colorama import init, Fore, Back, Style
import board
import digitalio
import busio
import adafruit_rfm9x
import time as t
import random
init(autoreset=True)

try:
    RADIO_FREQ_MHZ = 915.0
    CS = digitalio.DigitalInOut(board.CE1)
    RESET = digitalio.DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)
    rfm9x.tx_power = 23

    while True:
        packet = rfm9x.receive(timeout=1)

        if packet is not None:
            packet_text = str(packet, 'ascii')
            print('Received: {0}'.format(packet_text))
        else:
            print("No packets received...")

except KeyboardInterrupt:
    print('\n[ ! ] Stopped')
