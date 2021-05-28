from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *

from bmp280 import BMP280
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# print("""dump-calibration.py - Dumps calibration data.
# Press Ctrl+C to exit!
# """)

# Initialise the BMP280
bmp280 = BMP280(i2c_dev=SMBus(1))
bmp280.setup()

for key in dir(bmp280.calibration):
    if key.startswith('dig_'):
        value = getattr(bmp280.calibration, key)
        print('{} = {}'.format(key, value))




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

##  Accelerometer & Gyroscope
mpu.calibrateMPU6500() #  Calibrate sensors
mpu.configure() #  The calibration function rests the sensors, so you need to reconfigure them

abias = mpu.abias # Get the master accelerometer biases
abias_slave = mpu.abias_slave # Get the slave accelerometer biases
gbias = mpu.gbias # Get the master gyroscope biases
gbias_slave = mpu.gbias_slave # Get the slave gyroscope biases


##  Magnetometer
mpu.calibrateAK8963() # Calibrate sensors
mpu.configure() # The calibration function resets the sensors, so you need to reconfigure them

magScale = mpu.magScale # Get magnetometer soft iron distortion
mbias = mpu.mbias # Get magnetometer hard iron distortion
