# AstroPUP - LMS-ESP32 as a UART bridge
#
# Copy this file to the LMS-ESP32 as main.py.
# Also copy:
#   - astropup_sensor.py
#
# This program turns the LMS-ESP32 into a bridge between an external
# device (any MicroPython board, Arduino, or sensor that talks UART)
# and the LEGO hub. The LMS-ESP32 does no processing of its own - it
# just forwards data.
#
# Topology:
#
#   External device  --UART-->  LMS-ESP32  --LPF2/AstroPUP-->  LEGO Hub
#
# Line protocol (text, simple, no extra library required):
#
#   Each message is a single ASCII line terminated by '\n'.
#   Fields are integers separated by commas:
#
#       value,frame_id\n
#
#   - value:    -32768 .. 32767  (fits the "h" struct format)
#   - frame_id: 0 .. 32767       (used to detect stale data on the hub side)

from time import sleep_ms
from machine import UART, Pin
from astropup_sensor import AstroPUPSensor


# --- UART to the external device --------------------------------------------
# Adjust the pins to wherever you wired the external device on the LMS-ESP32.
# Avoid the ESP32 strapping pins (0, 2, 12, 15) and the pins reserved for
# the LPF2 link (RX_PIN / TX_PIN from `lms_esp32`).

UART_ID = 1
UART_BAUD = 115200
UART_TX = 17
UART_RX = 16

cam_uart = UART(UART_ID, baudrate=UART_BAUD, tx=Pin(UART_TX), rx=Pin(UART_RX))
buffer = b""

last_value = 0
last_frame_id = 0


def poll_external_device():
    """Read any new bytes from the UART and update last_value/last_frame_id.

    Designed to be safe to call every loop tick: it never blocks, never
    raises, and silently discards malformed lines.
    """
    global buffer, last_value, last_frame_id

    try:
        n = cam_uart.any()
        if n:
            buffer += cam_uart.read(n) or b""
    except Exception:
        return

    while b"\n" in buffer:
        line, _, buffer = buffer.partition(b"\n")
        try:
            parts = line.strip().split(b",")
            if len(parts) != 2:
                continue
            last_value = int(parts[0])
            last_frame_id = int(parts[1])
        except Exception:
            # Junk on the wire is normal at startup; ignore it.
            continue


# --- AstroPUP link to the LEGO hub ------------------------------------------

link = AstroPUPSensor(profile="competition", debug=False)


def state():
    poll_external_device()
    return (last_value, last_frame_id)


link.add_command("state", "hh", callback=state)

print("AstroPUP LMS-ESP32 UART bridge ready.")
print("Waiting for lines on UART", UART_ID, "(", UART_BAUD, "baud) ...")

while True:
    poll_external_device()
    link.safe_process()
    sleep_ms(2)
