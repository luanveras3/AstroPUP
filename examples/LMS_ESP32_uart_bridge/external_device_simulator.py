# External device simulator
#
# This is the "left side" of the bridge: any MicroPython device that
# sends data over UART to the LMS-ESP32. It exists only to make this
# example runnable without a real second device.
#
# Replace this file with whatever your actual sensor / camera / board
# is doing. The only contract is the line protocol:
#
#   value,frame_id\n
#
# Wire your device's UART TX to the LMS-ESP32 UART RX (and GND to GND).
# If you also want the hub-side to be able to send commands back, wire
# the LMS-ESP32 UART TX to your device's UART RX too.
#
# This stand-in code targets a generic MicroPython board. Adjust UART
# id, baud rate and pins for your hardware.

from time import sleep_ms
from machine import UART, Pin

UART_ID = 1
UART_BAUD = 115200
UART_TX = 4   # adjust to your device
UART_RX = 5   # adjust to your device

link = UART(UART_ID, baudrate=UART_BAUD, tx=Pin(UART_TX), rx=Pin(UART_RX))

frame_id = 0
value = 0

while True:
    # Replace this with your real sensor reading.
    value = (value + 1) % 1000

    # frame_id wraps to stay inside the signed 16-bit range used by "h".
    frame_id = (frame_id + 1) & 0x7FFF

    msg = "{},{}\n".format(value, frame_id)
    link.write(msg.encode("ascii"))

    sleep_ms(20)
