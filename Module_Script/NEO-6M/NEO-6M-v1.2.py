import pynmea2
import serial

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
