# AstroPUP example: Heartbeat / stale-data Hub
#
# Runs on the LEGO Hub with Pybricks.
#
# Use with sensor_main.py from this folder.

from pybricks.parameters import Port
from pybricks.tools import wait
from astropup_hub import AstroPUPHub

link = AstroPUPHub(Port.C, profile="debug", debug=True)

link.add_command("reset", "B")
link.add_command("state", "hh")

print(link.startup_report())

while True:
    data = link.safe_call("state", default=None)

    if data is not None:
        frame_id, value = data

        fresh = link.track_frame(frame_id, stale_after=2)

        print(
            "frame:", frame_id,
            "value:", value,
            "fresh:", fresh,
            "stale:", link.is_stale(),
            "stale_count:", link.stale_count(),
        )
    else:
        print("read failed:", link.last_error_text())

    wait(300)
