from modules import buzzer
from modules import HDC1080
from modules import NEO6M
from modules import receiver
from modules import transceiver
from data import cansat_csv

# hdc1080_csv = cansat_csv(file_name = "data/HDC-1080.csv", headers = ["Temperature", "Humidity"])
# neo6m_csv = cansat_csv(file_name = "data/NEO-6M.csv", headers = ["Latitude", "Longitude"])

while True:
    """
    # BUZZER
    buzz = Buzzer()
    buzz.beep()
    print("SENT BUZZER SIGNAL")
    """

    # HDC1080
    temperature, humidity = HDC1080()
    hdc1080_payload = str(temperature) + "|" + str(humidity)
    transmitPackets(hdc1080_payload)
    print("SENT HDC1080 SIGNAL")

    # NEO6M
    mylat, mylon = GPS()
    neo6m_payload = str(mylat) + "|" + str(mylon)
    print("SENT NEO6M SIGNAL")
    
