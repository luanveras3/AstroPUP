# AstroPUP Hub Hello World for OpenMV
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
        frame = data[0]
        print("OpenMV answered. Frame:", frame)
    else:
        print("No answer from OpenMV.")

    wait(1000)
