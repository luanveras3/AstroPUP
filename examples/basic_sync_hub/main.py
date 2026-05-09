from pybricks.parameters import Port
from pybricks.tools import wait
from astropup_hub import AstroPUPHub

link = AstroPUPHub(Port.C, profile="debug", debug=True)

link.add_command("reset", "B")
link.add_command("state", "hh")

print(link.startup_report())

while True:
    data = link.safe_call("state", default=None)

    print("data:", data)
    print("error:", link.last_error_text())
    print("calls:", link.call_count(), "success:", link.success_count(), "fails:", link.fail_count())

    wait(500)
