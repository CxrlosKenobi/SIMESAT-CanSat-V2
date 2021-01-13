import os
import time
import pynmea2
import serial
import string
import time
<<<<<<< HEAD

os.system("touch NEO-6M.csv")
os.system("echo >> NEO-6M.csv time,latitude,longitude,altitude")
=======
from datetime import datetime

>>>>>>> 9736f085fddd37672d90009b1caa9922289c5418

def parseGPS(str):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" % (current_time,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units)
    
        time = current_time
        lat = msg.lat,msg.lat_dir
        lon = msg.lon,msg.lon_dir
        alt =  msg.altitude,msg.altitude_units
        
        os.system("echo >> NEO-6M.csv " + "%s,%s %s,%s %s,%s %s" % (current_time,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units)
)    


serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

while True:
    str = serialPort.readline()
    parseGPS(str)
