# AstroPUP example: Saturn-style external device bridge
#
# This is an example template based on a robot that sends:
#
#   frame_id, line_error, junction, button, c1, c2, c3, c4
#
# Format:
#
#   "hhhBhhhh"
#
# This is project-specific code. It is intentionally outside AstroPUP Core.

from astropup_sensor import AstroPUPSensor

sensor = AstroPUPSensor(profile="competition", debug=False)

cam_vals = [0, 0, 0, 0]


def read_camera_or_external_data():
    # Replace this with your own UART, I2C, SPI, camera, or sensor reading.
    # Keep this project-specific code outside AstroPUP Core.
    pass


def calculate_line_error():
    # Replace with your own line sensor calculation.
    return 2000


def detect_junction():
    # Replace with your own junction logic.
    return 0


def read_button():
    # Replace with your own button input.
    return 0


def reset():
    sensor.reset_frame_id()
    return (1,)


def state():
    read_camera_or_external_data()

    return (
        sensor.next_frame_id(),   # h -> frame_id
        calculate_line_error(),   # h -> line_error
        detect_junction(),        # h -> junction
        read_button(),            # B -> button
        cam_vals[0],              # h -> custom value 1
        cam_vals[1],              # h -> custom value 2
        cam_vals[2],              # h -> custom value 3
        cam_vals[3],              # h -> custom value 4
    )


sensor.add_command("reset", "B", callback=reset)
sensor.add_command("state", "hhhBhhhh", callback=state)

while True:
    sensor.safe_process()
