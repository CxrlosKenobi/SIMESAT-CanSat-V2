from colorama import init, Fore, Back, Style
from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *
from datetime import *
from time import *
import csv
import os

os.system('clear')
counter = 0
hr = 0
min = 0
sec = 0

# Script for have a time's follow up
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

with open('GY-91.csv', 'w', newline='') as file:
	write = csv.writer(file)
	write.writerow(['Time','Acelerometer','Gyroscope','Magnetometer'])

while True:
	if sec == 60:
		min += 1
		sec = 0
	elif min == 60:
		hr += 1
		min = 0

	watch = (f'{hr}:{min}:{sec}')

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

	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")

	with open('GY-91.csv', 'a+', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([current_time, outA, outG, outM])

	try:
        	print('\t#.....MPU9250 in 0x68 Address at ' + Fore.GREEN + f'{watch}' + Style.RESET_ALL + '.....#\n')
	        print(Back.WHITE + Fore.BLACK + "Accelerometer:   " + str(outA) + Style.RESET_ALL)
	        print(Back.WHITE + Fore.BLACK + "Gyroscope:       " + str(outG) + Style.RESET_ALL)
	        print(Back.WHITE + Fore.BLACK + "Magnetometer:    " + str(outM) + Style.RESET_ALL)
	        print(Back.WHITE + Fore.BLACK + "(C) Temperature: " + str(round(temperature, 6)) + Style.RESET_ALL )
	        print('\n')
	        sec += 1
	        sleep(1)
	except KeyboardInterrupt:
        	print(Fore.RED + '\nStopped of collecting data from MPU9250 at the '+ Fore.GREEN + f'{counter}' + Fore.RED + 'th collection\n' + Style.RESET_ALL)
        	exit()
