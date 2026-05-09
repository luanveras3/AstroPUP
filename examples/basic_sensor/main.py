from astropup_sensor import AstroPUPSensor

sensor = AstroPUPSensor(profile="competition", debug=False)

def reset():
    return (1,)

def state():
    value_1 = 123
    value_2 = -45
    return (value_1, value_2)

sensor.add_command("reset", "B", callback=reset)
sensor.add_command("state", "hh", callback=state)

while True:
    sensor.safe_process()
