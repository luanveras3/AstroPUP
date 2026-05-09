# AstroPUP example: Basic LEGO Pybricks Hub reader
#
# Runs on the LEGO Hub with Pybricks.
#
# Copy astropup_hub.py to the same Hub project folder before running this file.

from pybricks.parameters import Port
from pybricks.tools import wait
from astropup_hub import AstroPUPHub

link = AstroPUPHub(Port.C, profile="debug", debug=True)

# The order, names, and formats must match the Sensor side.
link.add_command("reset", "B")
link.add_command("state", "hB")

print(link.startup_report())

while True:
    data = link.safe_call("state", default=None)

    if data is not None:
        counter, status = data
        print("counter:", counter, "status:", status)
    else:
        print("read failed:", link.last_error_text())

    print("calls:", link.call_count(), "success:", link.success_count(), "fails:", link.fail_count())

    wait(500)
