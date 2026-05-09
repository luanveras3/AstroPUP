# AstroPUP example: Startup diagnostics
#
# Runs on the LEGO Hub with Pybricks.
#
# Purpose:
#   Shows the remote modes, registered commands, and validation result.
#   This is useful before a run or when debugging command order errors.

from pybricks.parameters import Port
from astropup_hub import AstroPUPHub

link = AstroPUPHub(Port.C, profile="debug", debug=True)

# Must match the remote sensor.
link.add_command("reset", "B")
link.add_command("state", "hB")

print(link.startup_report())

# Optional strict validation:
# If the remote mode order does not match the Hub registration order,
# this will raise an AssertionError with a clear AstroPUP message.
link.validate_remote_modes(strict=True)

print("AstroPUP mode validation passed.")
