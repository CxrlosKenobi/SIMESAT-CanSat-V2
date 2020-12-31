# Pasos para conectarse a Raspberry Pi Zero W

## *Primera conección*
1. ssh pi@raspberrypi.local
2. [Raspberry password]

## *Ver I2C*
- sudo i2cdetect -y 1


--

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
