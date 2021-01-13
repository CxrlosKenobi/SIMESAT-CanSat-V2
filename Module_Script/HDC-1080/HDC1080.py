<<<<<<< HEAD
<<<<<<< HEAD
import sys
sys.path.append('./SDL_Pi_HDC1080_Python3')
=======
>>>>>>> 4cccd5e752d6627fa78766bcf9499eebd7b1f696
=======
>>>>>>> 9736f085fddd37672d90009b1caa9922289c5418
from colorama import Fore, Back, Style
import SDL_Pi_HDC1080
from datetime import * 
import time
import csv
<<<<<<< HEAD
<<<<<<< HEAD

print ("")
print ("Reading Temperature and Humidity from HDC1080 Module ")
print ("")
=======
import sys
import os
sys.path.append('./SDL_Pi_HDC1080_Python3')
os.system('clear')

print ("\nRead Temperature and Humidity from HDC1080 using I2C bus.\n")
>>>>>>> 4cccd5e752d6627fa78766bcf9499eebd7b1f696
=======
import sys
import os
sys.path.append('./SDL_Pi_HDC1080_Python3')
os.system('clear')


print ("\nRead Temperature and Humidity from HDC1080 using I2C bus.\n")
>>>>>>> 9736f085fddd37672d90009b1caa9922289c5418
hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

with open('HDC-1080.csv', 'w', newline='') as file:
	write = csv.writer(file)
	write.writerow(['Time', 'Temperature(C)', 'Humidity'])
<<<<<<< HEAD

while True:
	current_time = datetime.datetime.now()
=======
HH = 0
MM = 0
SS = 0
while True:
	current_time = datetime.now()
	if SS == 60:
		MM += 1
		SS = 0
	elif MM == 60:
		SS = 0
		HH += 1
		MM = 0

>>>>>>> 9736f085fddd37672d90009b1caa9922289c5418
	with open('HDC-1080.csv', 'a+', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([current_time, hdc1080.readTemperature(), hdc1080.readHumidity()])

<<<<<<< HEAD
	print (Fore.RED + f"|-------{now.strftime('%H:%M:%S')}-------|")
	print (Fore.WHITE + f'Temperature = {hdc1080.readTemperature()} C°')
	print (Fore.WHITE + f'Humidity = {hdc1080.readHumidity()}')
	print (Fore.RED +  "|----------------------|" + Style.RESET_ALL)
	time.sleep(5)
=======
	print (Fore.RED + "|-------" + Fore.WHITE + f'{HH}:{MM}:{SS}' + Fore.RED + "-------|")
	print (Fore.WHITE + f'Temperature = {hdc1080.readTemperature()} C°')
	print (Fore.WHITE + f'Humidity = {hdc1080.readHumidity()}')
	print (Fore.RED + "|----------------------|\n\n" + Style.RESET_ALL)

	SS += 5
	time.sleep(5)

>>>>>>> 9736f085fddd37672d90009b1caa9922289c5418
