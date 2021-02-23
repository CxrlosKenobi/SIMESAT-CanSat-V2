
    super(LoRaRcvCont, self).__init__(verbose)
    self.set_mode(MODE.SLEEP)
    self.set_dio_mapping([0] * 6)

def on_rx_done(self):
        print("\nReceived: ")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print(bytes(payload).decode("utf-8",'ignore'))
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
