## TO-DO LIST ##
#Remote control de Raspberry Pi Zero W sin ip publica
#Clases para cada componente.
    #Ejemplo: Class GY-91: GY-91.Accelerometer | GY-91.Pressure

import os
#Creando el requirements.txt
dir = os.system('pwd')
os.system(f'pipreqs {dir} --force')
os.system('clear')

'''
Módulo GY-91
- Acelerómetro
- Giroscopio
- Magnetómetro
- Presión
- Temperatura
'''
#Configurar desde Rasp con algunos de los siguientes:
    #https://pypi.org/project/mpu9250-jmdev/
    #http://www.pibits.net/code/raspberry-pi-and-bmp280-sensor-example.php
#MPU9250
import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ)
mpu.configure() # Apply the settings to the registers.

while True:
    print("|.....MPU9250 in 0x68 Address.....|")
    print("Accelerometer", mpu.readAccelerometerMaster())
    print("Gyroscope", mpu.readGyroscopeMaster())
    print("Magnetometer", mpu.readMagnetometerMaster())
    print("Temperature", mpu.readTemperatureMaster())
    print("\n")

    time.sleep(1)

#BMP280
import smbus
import time

bus = smbus.SMBus(1) # Get I2C bus

# BMP280 address, 0x76(118)
b1 = bus.read_i2c_block_data(0x76, 0x88, 24) # Read data back from 0x88(136), 24 bytes

# Convert the data # Temp coefficents
dig_T1 = b1[1] * 256 + b1[0]
dig_T2 = b1[3] * 256 + b1[2]
if dig_T2 > 32767 :
    dig_T2 -= 65536
    dig_T3 = b1[5] * 256 + b1[4]
if dig_T3 > 32767 :
    dig_T3 -= 65536

# Pressure coefficents
dig_P1 = b1[7] * 256 + b1[6]
dig_P2 = b1[9] * 256 + b1[8]
if dig_P2 > 32767 :
    dig_P2 -= 65536
    dig_P3 = b1[11] * 256 + b1[10]
if dig_P3 > 32767 :
    dig_P3 -= 65536
    dig_P4 = b1[13] * 256 + b1[12]
if dig_P4 > 32767 :
    dig_P4 -= 65536
    dig_P5 = b1[15] * 256 + b1[14]
if dig_P5 > 32767 :
    dig_P5 -= 65536
    dig_P6 = b1[17] * 256 + b1[16]
if dig_P6 > 32767 :
    dig_P6 -= 65536
    dig_P7 = b1[19] * 256 + b1[18]
if dig_P7 > 32767 :
    dig_P7 -= 65536
    dig_P8 = b1[21] * 256 + b1[20]
if dig_P8 > 32767 :
    dig_P8 -= 65536
    dig_P9 = b1[23] * 256 + b1[22]
if dig_P9 > 32767 :
    dig_P9 -= 65536

# BMP280 address, 0x76(118)
# Select Control measurement register, 0xF4(244)
# 0x27(39) Pressure and Temperature Oversampling rate = 1

# Normal mode
bus.write_byte_data(0x76, 0xF4, 0x27)

# BMP280 address, 0x76(118)
# Select Configuration register, 0xF5(245)
# 0xA0(00) Stand_by time = 1000 ms

bus.write_byte_data(0x76, 0xF5, 0xA0)
time.sleep(0.5)

# BMP280 address, 0x76(118)
# Read data back from 0xF7(247), 8 bytes
# Pressure MSB, Pressure LSB, Pressure xLSB, Temperature MSB, Temperature LSB
# Temperature xLSB, Humidity MSB, Humidity LSB

data = bus.read_i2c_block_data(0x76, 0xF7, 8)

# Convert pressure and temperature data to 19-bits
adc_p = ((data[0] * 65536) + (data[1] * 256) + (data[2] & 0xF0)) / 16
adc_t = ((data[3] * 65536) + (data[4] * 256) + (data[5] & 0xF0)) / 16

# Temperature offset calculations
var1 = ((adc_t) / 16384.0 - (dig_T1) / 1024.0) * (dig_T2)
var2 = (((adc_t) / 131072.0 - (dig_T1) / 8192.0) * ((adc_t)/131072.0 - (dig_T1)/8192.0)) * (dig_T3)
t_fine = (var1 + var2)
cTemp = (var1 + var2) / 5120.0
fTemp = cTemp * 1.8 + 32

# Pressure offset calculations
var1 = (t_fine / 2.0) - 64000.0
var2 = var1 * var1 * (dig_P6) / 32768.0
var2 = var2 + var1 * (dig_P5) * 2.0
var2 = (var2 / 4.0) + ((dig_P4) * 65536.0)
var1 = ((dig_P3) * var1 * var1 / 524288.0 + ( dig_P2) * var1) / 524288.0
var1 = (1.0 + var1 / 32768.0) * (dig_P1)
p = 1048576.0 - adc_p
p = (p - (var2 / 4096.0)) * 6250.0 / var1
var1 = (dig_P9) * p * p / 2147483648.0
var2 = p * (dig_P8) / 32768.0
pressure = (p + (var1 + var2 + (dig_P7)) / 16.0) / 100

# Output data to screen
print("Temp(C): %.2f C" %cTemp)
print("Temp(F): %.2f F" %fTemp)
print("Pres: %.2f hPa " %pressure)


'''
GPS Ublox NEO-6M
- Latitud, Longitud, Velocidad, Altitud
'''
#Configurar desde Rasp con alguno de los siguientes:
    #https://github.com/FranzTscharf/Python-NEO-6M-GPS-Raspberry-Pi
    #https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/
    #https://github.com/mikechan0731/GY-91_and_PiCamera_RaspberryPi
#Chequear en internet para printear también la Velocidad y la Altitud.
import serial
import time
import string
import pynmea2

while True:
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata = ser.readline()

    if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        long = newmsg.longitude
        gps = "Lat: " + str(lat) + " Long: " + str(long)
        print(gps)
#Output:
#Lat: XX.XXXXXXX  Long: XX.XXXXXXX
#Lat: XX.XXXXXXX  Long: XX.XXXXXXX


'''
GY-213 HDC1080
- Humedad
- Temperatura
'''
#Configurar desde Rasp | Posibles enlaces con info:
    #https://github.com/switchdoclabs/SDL_Pi_HDC1000
    #https://github.com/switchdoclabs/SDL_Pi_HDC1080_Python3/blob/master/testHDC1080.py

###### TESTING CODE 1 ######
#imports

import sys
import time
import datetime
import SDL_Pi_HDC1080



# Main Program
print
print ("")
print ("Test SDL_Pi_HDC1080 Version 1.1 - SwitchDoc Labs")
print ("")
print ("Sample uses 0x40 and SwitchDoc HDC1080 Breakout board ")
print ("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
print ("")

hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

print ("------------")
print ("Manfacturer ID=0x%X"% hdc1080.readManufacturerID())
print ("Device ID=0x%X"% hdc1080.readDeviceID() )
print ("Serial Number ID=0x%X"% hdc1080.readSerialNumber())
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())
# turn heater on
print ("turning Heater On")
hdc1080.turnHeaterOn()
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())
# turn heater off
print ("turning Heater Off")
hdc1080.turnHeaterOff()
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())

# change temperature resolution
print ("change temperature resolution")
hdc1080.setTemperatureResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_TEMPERATURE_RESOLUTION_11BIT)
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())
# change temperature resolution
print ("change temperature resolution")
hdc1080.setTemperatureResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())

# change humdity resolution
print ("change humidity resolution")
hdc1080.setHumidityResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_HUMIDITY_RESOLUTION_8BIT)
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())
# change humdity resolution
print ("change humidity resolution")
hdc1080.setHumidityResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_HUMIDITY_RESOLUTION_14BIT)
# read configuration register
print ("configure register = 0x%X" % hdc1080.readConfigRegister())

while True:
        print ("-----------------")
        print ("Temperature = %3.1f C" % hdc1080.readTemperature())
        print ("Humidity = %3.1f %%" % hdc1080.readHumidity())
        print ("-----------------")
        time.sleep(3.0)

'''
Placa STM32F103C8T
    - Temporizador.
    - Reloj integrado.
    - Conversor de señal analógica a digital (viceversa)
'''
#https://www.youtube.com/watch?v=a_G3WqjfPBA
#https://github.com/micropython/micropython | Micropython
#https://github.com/PhenixWen/MicroPython_STM32 | Micropython with STM32
#https://github.com/morris13579/micropython-stm32f1 | Micropython with STM32F1
    #https://github.com/rsp-esl/micropython-stm32-examples | Examples of the above

'''
Módulo LoRa RFM95W para 915MHz | Marca: HopeRF
    - Receptor y emisor de paquetes.
'''
#https://pypi.org/project/raspi-lora/
#https://pypi.org/project/pyLoraRFM9x/

from raspi_lora import LoRa, ModemConfig
#This is out callback function that runs when a message is received
def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RRSSI: {}; SNR: {}".fromat(payload.rssi, payload.snr))
#Use chip select 0. GPIO pin 17 will be used for interrupts
#The address of this device will be set to 2
lora = LoRa(0, 17, 2, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=True)
lora.on_recv = on_recv

lora.set_mode_rx()

#Send a  message to a recipient device with addres 10
#Retry sending the message twice if we don't get an ackonwledgment from the recipient
message = "Hello there!"
status = lora.send_to_wait(message, 10, retries=2)
if status is True:
    print("Message sent!")
else:
    print("No acknowledgment from recipient")
#And remember to call this as your program exits...
lora.close()

## Encrypt
from Crypto.Cipher import AES
crypto = AES.new(b"my-secret-encryption-key", AES.MODE_EAX)

lora = LoRa(0, 17, 2, crypto=crypto)



'''
Buzzer
    - Emite pitidos.
'''
#https://www.instructables.com/Raspberry-Pi-Tutorial-How-to-Use-a-Buzzer/
#https://www.youtube.com/watch?v=HOisQF-JaS0&ab_channel=AndyTran
from time import sleep
import RPi.GPIO as GPIO

#Disable warnings (optional)
GPIO.setwarnings(False)

#Select GPIO mode
GPIO.setmode(GPIO.BCM)

#Set buzzer - pin 23 as output
buzzer = 23
GPIO.setup(buzzer, GPIO.OUT)

#Run forever loop
while True:
    GPIO.output(buzzer, GPIO.HIGH)
    print("Beep")
    sleep(0.5) # Delay in seconds
    GPIO.output(buzzer, GPIO.LOW)
    print("No Beep")
    sleep(0.5)

#May the force be with you 
