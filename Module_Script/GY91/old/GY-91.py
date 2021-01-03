from mpu9250_jmdev.mpu_9250 import MPU9250
from colorama import init, Fore, Back
from mpu9250_jmdev.registers import *
from time import *

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
	temperature = mpu.readTemperatureMaster()

	try:

		#print("\t|.....MPU9250 in 0x68 Address.....|\n")

		#print("Accelerometer", mpu.readAccelerometerMaster())

		split = str(mpu.readAccelerometerMaster()).split(",")

		for i in split:
			for x in range(0, 10):
				if x == 9:
					print(i)
			print()

		print("%s," % i,end="")

		#print("Gyroscope", mpu.readGyroscopeMaster())
		#print("Magnetometer", mpu.readMagnetometerMaster())
		#print(Back.WHITE + Fore.MAGENTA + "(C) Temperature: " + str(round(temperature, 4)))
		#print('\n')

    	current_time = datetime.datetime.now()

        with open('/Data/_Data.csv', 'w', newline='') as file:
            fieldnames = ['Time','Accelerometer', 'Gyroscope', 'Magnetometer', 'Temperature']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
           	writer.writerow({'Time': current_time, 'Accelerometer': mpu.readAccelerometerMaster(),
            'Gyroscope': mpu.readMagnetometerMaster(), 'Magnetometer': mpu.readMagnetometerMaster(), 
            'Temperature': str(round(temperature, 4))})

		sleep(1)

	except KeyboardInterrupt:
		print('\nStopped\n')
		exit()
