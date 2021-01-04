## Importando librerias ##
from mpu9250_jmdev.mpu_9250 import MPU9250
from raspi_lora import LoRa, ModemConfig
from mpu9250_jmdev.registers import *
import matplotlib.pyplot as plt
from Cryto.Cipher import AES
import RPi.GPIO as GPIO
import SDL_Pi_HDC1080
import numpy as np
from time import *
import datetime
import pynmea2
import string
import serial
import smbus
import sys
import csv
import os

def plotter(type, data1, data2, data3):
    # Can be plot, bar, hist, pie...
    if type == 'plot':
        x = []
        y = []

        plt.xlabel('lala')
        plt.plot(x, y, linestyle=':', color='violet', alpha=0.9)
        #plt.show()
        plt.savefig('plot.png')
        return 0
    elif type == 'bar':
        return 0
    elif type == 'hist':

        return 0
    elif type == 'pie':
        fig1, ax1 = plt.subplots()
        labels = ['a', 'b', 'c']
        sizes = [3, 6, 8]
        colors = ['red', 'blue', 'violet']
        explode = (0.05, 0.05, 0.05)

        ax1.pie(sizes, colors = colors, labels = labels, explode = explode, autopct='%1.1f%%', startangle=90)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        ax1.axis = ('equal')
        plt.tight_layout()
        plt.show()
        plt.savefig('piechart.png')
        return 0

    return 0

def logs(): # The function is incorpore to each module function #
    	#### IN THE LOOP ####
	current_time = datetime.datetime.now()

    with open('/Data/_Data.csv', 'w', newline='') as file:
        fieldnames = ['Time', 'Data']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
       	writer.writerow({'Time': current_time, 'Data': "MODULE OUTPUT"})

     # En caso de que el modulo posea mas de una salida de datos, se puede aumentar el numero de "fieldnames" y luego especificar los datos dentro del diccionario.

#Modulo GY-91
def GY91():
    '''
    from time import *
    from colorama import init, Fore, Back, Style
    from mpu9250_jmdev.registers import *
    from mpu9250_jmdev.mpu_9250 import MPU9250
    import os
    '''
    os.system('clear')
    counter = 0
    hr = 0
    min = 0
    sec = 0

    # Script for have a time's follow up
    sec += 1
    if sec == 60:
        min += 1
        sec = 0
    if min == 60:
        hr += 1
        min = 0

    mpu = MPU9250(
        address_ak=AK8963_ADDRESS,
        address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
        address_mpu_slave=None,
        bus=1,
        gfs=GFS_1000,
        afs=AFS_8G,
        mfs=AK8963_BIT_16,
        mode=AK8963_MODE_C100HZ)
    mpu.configure()

    while True:
        watch = f'{hr}:{min}:{sec}'

        accelerometer = mpu.readAccelerometerMaster()
        gyroscope = mpu.readGyroscopeMaster()
        magnetometer = mpu.readMagnetometerMaster()
        temperature = mpu.readTemperatureMaster()

        #Accelerometer sorted values if [0][1][2] are X,Y,Z axis respectively
        xA = round(accelerometer[0], 6)
        yA = round(accelerometer[1], 6)
        zA = round(accelerometer[2], 6)
        outA = [xA, yA, zA]

        #Gyroscope sorted values if [0][1][2] are X,Y,Z axis respectively
        xG = round(gyroscope[0], 6)
        yG = round(gyroscope[1], 6)
        zG = round(gyroscope[2], 6)
        outG = [xG, yG, zG]

        #Magnetometer sorted values if [0][1][2] are X,Y,Z axis respectively
        xM = round(magnetometer[0], 6)
        yM = round(magnetometer[1], 6)
        zM = round(magnetometer[2], 6)
        outM = [xM, yM, zM]

        try:
            print('\t#.....MPU9250 in 0x68 Address at ' + Fore.GREEN + f'{watch}' + Style.RESET_ALL + '.....#\n')
    		print(Back.WHITE + Fore.BLACK + "Accelerometer:   " + str(outA) + Style.RESET_ALL)
    		print(Back.WHITE + Fore.BLACK + "Gyroscope:       " + str(outG) + Style.RESET_ALL)
    		print(Back.WHITE + Fore.BLACK + "Magnetometer:    " + str(outM) + Style.RESET_ALL)
    		print(Back.WHITE + Fore.BLACK + "(C) Temperature: " + str(round(temperature, 6)) + Style.RESET_ALL )
    		print('\n')
            counter += 1
    		sleep(1)
        except KeyboardInterrupt:
    		print(Fore.RED + '\nStopped of collecting data from MPU9250 at the '+ Fore.GREEN + f'{counter}' + Fore.RED + 'th collection\n' + Style.RESET_ALL)
    		exit()


#Modulo BMP280
def BMP280():
    bus = smbus.SMBus(1) # Get I2c bus
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
    sleep(0.5)

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
    out_data =
    print("Temp(C): %.2f C" %cTemp)
    print("Temp(F): %.2f F" %fTemp)
    print("Pres: %.2f hPa " %pressure)

#Modulo GPS Ublox NEO-6M
def NEO_6M():
    while True:
        port = '/dev/ttyAMA0'
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata = ser.readline()

        if newdata[0:6] == "$GPRMC":
            newmsg = pynmea2.parse(newdata)
            lat = newmsg.latitude
            long = newmsg.longitude
            gps = "Lat: " + str(lat) + " Long: " + str(long

        #Output:
        #Lat: XX.XXXXXXX  Long: XX.XXXXXXX
        #Lat: XX.XXXXXXX  Long: XX.XXXXXXX
    return gps

#Modulo GY-213 HDC1080
def GY213():
    print ("")
    print ("Test SDL_Pi_HDC1080 Version 1.1 - SwitchDoc Labs")
    print ("")
    print ("Sample uses 0x40 and SwitchDoc HDC1080 Breakout board ")
    print ("Program Started at:"+ strftime("%Y-%m-%d %H:%M:%S"))
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
        sleep(3.0)

#Modulo LoRa HopeRF
def loraFunction():
    def on_Recv(payload):
            print("From:", payload.header_from)
            print("Received:", payload.message)
            print("RRSSI: {}; SNR: {}".format(payload.rssi, payload.snr))

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

    crypto = AES.new(b'my-secret-encryption-key', AES.MODE_EAX)
    lora = LoRa(0, 17, 2, crypto=crypto)

#Buzzer script
def buzzer():
    #Disable warnings (optional)
    GPIO.setwarnings(False)

    #Select GPIO mode
    GPIO.setmode(GPIO.BCM)

    #Set buzzer - pin 23 as Output
    pinBuzzer = 23
    GPIO.setup(pinBuzzer, GPIO.OUT)

    while True:
        GPIO.output(pinBuzzer, GPIO.HIGH)
        print('Beep')
        sleep(0.5) # Delay in seconds
        GPIO.output(pinBuzzer, GPIO.LOW)
        print('No Beep')
        sleep(0.5)


def main():
    print('Just the main function')
    return 0


if __name__ == '__main__':
    main()
