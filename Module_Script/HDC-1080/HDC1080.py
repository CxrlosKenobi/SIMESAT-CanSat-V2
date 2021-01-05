sys.path.append('./SDL_Pi_HDC1080_Python3')
from colorama impor Fore, Back, Style
import SDL_Pi_HDC1080
import datetime
import time
import csv
import sys

print ("")
print ("Read Temperature and Humidity from HDC1080 using I2C bus ")
print ("")
hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

with open('HDC-1080.csv', 'w', newline='') as file:
	write = csv.writer(file)
	write.writerow(['Time', 'Temperature', 'Humidity'])
	file.close()

while True:
	current_time = datetime.datetime.now()

	with open('HDC-1080.csv', 'a+', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([current_time, hdc1080.readTemperature(), hdc1080.readHumidity()])
		file.close()

	print (Fore.RED + "|----------------------|")
	print (Fore.WHITE + " Temperature = %3.1f C°" % hdc1080.readTemperature())
	print (Fore.WHITE + " Humidity = %3.1f %%" % hdc1080.readHumidity())
	print (Fore.RED + "|----------------------|")
	print(Style.RESET_ALL)
	time.sleep(2)
