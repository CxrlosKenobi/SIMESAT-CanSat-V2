import time
import csv
import os
import random
from datetime import datetime, date
import sqlite3
from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.registers import *
from colorama import init, Fore, Back, Style

conn = sqlite3.connect('gy91.db')
cur = conn.cursor()

print(Fore.GREEN  + '[ ok ] ' + Fore.WHITE + 'Succesfully Connected to DB' + Style.RESET_ALL + '\n')

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

try:
	while True:
	    now = datetime.now()
	    current_time = now.strftime('%H:%M:%S')
	    gyroscope = mpu.readGyroscopeMaster()

	    #Gyroscope sorted values if [0][1][2] are X,Y,Z axis respectively
	    xG = round(gyroscope[0], 6)
	    yG = round(gyroscope[1], 6)
	    zG = round(gyroscope[2], 6)
	    outG = [xG, yG, zG]


	    # Add data to database
	    cur.execute("INSERT INTO Gyroscope (time, xG, yG, zG) VALUES(?,?,?,?)", (date.today(), xG, yG, zG))
	    print(Fore.GREEN + '[ ok ]' + Fore.WHITE + ' Data succesful added to db' + Style.RESET_ALL)

	    time.sleep(1)

	    conn.commit()

except KeyboardInterrupt:
    conn.commit()
    cur.close()
    print('\n' + '[ bye ]')

