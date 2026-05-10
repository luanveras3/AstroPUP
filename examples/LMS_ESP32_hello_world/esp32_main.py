# AstroPUP ESP32 Hello World
#
# Copy this file to the ESP32 as main.py.
# Also copy:
# - astropup_sensor.py
# - lpf2.py

from time import sleep_ms
from astropup_sensor import AstroPUPSensor


link = AstroPUPSensor(profile="debug", debug=True)

counter = 0


def hello():
    global counter

    counter += 1

    print("Hello from ESP32! Call:", counter)

    # Return any small number to the hub.
    return (counter,)


link.add_command("hello", "h", callback=hello)

print("AstroPUP ESP32 Hello World ready.")

while True:
    link.safe_process()
    sleep_ms(5)
