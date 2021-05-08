import sys
from colorama import Fore, Back, Style
import SDL_Pi_HDC1080
from datetime import *
import time
import csv
import sys
import os
sys.path.append('./SDL_Pi_HDC1080_Python3')

hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

temperature = round(hdc1080.readTemperature(),1)
humidity = round(hdc1080.readHumidity(),1)

writer = csv.writer(file)
writer.writerow([current_time, hdc1080.readTemperature(), hdc1080.readHumidity()])
