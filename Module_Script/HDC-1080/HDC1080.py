import csv
import datetime
import sys
sys.path.append('./SDL_Pi_HDC1080_Python3')
import time
import SDL_Pi_HDC1080

# Main Program
print ("")
print ("Read Temperature and Humidity from HDC1080 using I2C bus ")
print ("")
hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

while True:
	current_time = datetime.datetime.now()

	with open('HDC-1080.csv', 'a', newline='') as file:
		fieldnames = ['Time', 'Temperature', 'Humidity']
		writer = csv.DictWriter(file, fieldnames=fieldnames)

		writer.writeheader()
		writer.writerow({'Time': current_time, 'Temperature': hdc1080.readTemperature(), 'Humidity': hdc1080.readHumidity()})

	print ("-----------------")
	print ("Temperature = %3.1f C" % hdc1080.readTemperature())
	print ("Humidity = %3.1f %%" % hdc1080.readHumidity())
	print ("-----------------")
	time.sleep(2)
