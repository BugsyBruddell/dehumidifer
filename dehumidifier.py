import Adafruit_DHT
import time
from relay_control import RelayControl
from logger import Logger
from web_logger import WebLogger  # Import the WebLogger class

# Sensor Setup
DHT_PIN = 23
SENSOR_TYPE = Adafruit_DHT.DHT22

# Create instances of RelayControl, Logger, and WebLogger classes
relay = RelayControl()
logger = Logger('./logs/enviro.txt', './logs/relay-activity.txt', './logs/STATE')
web_logger = WebLogger('./logs/relay-activity.txt', './logs/enviro.txt', './logs/STATE', '/var/www/html/index.html')

# Load the initial state of the dehumidifier from the STATE file
initial_state = logger.get_state()
if initial_state == "ON":
    power_turned_on = True
else:
    power_turned_on = False

relay_3_triggered = False
relay_4_triggered = 0

update_counter = 0  # Counter to track when to update the HTML file

# Initialize timer variables
dehumidifier_on_time = 0
dehumidifier_off_time = 0
defrost_cycle = False

# Initialize the cooldown timer
cooldown_timer = 0

# Initialize the hourly timer
hourly_timer = time.time()  # Initialize it to the current time

try:
    while True:
        humidity, temperature_celsius = Adafruit_DHT.read_retry(SENSOR_TYPE, DHT_PIN)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{current_time}: Temperature: {temperature_celsius:.2f}°C, Humidity: {humidity:.2f}%"
        logger.log_env_data(log_message)

        # Check if it's time to initiate the hourly defrost cycle
        if power_turned_on and (time.time() - hourly_timer) >= 3600:  # 3600 seconds = 1 hour
            logger.log_relay_activity(f"{current_time}: Hourly defrost cycle. Entering defrost cycle for 5 minutes.")
            relay.activate_relay(relay.RELAY_PIN_1)  # Turn off the dehumidifier during defrost
            time.sleep(300)  # Wait for 5 minutes (300 seconds) for defrost
            relay.activate_relay(relay.RELAY_PIN_1)  # Turn the dehumidifier back on
            hourly_timer = time.time()  # Reset the hourly timer

        if humidity > 45 and cooldown_timer <= 0:
            if not power_turned_on:
                relay.activate_relay(relay.RELAY_PIN_1)
                logger.log_relay_activity(f"{current_time}: Activated Relay 1 (Power Supply)")
                power_turned_on = True
                dehumidifier_on_time = time.time()

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
                dehumidifier_off_time = time.time()

                # Set the cooldown timer to 300 seconds (5 minutes)
                cooldown_timer = 300

        # Decrement the cooldown timer if it is greater than zero
        if cooldown_timer > 0:
            cooldown_timer -= 5  # Decrement by 5 seconds

        # Set state after relay actions
        if power_turned_on:
            logger.set_state("ON")
        else:
            logger.set_state("OFF")

        # Increment and check the update counter
        update_counter += 1
        if update_counter >= 6:  # 5 seconds * 6 = 30 seconds
            web_logger.generate_html()
            update_counter = 0

        time.sleep(5)

except KeyboardInterrupt:
    relay.cleanup()
