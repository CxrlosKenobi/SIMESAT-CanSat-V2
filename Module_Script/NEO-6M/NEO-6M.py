#mport serial
import time
import pynmea2
import serial
import string
#from serial import Serial
#from serial
import time



def parseGPS(str):
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" % (dt_string,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units)

serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

while True:
    str = serialPort.readline()
    parseGPS(str)