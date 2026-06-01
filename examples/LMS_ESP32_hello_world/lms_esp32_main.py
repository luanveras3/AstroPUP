# AstroPUP - LMS-ESP32 Hello World
#
# Copy this file to the LMS-ESP32 as main.py.
# Also copy:
#   - astropup_sensor.py
#
# The LMS-ESP32 ships pre-flashed with MicroPython + PUPRemote, so you
# do NOT need to copy lpf2.py here (the firmware already provides it).
# That is the main difference vs. a generic ESP32.

from time import sleep_ms
from astropup_sensor import AstroPUPSensor


# AstroPUPSensor auto-detects the LMS-ESP32 hub pins from the firmware.
link = AstroPUPSensor(profile="debug", debug=True)

counter = 0


def hello():
    global counter
    counter += 1
    print("Hello from LMS-ESP32! Call:", counter)
    return (counter,)


link.add_command("hello", "h", callback=hello)

print("AstroPUP LMS-ESP32 Hello World ready.")

while True:
    link.safe_process()
    sleep_ms(5)
