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

# Create and open a status log file
status_log_file = open('./logs/status.txt', 'w')

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
        
        # Create a log message with temperature, humidity, and timestamp
        log_message = f"{current_time}: Temperature: {temperature_celsius:.2f}°C, Humidity: {humidity:.2f}%, " \
                      f"power_turned_on: {power_turned_on}, defrost_cycle: {defrost_cycle}, " \
                      f"cooldown_timer: {cooldown_timer}, hourly_timer: {hourly_timer}"
                      
        # Write the log message to the status log file
        status_log_file.write(log_message + '\n')
        status_log_file.flush()  # Make sure the data is written to the file

        # Your existing code...

        time.sleep(5)

except KeyboardInterrupt:
    relay.cleanup()
    status_log_file.close()  # Close the status log file when the script is terminated
