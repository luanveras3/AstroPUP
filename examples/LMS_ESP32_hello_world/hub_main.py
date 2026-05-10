# AstroPUP Hub Hello World for ESP32
#
# Copy this file to the LEGO hub Pybricks project.
# Also copy astropup_hub.py to the same project.

from pybricks.parameters import Port
from pybricks.tools import wait
from astropup_hub import AstroPUPHub


link = AstroPUPHub(Port.C, profile="debug", debug=True)

link.add_command("hello", "h")

print("AstroPUP Hub Hello World ready.")
print(link.startup_report())

while True:
    print("Hello from LEGO Hub!")

    data = link.safe_call("hello", default=None)

    if data is not None:
        value = data[0]
        print("ESP32 answered:", value)
    else:
        print("No answer from ESP32.")

    wait(1000)
