# AstroPUP example: Heartbeat / stale-data sensor
#
# Runs on the external MicroPython device.
#
# Change FREEZE_FRAME to True to simulate a sensor that is still responding
# but no longer producing new data.

from astropup_sensor import AstroPUPSensor

sensor = AstroPUPSensor(profile="competition", debug=False)

FREEZE_FRAME = False
frozen_frame_id = 100

value = 0


def reset():
    global value
    value = 0
    sensor.reset_frame_id()
    return (1,)


def state():
    global value

    value += 1

    if FREEZE_FRAME:
        frame_id = frozen_frame_id
    else:
        frame_id = sensor.next_frame_id()

    # Format "hh":
    # h -> frame_id
    # h -> value
    return (frame_id, value)


sensor.add_command("reset", "B", callback=reset)
sensor.add_command("state", "hh", callback=state)

while True:
    sensor.safe_process()
