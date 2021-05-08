from colorama import init, Fore, Back, Style
import adafruit_rfm9x
import digitalio
import time as t
import board
import busio
init(autoreset=True)

def receivePackets():
    RADIO_FREQ_MHZ = 915.0
    CS = digitalio.DigitalInOut(board.CE1)
    RESET = digitalio.DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)
    rfm9x.tx_power = 23

    times = 0

    packet = rfm9x.receive(timeout=3)

    if packet is not None:
        packet_text = str(packet, 'ascii')
        rssi = rfm9x.last_rssi
        times += 1

        return packet, rssi, packet_text # RAW bytes, signal strength, ASCII

    elif packet is None:
        return '[ ! ] The conection is interrupted.'

