from raspi_lora import LoRa, ModemConfig # Importing libraries

# This is our callback function that runs when a message is received
def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))


# Use chip select 0. GPIO pin 17 will be used for interrupts
# The address of this device will be set to 101
sleep() # This is just a testing line.
lora = LoRa(1, 25, 101, modem_config=ModemConfig.Bw125Cr45Sf2048, tx_power=14, acks=False)
lora.on_recv = on_recv

lora.set_mode_rx() # Turn on the "recivier mode (rx)"


# And remember to call this as your program exits...
lora.close()
