# AstroPUP example: Saturn-style Hub reader
#
# Runs on the LEGO Hub with Pybricks.
#
# This example reads:
#
#   frame_id, line_error, junction, button, c1, c2, c3, c4
#
# It also tracks stale data using frame_id.

from pybricks.parameters import Port
from pybricks.tools import wait
from astropup_hub import AstroPUPHub

link = AstroPUPHub(Port.C, profile="debug", debug=True)

link.add_command("reset", "B")
link.add_command("state", "hhhBhhhh")

print(link.startup_report())

while True:
    data = link.safe_call("state", default=None)

    if data is not None and len(data) == 8:
        frame_id, line_error, junction, button, c1, c2, c3, c4 = data

        link.track_frame(frame_id, stale_after=3)

        print(
            "frame:", frame_id,
            "stale:", link.is_stale(),
            "line:", line_error,
            "junction:", junction,
            "button:", button,
            "custom:", c1, c2, c3, c4,
        )
    else:
        print("read failed:", link.last_error_text())

    wait(200)
