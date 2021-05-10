import RPi.GPIO as GPIO
import SDL_Pi_HDC1080
import sys
import os
import serial
import board
import digitalio
import busio
import adafruit_rfm9x
import csv
from bmp280 import BMP280
from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *

try:
    from smbus2 import SMBus  # (1)

except ImportError:
    from smbus import SMBus  # (2)


# CSV
class cansat_csv:
    def __init__(self, file_name="", headers=[], data=[]):
        self.file_name = file_name  # File name
        self.headers = headers  # This need to be a list

    def csv_header(file_name, headers):
        with open(self.file_name, 'w', newline='') as file:
            write = csv.writer(file)
            write.writerow(self.headers)

    def csv_writer(file_name, data):
        with open(self.filename, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.data)


# BMP280
# Initialize the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)


def BMP_press():  # Get pressure
    pressure = bmp280.get_pressure()

    return pressure


def BMP_alt():  # Get altitude
    baseline_values = []
    baseline_size = 100

    # Calibration with 100 sampling
    for i in range(baseline_size):
        baseline_values.append(pressure)

    baseline = sum(baseline_values[:-25]) / len(baseline_values[:-25])

    altitude = bmp280.get_altitude(qnh=baseline)

    return altitude


# MPU9250
"""
mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68,  # In 0x68 Address
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ)
mpu.configure()

##  Accelerometer & Gyroscope
mpu.calibrateMPU6500()  # Calibrate sensors
mpu.configure()  # The calibration function rests the sensors, so you need to reconfigure them

abias = mpu.abias  # Get the master accelerometer biases
abias_slave = mpu.abias_slave  # Get the slave accelerometer biases
gbias = mpu.gbias  # Get the master gyroscope biases
gbias_slave = mpu.gbias_slave  # Get the slave gyroscope biases

# Magnetometer
mpu.calibrateAK8963()  # Calibrate sensors
# The calibration function resets the sensors, so you need to reconfigure them
mpu.configure()

magScale = mpu.magScale  # Get magnetometer soft iron distortion
mbias = mpu.mbias  # Get magnetometer hard iron distortion


def MPU9250_accel():
    accelerometer = mpu.readAccelerometerMaster()

    # Accelerometer sorted values if [0][1][2] are X,Y,Z axis respectively
    xA = round(accelerometer[0], 6)
    yA = round(accelerometer[1], 6)
    zA = round(accelerometer[2], 6)
    outA = [xA, yA, zA]

    return outA


def MPU9250_gyros():
    gyroscope = mpu.readGyroscopeMaster()

    # Gyroscope sorted values if [0][1][2] are X,Y,Z axis respectively
    xG = round(gyroscope[0], 6)
    yG = round(gyroscope[1], 6)
    zG = round(gyroscope[2], 6)
    outG = [xG, yG, zG]

    return outG


def MPU9250_magnet():
    magnetometer = mpu.readMagnetometerMaster()

    # Magnetometer sorted values if [0][1][2] are X,Y,Z axis respectively
    xM = round(magnetometer[0], 6)
    yM = round(magnetometer[1], 6)
    zM = round(magnetometer[2], 6)
    outM = [xM, yM, zM]

    return outM


# HDC1080
def HDC1080():
    sys.path.append('./SDL_Pi_HDC1080_Python3')

    hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

    temperature = round(hdc1080.readTemperature(), 1)
    humidity = round(hdc1080.readHumidity(), 1)

    return temperature, humidity
"""

# Get current time
def get_current_time():
    now = dt.datetime.now()
    total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)

    return total_time


# NEO6M
'''
#choose your com port on which you connected your neo 6m GPS
mport = "/dev/ttyAMA0"            #for Raspberry Pi pins
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

    return mylat, mylon
'''

# TRANSCEIVER
# init(autoreset=True)


def transmitPackets(Payload):
    if len(Payload) > 252:
        return "You can only send a message up to 252 bytes in length at a time!"

    BAUDRATE = 1000000  # min 1Mhz; max 10MHz
    RADIO_FREQ_MHZ = 915.0  # 915 Mhz
    CS = digitalio.DigitalInOut(board.CE1)
    RESET = digitalio.DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    rfm9x = adafruit_rfm9x.RFM9x(
        spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=BAUDRATE)
    rfm9x.tx_power = 23  # min 5dB; max 23dB
    #rfm9x.enable_crc = True
    #rfm9x.ack_delay = .1
    #rfm9x.node = 1
    #rfm9x.destination = 2

    rfm9x.send(bytes(Payload, "UTF-8"))

    return "[ ok ] Sending packages"


# BUZZER
"""
GPIO.cleanup()

pin = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, 300)

def beep():
    GPIO.setwarnings(False)
    GPIO.output(pin, True)
    p.start(0)
    p.ChangeDutyCycle(100)
    p.ChangeFrequency(100)
    sleep(0.5)
    p.stop()

    GPIO.output(pin, False)
    sleep(2)

    GPIO.cleanup()
"""

# MAIN PROGRAM
while True:
    # BUZZER
    # beep()
    #print("BUZZER SIGNAL READY")

    # HDC1080
    hdc1080_te, hdc1080_hu = HDC1080()

    print("HDC1080 SIGNAL READY")

    # NEO6M
    # neo6m_la, neo6m_lo = GPS()
    neo_la = "NO DATA"
    neo_lo = "NO DATA"

    print("NEO6M SIGNAL READY")

    # BMP280
    bmp280_pr = BMP_press()
    bmp_al = BMP_alt()

    print("BMP280 SIGNAL READY")

    # MPU9250
    mpu9250_ac = MPU9250_accel()
    mpu9250_gy = MPU9250_gyros()
    mpu9250_ma = MPU9250_magnet()

    mpu9250_ac = "NULL"
    mpu9250_gy = "NULL"
    mpu9250_ma = "NULL"

    print("MPU9250 SIGNAL READY")

    payload = f"{now.strftime('%d/%m, %H:%M:%S')};{get_current_time()};{bmp280_pr},{bmp_al};{hdc1080_te},{hdc1080_hu};{neo6m_la},{neo6m_lo};{mpu9250_ac};{mpu9250_gy};{mpu9250_ma}"

    transmitPackets(payload)
