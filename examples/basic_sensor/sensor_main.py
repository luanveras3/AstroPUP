# AstroPUP example: Basic external MicroPython sensor
#
# Runs on an external MicroPython device that is connected to the LEGO Hub
# through a PUPRemote/LPF2-compatible connection.
#
# Copy astropup_sensor.py to the same device before running this file.

from astropup_sensor import AstroPUPSensor

sensor = AstroPUPSensor(profile="competition", debug=False)

counter = 0


def reset():
    global counter
    counter = 0
    return (1,)


def state():
    global counter

    counter += 1

    # Format "hB":
    # h -> signed 16-bit counter
    # B -> unsigned byte status
    status = 1
    return (counter, status)


# The order, names, and formats must match the Hub side.
sensor.add_command("reset", "B", callback=reset)
sensor.add_command("state", "hB", callback=state)

while True:
    sensor.safe_process()
