# Cansat-programming [![GitHub stars](https://img.shields.io/github/stars/Naereen/StrapDown.js.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/Cxrloskenobi/CanSat-programming/) [![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

*[Centro SIMES](https://aeroespacial.centrosimes.cl/)*

---

## RPi-GPIO usos de la libreria:
 [Library Source](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/) <br>
  **Importing libraries without bugs**
```yaml
  try:
    import RPi.GPIO as GPIO
  except RuntimeError:
    print("Error al importar GPIO. Puede que necesites permisos de adminitrador; puedes probar ejecutando el Script con "sudo")
```

  **Select IN pin:**
```yaml
  GPIO.setup(Pin, GPIO.IN)
```

  **Select OUT pin**
```yaml
  GPIO.setup(Pin, GPIO.OUT)
```

  **Read the IN value of a specific pin**
 ```yaml
 GPIO.input(Pin)
 ```

  **Give an OUT to the pin**
```yaml
GPIO.output(channel, state)
Dato -> "state" puede ser "LOW" o "HIGH"
```

**The OUT of a pin can be in colab**
```yaml
Pin_List = [11,12] # Seleciona un lista con dos Pines (11 y 12)                           
GPIO.output(Pin_List, GPIO.LOW) # Modifica los Pines 11 y 12 como "Low"             
GPIO.output(Pin_List, (GPIO.HIGH, GPIO.LOW)) # Para ambos Pines, pimero pasa por "HIGH" y luego por "LOW"
```
