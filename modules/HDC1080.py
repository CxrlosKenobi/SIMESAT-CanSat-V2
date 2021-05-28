import sys
import SDL_Pi_HDC1080
import os

class HDC:
	def __init__(self):
		sys.path.append('./SDL_Pi_HDC1080_Python3')
		self.hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

	def temp(self):
		temperature = round(self.hdc1080.readTemperature(), 3)
		return temperature

	def hum(self):
		humidity = round(self.hdc1080.readHumidity(), 3)
		return humidity
