import SDL_Pi_HDC1080
import sys
import os
import serial
import board
import digitalio
import busio
import adafruit_rfm9x

#################################################################################################
def HDC1080():
	sys.path.append('./SDL_Pi_HDC1080_Python3')

	hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

	temperature = round(hdc1080.readTemperature(),1)
	humidity = round(hdc1080.readHumidity(),1)

	return temperature, humidity

#################################################################################################

mport = '/dev/ttyAMA0'                     #choose your com port on which you connected your neo 6m GPS
#mport = "/dev/ttyAMA0"            #for Raspberry Pi pins
#mport = "/dev/ttyUSB0"            #for Raspberry Pi USB

def parseGPS(data):
    if data[0:6] == "$GPGGA":
        s = data.split(",")
        if s[7] == '0' or s[7]=='00':
            print ("no satellite data available")
            return
        time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
        lat = decode(s[2])
        lon = decode(s[4])
        return lat,lon

def decode(coord):
    l = list(coord)
    for i in range(0,len(l)-1):
            if l[i] == "." :
                    break
    base = l[0:i-2]
    degi = l[i-2:i]
    degd = l[i+1:]
    baseint = int("".join(base))
    degiint = int("".join(degi))
    degdint = float("".join(degd))
    degdint = degdint / (10**len(degd))
    degs = degiint + degdint
    full = float(baseint) + (degs/60)

    return full


def GPS():
    ser = serial.Serial(mport,9600,timeout = 2)

    dat = ser.readline().decode("UTF-4")
	
    mylat,mylon = parseGPS(dat)

    return (str(mylat) + "|" + str(mylon))
######################################################################################################
# init(autoreset=True)

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
##############################################################################################################
'''
from modules import HDC1080
from modules import NEO6M
from modules import receiver
from modules import transceiver
from data import cansat_csv

# hdc1080_csv = cansat_csv(file_name = "data/HDC-1080.csv", headers = ["Temperature", "Humidity"])
# neo6m_csv = cansat_csv(file_name = "data/NEO-6M.csv", headers = ["Latitude", "Longitude"])
'''

while True:
    """
    # BUZZER
    buzz = Buzzer()
    buzz.beep()
    print("SENT BUZZER SIGNAL")
    """

    # HDC1080
    temperature, humidity = HDC1080()
    hdc1080_payload = str(temperature) + "|" + str(humidity)
    transmitPackets(hdc1080_payload)
    print("SENT HDC1080 SIGNAL")

    # NEO6M
    # mylat, mylon = GPS()
    neo6m_payload = GPS()
    print("SENT NEO6M SIGNAL")
