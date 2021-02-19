# raspi-lora documentation: https://pypi.org/project/raspi-lora/

from raspi_lora import LoRa, ModemConfig

# This is our callback function that runs when a message is received
def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))


lora = LoRa(0, 17, 2, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=True) #GPIO
lora.on_recv = on_recv

lora.set_mode_tx()
while True:
    message = "Hello there!"
    status = lora.send_to_wait(message, 10, retries=2)

    if status is True:
        print("Message sent!")
    else:
        print("No acknowledgment from recipient")

    lora.close()
