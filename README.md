# AstroPUP

**AstroPUP** is a generic, competition-oriented communication helper for LEGO Pybricks hubs and external MicroPython devices.

It is designed for educational robotics, competition robots, and custom LPF2 / Powered Up sensor bridges.

AstroPUP is developed by **Astrogenius - Brazil**.

Team Instagram: **@astrogenius.team**

## What AstroPUP does

AstroPUP provides a safer and clearer layer on top of the PUPRemote communication foundation.

It adds:

- safe hub-side calls;
- safe sensor-side processing;
- Pybricks multitask support helpers;
- remote mode validation;
- startup reports;
- call, success, and failure counters;
- last good response storage;
- optional heartbeat / frame tracking;
- stale-data detection helpers;
- generic command registration helpers;
- readable diagnostics for students, mentors, and teams.

## What AstroPUP does not do

AstroPUP does **not** replace the LPF2 / Powered Up protocol.

AstroPUP does **not** include robot-specific logic.

AstroPUP does **not** know your camera, line sensor, color table, mission strategy, or packet meaning.

Your project-specific logic should stay in your own files, such as:

- `main.py`;
- `robot.py`;
- `sensors.py`;
- `my_robot_profile.py`;
- `saturn_profile.py`.

## Foundation and attribution

AstroPUP includes code derived from **PUPRemote by Anton's Mindstorms**.

Original project:

https://github.com/antonvh/PUPRemote

AstroPUP keeps attribution to the original project and adds Astrogenius-specific improvements on top.

## Files

```text
src/
  astropup_hub.py      # LEGO Pybricks hub side
  astropup_sensor.py   # external MicroPython sensor side

docs/
  HEARTBEAT_GUIDE.md

examples/
  basic_sensor/
  basic_sync_hub/
  pybricks_multitask_hub/
  saturn_heartbeat_example/
```

## Basic sensor-side example

```python
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
```

## Basic hub-side example

```python
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
        print(data)

    wait(100)
```

## Optional heartbeat / stale-data tracking

Sensor side:

```python
def state():
    frame_id = sensor.next_frame_id()
    value_1 = 123
    value_2 = -45
    return (frame_id, value_1, value_2)

sensor.add_command("state", "hhh", callback=state)
```

Hub side:

```python
link.add_command("state", "hhh")

data = link.safe_call("state", default=None)

if data is not None:
    frame_id, value_1, value_2 = data
    fresh = link.track_frame(frame_id)

    print("fresh:", fresh)
    print("stale:", link.is_stale())
    print("stale_count:", link.stale_count())
```

## Important rule

The hub side and the sensor side must register commands in the same:

1. order;
2. names;
3. formats.

Example:

Sensor:

```python
sensor.add_command("reset", "B", callback=reset)
sensor.add_command("state", "hh", callback=state)
```

Hub:

```python
link.add_command("reset", "B")
link.add_command("state", "hh")
```

## Version

Current development version: **v0.3.0**

## License

AstroPUP contains code derived from PUPRemote.

PUPRemote is distributed under the GPL / GPL-3.0 license.

AstroPUP is released under **GPL-3.0-compatible terms** and keeps attribution to the original PUPRemote project.

See `CREDITS.md` and `LICENSE` for details.
