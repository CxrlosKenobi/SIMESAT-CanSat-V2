# Cansat-programming [![GitHub stars](https://img.shields.io/github/stars/Naereen/StrapDown.js.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/Cxrloskenobi/CanSat-programming/) [![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

*[Centro SIMES](https://aeroespacial.centrosimes.cl/)*

---

## RPi-GPIO usos de la libreria:
 [Library Source](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/)
  **Para importar la librería sin "errores":**
```
  try:
    import RPi.GPIO as GPIO
  except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
```
  **Seleccionar Pin de entrada:**
```
  GPIO.setup(Pin, GPIO.IN)
```
  **Seleccionar Pin de salida:**
```
  GPIO.setup(Pin, GPIO.OUT)
```
