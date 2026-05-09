# Sensor-side snippet for an LMS-ESP32 style project.

sensor.add_command("state", "hhhBhhhh", callback=state)

def state():
    read_devkit()

    return (
        sensor.next_frame_id(),       # h -> frame_id
        calculate_position(),         # h -> error
        custom_junction_detect(),     # h -> junction
        read_button(),                # B -> button
        cam_vals[0],                  # h -> custom value 1
        cam_vals[1],                  # h -> custom value 2
        cam_vals[2],                  # h -> custom value 3
        cam_vals[3],                  # h -> custom value 4
    )
