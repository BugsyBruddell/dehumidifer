import RPi.GPIO as GPIO
import time

class RelayControl:

    def __init__(self):
        # Pin Setup
        self.RELAY_PIN_1 = 24
        self.RELAY_PIN_3 = 27
        self.RELAY_PIN_4 = 22
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RELAY_PIN_1, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.RELAY_PIN_3, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.RELAY_PIN_4, GPIO.OUT, initial=GPIO.HIGH)

    def activate_relay(self, pin):
        GPIO.output(pin, GPIO.LOW)
        time.sleep(1)
        GPIO.output(pin, GPIO.HIGH)

    def cleanup(self):
        GPIO.cleanup()
