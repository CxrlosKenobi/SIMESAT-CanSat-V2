# Cansat-programming [![GitHub stars](https://img.shields.io/github/stars/Naereen/StrapDown.js.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/Cxrloskenobi/CanSat-programming/) [![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

*[Centro SIMES](https://aeroespacial.centrosimes.cl/)*

---

## RPi-GPIO usos de la libreria:
 [Library Source](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/) <br>
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

  **Leer un valor de entrada de un Pin específico:**
 ```
 GPIO.input(Pin)
 ```

  **Entregar un salida al Pin:**
```
GPIO.output(channel, state)
Dato -> "state" puede ser "LOW" o "HIGH"
```

**La salida de un Pin se puede trabajar en conjunto:**
```
Pin_List = [11,12] # Seleciona un lista con dos Pines (11 y 12)                           
GPIO.output(Pin_List, GPIO.LOW) # Modifica los Pines 11 y 12 como "Low"             
GPIO.output(Pin_List, (GPIO.HIGH, GPIO.LOW)) # Para ambos Pines, pimero pasa por "HIGH" y luego por "LOW"
```
