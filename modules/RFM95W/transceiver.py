from colorama import init, Fore, Back, Style
import board
import digitalio
import busio
import adafruit_rfm9x
init(autoreset=True)

def transmitPackets(Payload):
    if len(Payload) > 252:
        return "You can only send a message up to 252 bytes in length at a time!"

    BAUDRATE = 1000000 # min 1Mhz; max 10MHz
    RADIO_FREQ_MHZ = 915.0 # 915 Mhz
    CS = digitalio.DigitalInOut(board.CE1)
    RESET = digitalio.DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=BAUDRATE)
        rfm9x.tx_power = 23 # min 5dB; max 23dB
        # rfm9x.enable_crc = True
        # rfm9x.ack_delay = .1
        # rfm9x.node = 1
        # rfm9x.destination = 2

	rfm9x.send(bytes(Payload, "UTF-8"))
        return print(Fore.GREEN + '[ ok ]' + Fore.WHITE + ' Transmitting packets...' + Style.RESET_ALL)

    except KeyboardInterrupt:
        print('\n[ ! ] Stopped')

while True:
	transmitPackets(Payload='Eh, futuro; Code; Carlos Adonis, Vaso Mouse, Raton')
