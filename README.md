# Cansat-programming [![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

*[Centro SIMES](https://aeroespacial.centrosimes.cl/)*

## Who is the team?
The first high school students, determined to build the CanSat nanosatellite. Inspired by learning, innovating and sharing knowledge, these students work together to send this nanosatellite 50 km high with a hydrogen balloon, thus capturing data and images. After 5 hours of flight, the CanSat will be received on the ground with the help of a parachute.
The work does not end here. This is only the beginning of a great journey full of feats and great achievements.

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

---
## Conceptual Map of the Proyect's flow
![image](https://raw.githubusercontent.com/CxrlosKenobi/CanSat-programming/main/assets/images/flow.png)
<br><p align="center">

## Programming's Team
[![Carlos Pinto](https://raw.githubusercontent.com/CxrlosKenobi/CanSat-programming/main/assets/images/CarlosPinto.jpg)](https://www.linkedin.com/in/carloskenobi/) | [![Rodrigo Flores](https://raw.githubusercontent.com/CxrlosKenobi/CanSat-programming/main/assets/images/RodrigoFlores.jpeg)](https://www.linkedin.com/in/rodrigo-flores-549269160/)
---|---
[Carlos Pinto ](https://www.linkedin.com/in/carloskenobi/) |[Rodrigo Flores](http://linkedin.com/in/rodrigo-flores-549269160)
