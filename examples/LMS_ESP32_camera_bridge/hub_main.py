# AstroPUP Hub - reads vision data through an LMS-ESP32 bridge
#
# Copy this file to the LEGO hub Pybricks project.
# Also copy astropup_hub.py to the same project.
#
# The hub does not know there is a camera at the other end of the
# bridge. It only talks to the LMS-ESP32 through AstroPUP/LPF2 using a
# single command, "vision".

from pybricks.parameters import Port
from pybricks.tools import wait
from astropup_hub import AstroPUPHub


# Adjust Port.C to wherever the LMS-ESP32 cable is plugged in.
link = AstroPUPHub(Port.C, profile="competition", debug=False)
link.add_command("vision", "Bhhhh")

print("AstroPUP Hub - camera bridge reader ready.")
print(link.startup_report())

while True:
    # 10 ms of slack for the bridge to finish a UART read before we
    # poll. Tune up if you see stale data on heavy loads.
    data = link.safe_call("vision", default=None, wait_ms=10)

    if data is None:
        print("No data from LMS-ESP32 yet.")
        wait(50)
        continue

    found, cx, cy, area, frame_id = data
    link.track_frame(frame_id)

    if link.is_stale(max_stale=10):
        # Same frame_id for too many cycles = camera is stuck.
        print("WARN: camera appears stuck (same frame_id repeated)")
    elif found == 0:
        print("Nothing in view")
    else:
        print("Target at ({}, {}) area={}  frame={}".format(cx, cy, area, frame_id))

    wait(50)
