import SDL_Pi_HDC1080
import sys
import os


def HDC1080():
	sys.path.append('./SDL_Pi_HDC1080_Python3')

	hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

	temperature = round(hdc1080.readTemperature(),1)
	humidity = round(hdc1080.readHumidity(),1)

	return temperature, humidity
