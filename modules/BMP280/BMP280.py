from bmp280 import BMP280

try:
    from smbus2 import SMBus

except ImportError:
    from smbus import SMBus

# Initialize the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

def BMP_temp():
    temperature = bmp280.get_temperature()

    return temperature

def BMP_press():
    pressure = bmp280.get_pressure()

    return pressure

def BMP_alt():
    baseline_values = []
    baseline_size = 100

    # Calibration with 100 sampling
    for i in range(baseline_size):
        baseline_values.append(pressure)

    baseline = sum(baseline_values[:-25]) / len(baseline_values[:-25])

    altitude = bmp280.get_altitude(qnh=baseline)

    return altitude
