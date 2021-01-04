import pynmea2
import serial

# First Option
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

        print(gps)

#return gps
"""
# Second Option
def parseGPS(str):
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" % (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units)

serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

while True:
    str = serialPort.readline()
    parseGPS(str)

# Third Option
port = "/dev/ttyAMA0"

ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

while 1:
    try:
        data = ser.readline()
    except:
        print("loading")

    if data[0:6] == '$GPGGA':
        msg = pynmea2.parse(data)
        latval = msg.lat
        concatlat = "lat:" + str(latval)
        print(concatlat)
        longval = msg.lon
        concatlong = "long:" + str(longval)
        print(concatlong, concatlat)
"""
