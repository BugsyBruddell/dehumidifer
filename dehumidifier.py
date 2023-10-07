import Adafruit_DHT
import time
import RPi.GPIO as GPIO

# Set the GPIO pin where the DHT22 sensor is connected
DHT_PIN = 23
RELAY_PIN_1 = 24  # GPIO pin for relay 1 (power supply)
RELAY_PIN_3 = 27  # GPIO pin for relay 3 (power button)
RELAY_PIN_4 = 22  # GPIO pin for relay 4 (indicator light)
SENSOR_TYPE = Adafruit_DHT.DHT22

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN_1, GPIO.OUT, initial=GPIO.HIGH)  # assuming relay is off when HIGH
GPIO.setup(RELAY_PIN_3, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RELAY_PIN_4, GPIO.OUT, initial=GPIO.HIGH)

power_turned_on = False
relay_3_triggered = False
relay_4_triggered = 0

def activate_relay(pin):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin, GPIO.HIGH)

try:
    while True:
        humidity, temperature_celsius = Adafruit_DHT.read_retry(SENSOR_TYPE, DHT_PIN)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Power Turned On: {power_turned_on}")
        print(f"Relay 3 Triggered: {relay_3_triggered}")
        print(f"Relay 4 Triggered: {relay_4_triggered}")

        if humidity is not None and temperature_celsius is not None:
            temperature_fahrenheit = (temperature_celsius * 9/5) + 32
            print(f"{current_time}: Temperature: {temperature_fahrenheit:.2f}°F, Humidity: {humidity:.2f}%")

            if humidity > 60:
                if not power_turned_on:
                    activate_relay(RELAY_PIN_1)
                    print("Dehumidifier is ON")
                    power_turned_on = True

                if not relay_3_triggered:
                    activate_relay(RELAY_PIN_3)
                    relay_3_triggered = True

                if relay_3_triggered and relay_4_triggered < 2:
                    activate_relay(RELAY_PIN_4)
                    relay_4_triggered += 1

            else:
                if power_turned_on:
                    activate_relay(RELAY_PIN_1)
                    print("Dehumidifier is OFF")
                    power_turned_on = False
                    relay_3_triggered = False
                    relay_4_triggered = 0

        else:
            print(f"{current_time}: Failed to retrieve data from the sensor. Check your connections.")

        time.sleep(10)

except KeyboardInterrupt:
    GPIO.cleanup()
