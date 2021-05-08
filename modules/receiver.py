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

        times = 0

        print(Fore.RED + '[ ? ] Waiting for packets ...')

        while True:
            packet = rfm9x.receive(timeout=3)

            if packet is not None:
                packet_text = str(packet, 'ascii')
                rssi = rfm9x.last_rssi
                times += 1

                print(Fore.GREEN + f'\nPackets sents: [{times}] times.')
                print(f'Received (RAW bytes): {packet}')
                print(f'Received signal strength: {rssi} dB\n' + f'\nType: {type(rssi)}\n')
                print(f'Received (ASCII): {packet_text}')


            elif packet is None:
                print(Fore.RED + '[ X ] The conection is interrupted.')

    except KeyboardInterrupt:
        print('\n[ ! ] Stopped')

    except UnicodeDecodeError:
        pass

receivePackets()
