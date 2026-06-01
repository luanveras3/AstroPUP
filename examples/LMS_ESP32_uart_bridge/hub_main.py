# AstroPUP Hub - LMS-ESP32 UART Bridge
#
# Copy this file to the LEGO hub Pybricks project.
# Also copy astropup_hub.py to the same project.
#
# The hub does not know there is a bridge in the middle. It only talks
# to the LMS-ESP32 through AstroPUP/LPF2 the same way it would talk to
# any other AstroPUP sensor.

from pybricks.parameters import Port
from pybricks.tools import wait
from astropup_hub import AstroPUPHub


link = AstroPUPHub(Port.C, profile="competition", debug=False)
link.add_command("state", "hh")

print("AstroPUP Hub - UART bridge reader ready.")
print(link.startup_report())

while True:
    data = link.safe_call("state", default=None, wait_ms=2)

    if data is not None:
        value, frame_id = data
        # Heartbeat tracking spots a stuck external device (same frame_id
        # arriving over and over) without any extra wiring.
        link.track_frame(frame_id)
        if link.is_stale(max_stale=10):
            print("WARN: external device is stale (no new frames)")
        else:
            print("value =", value, " frame =", frame_id)
    else:
        print("No data from LMS-ESP32 yet.")

    wait(50)
