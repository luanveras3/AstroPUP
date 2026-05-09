# AstroPUP Generic Core v0.3.0 — Heartbeat / Frame Tracking Guide

AstroPUP v0.3.0 adds optional heartbeat support without changing the LPF2/PUPRemote protocol.

This is generic. AstroPUP does not know your robot, packet format, camera, line sensor, or mission.

You decide:

- whether your packet has a frame_id;
- where the frame_id is inside the packet;
- how the robot should react to stale data.

---

## 1. Performance impact

If you do not use heartbeat tracking, the impact is essentially only a few stored attributes.

If you use it, the added cost is small:

- one extra integer in your packet;
- one comparison on the Hub;
- a few counters updated in memory.

For a typical Pybricks/PUPRemote use case, this is much lighter than camera processing, I2C sensor reading, line calculation, or motor control logic.

Keep packets small. PUPRemote recommends `max_packet_size=16` for Pybricks compatibility. So use one compact `h` or `B` field for frame_id when possible.

---

## 2. Sensor-side example

This runs on the external MicroPython device.

```python
from astropup_sensor import AstroPUPSensor

sensor = AstroPUPSensor(profile="competition", debug=False)

def reset():
    return (1,)

def state():
    frame_id = sensor.next_frame_id()  # optional heartbeat value

    value_1 = 123
    value_2 = -45

    # Format below is "hhh":
    # frame_id, value_1, value_2
    return (frame_id, value_1, value_2)

sensor.add_command("reset", "B", callback=reset)
sensor.add_command("state", "hhh", callback=state)

while True:
    sensor.safe_process()
```

---

## 3. Hub-side example

This runs on the LEGO Pybricks Hub.

```python
from pybricks.parameters import Port
from pybricks.tools import wait
from astropup_hub import AstroPUPHub

link = AstroPUPHub(Port.C, profile="debug", debug=True)

link.add_command("reset", "B")
link.add_command("state", "hhh")

print(link.startup_report())

while True:
    data = link.safe_call("state", default=None)

    if data is not None:
        frame_id, value_1, value_2 = data

        fresh = link.track_frame(frame_id)

        print("frame:", frame_id)
        print("fresh:", fresh)
        print("stale:", link.is_stale())
        print("stale_count:", link.stale_count())
        print("data:", value_1, value_2)

    wait(100)
```

---

## 4. Adapting your existing Saturn packet

Your current packet:

```python
# old format:
"hhBhhhh"

# old return:
(error, junction, button, c1, c2, c3, c4)
```

With frame_id:

```python
# new format:
"hhhBhhhh"

# new return:
(frame_id, error, junction, button, c1, c2, c3, c4)
```

Sensor side:

```python
def state():
    frame_id = sensor.next_frame_id()

    return (
        frame_id,
        calculate_position(),
        custom_junction_detect(),
        read_button(),
        cam_vals[0],
        cam_vals[1],
        cam_vals[2],
        cam_vals[3],
    )
```

Hub side registration:

```python
Robot.sensor.add_command("state", "hhhBhhhh")
```

Hub side reading:

```python
res = await Robot.sensor.safe_call_multitask("state", default=None)

if res is not None and len(res) == 8:
    frame_id, Robot.erro, Robot.junction, Robot.button, Robot.c1, Robot.c2, Robot.c3, Robot.c4 = res
    Robot.sensor.track_frame(frame_id)
```

Debug print:

```python
print("frame:", Robot.sensor.last_frame_id())
print("stale:", Robot.sensor.is_stale())
print("stale_count:", Robot.sensor.stale_count())
```

---

## 5. Important warning

Using `last_good_response()` and heartbeat tracking does not automatically make old data safe.

In a moving robot, old camera or line data may be dangerous.

AstroPUP gives you the information. Your robot code decides whether to:

- keep using the last value;
- slow down;
- stop;
- retry;
- ignore a stale packet.
