import time
from bmp280 import BMP280
import csv

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# print("""temperature-and-pressure.py - Displays the temperature and pressure.
# Press Ctrl+C to exit!
# """)

# datetime.now().strftime('%Y-%h-%d %H:%M:%S')
# with open('BMP280.csv', 'w', newline='') as file:
# 	write = csv.writer(file)
# 	write.writerow(['Time', 'Temperature(C)', 'Pressure'])

# HH = 0
# MM = 0
# SS = 0

# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

while True:
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # if SS == 60:
	# 	MM += 1
	# 	SS = 0
    # elif MM == 60:
	# 	SS = 0
	# 	HH += 1
	# 	MM = 0

    temperature = bmp280.get_temperature()
    pressure = bmp280.get_pressure()
    # with open('BMP280.csv', 'a+', newline='') as file:
	# 	writer = csv.writer(file)
	# 	writer.writerow([current_time, bmp280.get_temperature(), bmp280.get_pressure()])

    print('{:05.2f}*C {:05.2f}hPa'.format(temperature, pressure))
    time.sleep(1)
