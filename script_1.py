## Importando librerias ##
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
from raspi_lora import LoRa, ModemConfig
from Cryto.Cipher import AES
import time import *
import os
import sys
import smbus
import string
import serial
import pynmea2
import datetime
import SDL_Pi_HDC1080
import RPi.GPIO as GPIO


#Modulo GY-91
def GY91():
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
    return 0


def BMP280():
    bus = smbus.SMBus(1) # Get I2c bus
    return 0

def main():
    print('Main...')
    return True

if __name__ == '__main__':
    main()
