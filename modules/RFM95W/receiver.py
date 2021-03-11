from colorama import init, Fore, Back, Style
import adafruit_rfm9x
import digitalio
import time as t
import board
import busio
init(autoreset=True)

def receivePackets():
    try:
        RADIO_FREQ_MHZ = 915.0
        CS = digitalio.DigitalInOut(board.CE1)
        RESET = digitalio.DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)
        rfm9x.tx_power = 23

        print('[ ? ] Waiting for packets ...')
        while True:
            packet = rfm9x.receive(timeout=3)

            if packet is not None:
                packet_text = str(packet, 'ascii')
                rssi = rfm9x.last_rssi
                print(f'\nReceived (RAW bytes): {packet}')
                print(f'Received signal strength: {rssi} dB\n')
                print(f'Received (ASCII): {packet_text}')

    except KeyboardInterrupt:
        print('\n[ ! ] Stopped')
receivePackets()
