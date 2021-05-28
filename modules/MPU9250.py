from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *


class MPU9250:
	def __init__(self):
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

	def accel(self):
		accelerometer = mpu.readAccelerometerMaster()

		#Accelerometer sorted values if [0][1][2] are X,Y,Z axis respectively
		xA = round(accelerometer[0], 6)
		yA = round(accelerometer[1], 6)
		zA = round(accelerometer[2], 6)
		outA = [xA, yA, zA]

		return outA

	def gyros(self):
		gyroscope = mpu.readGyroscopeMaster()

		#Gyroscope sorted values if [0][1][2] are X,Y,Z axis respectively
		xG = round(gyroscope[0], 6)
		yG = round(gyroscope[1], 6)
		zG = round(gyroscope[2], 6)
		outG = [xG, yG, zG]

		return outG

	def magnet(self):
		magnetometer = mpu.readMagnetometerMaster()

		#Magnetometer sorted values if [0][1][2] are X,Y,Z axis respectively
		xM = round(magnetometer[0], 6)
		yM = round(magnetometer[1], 6)
		zM = round(magnetometer[2], 6)
		outM = [xM, yM, zM]

		return outM
