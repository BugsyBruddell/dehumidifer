import Adafruit_DHT
import time

# Set the GPIO pin where the DHT22 sensor is connected
DHT_PIN = 23
SENSOR_TYPE = Adafruit_DHT.DHT22

try:
    while True:
        humidity, temperature_celsius = Adafruit_DHT.read_retry(SENSOR_TYPE, DHT_PIN)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        if humidity is not None and temperature_celsius is not None:
            temperature_fahrenheit = (temperature_celsius * 9/5) + 32
            data = f"{current_time}: Temperature: {temperature_fahrenheit:.2f}°F, Humidity: {humidity:.2f}%"

            # Append data to the file
            with open("/home/bripi/Code/logs/enviro.txt", "a") as file:
                file.write(data + "\n")
                print(data)  # Print the data to the console

        else:
            print(f"{current_time}: Failed to retrieve data from the sensor. Check your connections.")

        time.sleep(10)  # Sleep for 10 seconds before the next reading

except KeyboardInterrupt:
    pass
