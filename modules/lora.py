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

def transmitPackets(Payload):
    if len(Payload) > 252:
        return "You can only send a message up to 252 bytes in length at a time!"

    BAUDRATE = 1000000 # min 1Mhz; max 10MHz
    RADIO_FREQ_MHZ = 915.0 # 915 Mhz
    CS = digitalio.DigitalInOut(board.CE1)
    RESET = digitalio.DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=BAUDRATE)
    rfm9x.tx_power = 23 # min 5dB; max 23dB
    #rfm9x.enable_crc = True
    #rfm9x.ack_delay = .1
    #rfm9x.node = 1
    #rfm9x.destination = 2

    rfm9x.send(bytes(Payload, "UTF-8"))

    return "[ ok ] Sending packages"
