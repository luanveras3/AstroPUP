# AstroPUP - LMS-ESP32 bridging an OpenMV camera to the LEGO hub
#
# Copy this file to the LMS-ESP32 as main.py.
# Also copy:
#   - astropup_sensor.py
#
# The LMS-ESP32 reads vision results from the OpenMV over UART and
# forwards them to the LEGO hub through AstroPUP. It does NOT process
# images here - keep all OpenCV-style work on the OpenMV.
#
# Line protocol from the OpenMV (ASCII, '\n' terminated):
#
#   found,cx,cy,area,frame_id\n

from time import sleep_ms
from machine import UART, Pin
from astropup_sensor import AstroPUPSensor


# --- UART to the OpenMV camera ---------------------------------------------
# Default pins below are safe choices on the LMS-ESP32 (free GPIOs, not
# strapping pins, not reserved for the LPF2 link). Adjust if you wired
# differently. Do NOT reuse the pins from `from lms_esp32 import RX_PIN, TX_PIN`
# - those carry the LPF2 link to the hub.

UART_ID = 1
UART_BAUD = 115200
UART_TX = 17
UART_RX = 16

cam = UART(UART_ID, baudrate=UART_BAUD, tx=Pin(UART_TX), rx=Pin(UART_RX))
buffer = b""

last_found = 0
last_cx = 0
last_cy = 0
last_area = 0
last_frame_id = 0


def poll_camera():
    """Read any new bytes from the camera UART and update the last state.

    Safe to call every loop tick: never blocks, never raises, silently
    discards malformed lines.
    """
    global buffer, last_found, last_cx, last_cy, last_area, last_frame_id

    try:
        n = cam.any()
        if n:
            buffer += cam.read(n) or b""
    except Exception:
        return

    while b"\n" in buffer:
        line, _, buffer = buffer.partition(b"\n")
        try:
            parts = line.strip().split(b",")
            if len(parts) != 5:
                continue
            last_found = int(parts[0])
            last_cx = int(parts[1])
            last_cy = int(parts[2])
            last_area = int(parts[3])
            last_frame_id = int(parts[4])
        except Exception:
            continue


# --- AstroPUP link to the LEGO hub -----------------------------------------

link = AstroPUPSensor(profile="competition", debug=False)


def vision():
    poll_camera()
    return (last_found, last_cx, last_cy, last_area, last_frame_id)


link.add_command("vision", "Bhhhh", callback=vision)

print("AstroPUP LMS-ESP32 camera bridge ready.")
print("Waiting for OpenMV on UART", UART_ID, "(", UART_BAUD, "baud) ...")

while True:
    poll_camera()
    link.safe_process()
    sleep_ms(2)
