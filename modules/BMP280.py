from bmp280 import BMP280
from subprocess import PIPE, Popen

try:
    from smbus2 import SMBus

except ImportError:
    from smbus import SMBus


class BMP:
    def __init__(self):
        # Initialize the BMP280
        self.bus = SMBus(1)
        self.bmp280 = BMP280(i2c_dev=self.bus)

    def temp(self, decimal):
        temperature = round(self.bmp280.get_temperature(), decimal)
        return temperature

    def press(self, decimal):
        pressure = round(self.bmp280.get_pressure(), decimal)
        return pressure

    def alt(self):
        baseline_values = []
        baseline_size = 100

        # Calibration with 100 sampling
        for i in range(baseline_size):
            baseline_values.append(self.bmp280.get_pressure())

        baseline = sum(baseline_values[:-25]) / len(baseline_values[:-25])
        altitude = self.bmp280.get_altitude(qnh=baseline)
        return altitude

    # Gets the CPU temperature in degrees C
    def get_cpu_temperature(self):
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        output, _error = process.communicate()
        #return float(output[output.index('=') + 1:output.rindex("'")])
        return output

    def comps_temp(self):
        factor = 1.2  # Smaller numbers adjust temp down, vice versa
        smooth_size = 10  # Dampens jitter due to rapid CPU temp changes
        cpu_temps = []
        cpu_temp = self.get_cpu_temperature()
        cpu_temps.append(cpu_temp)

        if len(cpu_temps) > smooth_size:
            cpu_temps = cpu_temps[1:]

        smoothed_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
        raw_temp = self.bmp280.get_temperature()
        comp_temp = raw_temp - ((smoothed_cpu_temp - raw_temp) / factor)
        # print("Compensated temperature: {:05.2f} *C".format(comp_temp))
        return comp_temp
