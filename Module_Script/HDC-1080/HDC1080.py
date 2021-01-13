from colorama import Fore, Back, Style
import SDL_Pi_HDC1080
import datetime
import time
import csv
import sys
import os
sys.path.append('./SDL_Pi_HDC1080_Python3')
os.system('clear')

print ("\nRead Temperature and Humidity from HDC1080 using I2C bus.\n")
hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

with open('HDC-1080.csv', 'w', newline='') as file:
	write = csv.writer(file)
	write.writerow(['Time', 'Temperature(C)', 'Humidity'])

while True:
	current_time = datetime.datetime.now()
	with open('HDC-1080.csv', 'a+', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([current_time, hdc1080.readTemperature(), hdc1080.readHumidity()])

	print (Fore.RED + f"|-------{now.strftime('%H:%M:%S')}-------|")
	print (Fore.WHITE + f'Temperature = {hdc1080.readTemperature()} C°')
	print (Fore.WHITE + f'Humidity = {hdc1080.readHumidity()}')
	print (Fore.RED +  "|----------------------|" + Style.RESET_ALL)
	time.sleep(5)
