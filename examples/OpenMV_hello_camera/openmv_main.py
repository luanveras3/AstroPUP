# AstroPUP OpenMV Hello Camera
#
# Copy this file to the OpenMV board as main.py.
# Also copy:
# - astropup_sensor.py
# - lpf2.py
#
# This example only confirms that the camera is running and that
# the LEGO hub can call the OpenMV through AstroPUP.

import sensor
import time
from astropup_sensor import AstroPUPSensor


# Basic OpenMV camera setup.
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=1000)

clock = time.clock()

link = AstroPUPSensor(profile="debug", debug=True)

frame_counter = 0


def hello():
    global frame_counter

    frame_counter += 1

    print("Hello from OpenMV camera! Frame:", frame_counter)

    # Return a small number to the hub.
    return (frame_counter,)


link.add_command("hello", "h", callback=hello)

print("AstroPUP OpenMV Hello Camera ready.")

while True:
    clock.tick()

    # Take a snapshot so we know the camera loop is alive.
    img = sensor.snapshot()

    # Optional visual debug in OpenMV IDE.
    img.draw_string(5, 5, "AstroPUP Hello")

    link.safe_process()

    time.sleep_ms(5)
