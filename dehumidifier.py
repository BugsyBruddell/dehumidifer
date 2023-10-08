import Adafruit_DHT
import time
from relay_control import RelayControl
from logger import Logger

# Sensor Setup
DHT_PIN = 23
SENSOR_TYPE = Adafruit_DHT.DHT22

# State Variables
power_turned_on = False
relay_3_triggered = False
relay_4_triggered = 0

# Create instances of RelayControl and Logger classes
relay = RelayControl()
logger = Logger('./logs/enviro.txt', './logs/relay-activity.txt')

try:
    while True:
        humidity, temperature_celsius = Adafruit_DHT.read_retry(SENSOR_TYPE, DHT_PIN)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{current_time}: Temperature: {temperature_celsius:.2f}°C, Humidity: {humidity:.2f}%"
        logger.log_env_data(log_message)

        if humidity > 45:
            if not power_turned_on:
                relay.activate_relay(relay.RELAY_PIN_1)
                logger.log_relay_activity(f"{current_time}: Activated Relay 1 (Power Supply)")
                power_turned_on = True

            if not relay_3_triggered:
                relay.activate_relay(relay.RELAY_PIN_3)
                logger.log_relay_activity(f"{current_time}: Pulses Relay 3 (Power Button)")
                relay_3_triggered = True

            if relay_3_triggered and relay_4_triggered < 2:
                relay.activate_relay(relay.RELAY_PIN_4)
                logger.log_relay_activity(f"{current_time}: Pulses Relay 4 (Indicator Light)")
                relay_4_triggered += 1

        else:
            if power_turned_on:
                relay.activate_relay(relay.RELAY_PIN_1)
                logger.log_relay_activity(f"{current_time}: Deactivated Relay 1 (Power Supply)")
                power_turned_on = False
                relay_3_triggered = False
                relay_4_triggered = 0

        time.sleep(5)

except KeyboardInterrupt:
    relay.cleanup()
