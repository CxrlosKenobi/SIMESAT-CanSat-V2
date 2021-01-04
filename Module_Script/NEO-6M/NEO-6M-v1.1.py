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
        gps = "Lat: " + str(lat) + " Long: " + str(long)

        print (gps)
