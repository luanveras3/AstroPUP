# AstroPUP Hub - LMS-ESP32 Hello World
#
# Copy this file to the LEGO hub Pybricks project.
# Also copy astropup_hub.py to the same project.

from pybricks.parameters import Port
from pybricks.tools import wait
from astropup_hub import AstroPUPHub


# Adjust Port.C to wherever the flat LPF2 cable from the LMS-ESP32
# is plugged into the LEGO hub.
link = AstroPUPHub(Port.C, profile="debug", debug=True)

link.add_command("hello", "h")

print("AstroPUP Hub Hello World (LMS-ESP32) ready.")
print(link.startup_report())

while True:
    print("Hello from LEGO Hub!")

    data = link.safe_call("hello", default=None)

    if data is not None:
        (counter,) = data
        print("LMS-ESP32 answered. Counter:", counter)
    else:
        print("No answer from LMS-ESP32.")

    wait(1000)
