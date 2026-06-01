# AstroPUP - Generic OpenMV blob tracker (sends data over UART)
#
# Copy this file to the OpenMV as main.py.
#
# This is a *generic* color blob tracker: it finds the largest blob
# matching TARGET_THRESHOLD and sends its presence + center + size to
# the LMS-ESP32 over UART. The LMS-ESP32 forwards that data to the
# LEGO hub through AstroPUP.
#
# Topology:
#
#   OpenMV (vision)  --UART-->  LMS-ESP32 (bridge)  --LPF2/AstroPUP-->  LEGO Hub
#
# Tune TARGET_THRESHOLD for your object using the OpenMV IDE Threshold
# Editor under the lighting you will actually use.

import sensor
import time
import math
from machine import UART

# --- Camera setup ----------------------------------------------------------

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=1000)

# Stable thresholds need a fixed exposure / white balance.
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()

# --- UART to the LMS-ESP32 --------------------------------------------------
# On the OpenMV, the primary UART is on P4 (TX) and P5 (RX).
# Wire OpenMV P4 -> LMS-ESP32 GPIO 16 (RX) and OpenMV P5 -> LMS-ESP32 GPIO 17 (TX).

UART_BAUD = 115200
link = UART(3, UART_BAUD, timeout_char=1000)

# --- Tracking target -------------------------------------------------------
# Replace these LAB values with whatever your object looks like under
# the real lighting. Use Tools > Machine Vision > Threshold Editor.
# Example below is "a bright red object".
TARGET_THRESHOLD = [(40, 80, 30, 90, 0, 60)]

MIN_AREA = 100          # pixels - ignore very small noise blobs
frame_id = 0


def send(found, cx, cy, area):
    """Send one line to the LMS-ESP32 over UART."""
    msg = "{},{},{},{},{}\n".format(found, cx, cy, area, frame_id)
    link.write(msg.encode("ascii"))


print("AstroPUP OpenMV blob tracker (bridge) ready.")

while True:
    clock.tick()

    img = sensor.snapshot()
    frame_id = (frame_id + 1) & 0x7FFF

    blobs = img.find_blobs(
        TARGET_THRESHOLD,
        pixels_threshold=MIN_AREA,
        area_threshold=MIN_AREA,
        merge=True,
    )

    if blobs:
        # Largest blob = our target.
        b = max(blobs, key=lambda x: x.pixels())
        img.draw_rectangle(b.rect(), color=(0, 255, 0))
        img.draw_cross(b.cx(), b.cy(), color=(255, 0, 0))

        send(1, b.cx(), b.cy(), b.pixels())
    else:
        send(0, 0, 0, 0)
