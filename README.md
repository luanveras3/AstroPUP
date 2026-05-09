<p align="center">
  <img src="assets/astrogenius-logo.png" alt="Astrogenius Team Logo" width="180">
</p>
<h1 align="center">AstroPUP</h1>
<p align="center">
  Generic communication helper for LEGO Pybricks hubs and external MicroPython devices.
</p>
<p align="center">
  Built by <strong>Astrogenius Team from Brazil</strong> 🇧🇷<br>
  Instagram: <a href="https://www.instagram.com/astrogenius.team">@astrogenius.team</a>
</p>
---
What is AstroPUP?
AstroPUP is a generic, competition-oriented communication helper for LEGO Pybricks hubs and external MicroPython devices.
It is designed for educational robotics, competition robots, and custom LPF2 / Powered Up sensor bridges.
AstroPUP is built on top of the PUPRemote communication foundation and adds safer calls, clearer diagnostics, startup checks, counters, and optional heartbeat / stale-data detection.
AstroPUP is especially useful when a LEGO Hub running Pybricks needs to communicate with external devices such as:
LMS-ESP32;
OpenMV;
ESP32;
RP2040;
custom MicroPython boards;
external sensor bridges;
external vision or data-processing pipelines.
---
What AstroPUP does
AstroPUP provides a safer and clearer layer on top of the PUPRemote communication foundation.
It adds:
safe hub-side calls;
safe sensor-side processing;
Pybricks multitask support helpers;
remote mode validation;
startup reports;
call, success, and failure counters;
last good response storage;
optional heartbeat / frame tracking;
stale-data detection helpers;
generic command registration helpers;
readable diagnostics for students, mentors, and teams.
---
What AstroPUP does not do
AstroPUP does not replace the LPF2 / Powered Up protocol.
AstroPUP does not include robot-specific logic.
AstroPUP does not know your camera, line sensor, color table, mission strategy, or packet meaning.
Your project-specific logic should stay in your own files, such as:
`main.py`;
`robot.py`;
`sensors.py`;
`my_robot_profile.py`;
`saturn_profile.py`.
---
Foundation and attribution
AstroPUP includes code derived from PUPRemote by Anton's Mindstorms.
Original project:
https://github.com/antonvh/PUPRemote
AstroPUP keeps attribution to the original project and adds Astrogenius-specific improvements on top.
AstroPUP does not claim authorship of the original PUPRemote or LPF2 foundation. It packages and extends the hub-side and sensor-side workflow to make it easier to use in educational and competition robotics projects.
---
Repository structure
```text
src/
  astropup_hub.py      # LEGO Pybricks hub side
  astropup_sensor.py   # external MicroPython sensor side
  lpf2.py              # vendored LPF2 dependency from PUPRemote

docs/
  HEARTBEAT_GUIDE.md

examples/
  00_basic_counter_pair/
  01_startup_diagnostics/
  02_pybricks_multitask_reader/
  03_heartbeat_stale_demo/
  04_saturn_style_bridge/
```
---
Which files do I need?
The required files depend on where your code is running.
On the LEGO Pybricks Hub
Copy this file to the LEGO Hub project:
```text
astropup_hub.py
```
Your Hub-side program will usually import:
```python
from astropup_hub import AstroPUPHub
```
---
On an LMS-ESP32 with PUPRemote / LPF2 already available
Copy this file to the external device:
```text
astropup_sensor.py
```
Some LMS-ESP32 setups may already include the required LPF2 / PUPRemote foundation.
If your LMS-ESP32 already has `lpf2.py` available, you may not need to copy it again.
---
On OpenMV, ESP32, RP2040 or other MicroPython boards
Copy both files to the external MicroPython device:
```text
astropup_sensor.py
lpf2.py
```
The `lpf2.py` file is included as a vendored dependency from PUPRemote for external MicroPython devices that do not already provide it.
Your sensor-side program will usually import:
```python
from astropup_sensor import AstroPUPSensor
```
---
Important rule
The Hub side and the Sensor side must register commands in the same:
order;
names;
formats.
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
If the order, names, or formats do not match, the Hub and Sensor will not communicate correctly.
AstroPUP helps diagnose this with:
```python
link.startup_report()
link.validate_remote_modes()
```
---
Basic sensor-side example
This code runs on the external MicroPython device.
Required files on the external device:
```text
astropup_sensor.py
lpf2.py
```
If your device already provides `lpf2.py`, only `astropup_sensor.py` may be needed.
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
---
Basic hub-side example
This code runs on the LEGO Hub with Pybricks.
Required file on the Hub:
```text
astropup_hub.py
```
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
---
Pybricks multitask example
Use this when your robot already uses Pybricks multitasking.
```python
from pybricks.parameters import Port
from pybricks.tools import wait, multitask, run_task
from astropup_hub import AstroPUPHub

link = AstroPUPHub(Port.C, profile="competition", debug=False)

link.add_command("reset", "B")
link.add_command("state", "hh")

async def pup_loop():
    while True:
        await link.process_async()
        await wait(0)

async def read_loop():
    while True:
        data = await link.safe_call_multitask("state", default=None)

        if data is not None:
            value_1, value_2 = data
            # Use your values here.

        await wait(0)

async def main():
    await multitask(
        pup_loop(),
        read_loop(),
    )

run_task(main())
```
---
Startup diagnostics
AstroPUP can print a startup report to confirm that the Hub and Sensor are using matching modes.
```python
print(link.startup_report())
```
Example output:
```text
AstroPUP Startup Report
Project: AstroPUP
Version: 0.3.0
Team: Astrogenius - Brazil
Instagram: @astrogenius.team
Port: Port.C
Profile: debug
Registered commands:
  0 reset
  1 state
Remote modes:
  0 ('reset', 1, 0)
  1 ('state', 4, 0)
Mode validation: OK
Last error: ASTRO_OK
```
You can also run a strict validation:
```python
link.validate_remote_modes(strict=True)
```
If the Hub command order does not match the remote Sensor mode order, AstroPUP will raise a clear error.
---
Optional heartbeat / stale-data tracking
AstroPUP can help detect when a sensor is still responding but the data is not updating.
This is optional and generic. AstroPUP does not decide where the frame ID goes inside your packet.
Sensor side
```python
def state():
    frame_id = sensor.next_frame_id()
    value_1 = 123
    value_2 = -45

    return (frame_id, value_1, value_2)

sensor.add_command("state", "hhh", callback=state)
```
Hub side
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
This makes it possible to detect repeated or stale packets.
---
Example: project-specific packet
AstroPUP Core is generic, so your robot-specific packet should stay in your own project.
Example packet:
```python
(frame_id, line_error, junction, button, c1, c2, c3, c4)
```
Format:
```python
"hhhBhhhh"
```
Sensor side:
```python
def state():
    return (
        sensor.next_frame_id(),   # h -> frame_id
        calculate_line_error(),   # h -> line_error
        detect_junction(),        # h -> junction
        read_button(),            # B -> button
        c1,                       # h -> custom value 1
        c2,                       # h -> custom value 2
        c3,                       # h -> custom value 3
        c4,                       # h -> custom value 4
    )

sensor.add_command("state", "hhhBhhhh", callback=state)
```
Hub side:
```python
link.add_command("state", "hhhBhhhh")

data = link.safe_call("state", default=None)

if data is not None:
    frame_id, line_error, junction, button, c1, c2, c3, c4 = data

    link.track_frame(frame_id, stale_after=3)

    if link.is_stale():
        # Your robot decides what to do:
        # stop, slow down, retry, ignore, etc.
        pass
```
---
Error handling
AstroPUP stores error information so your project can decide how to react.
Useful Hub-side methods:
```python
link.last_error()
link.last_error_text()
link.fail_count()
link.success_count()
link.call_count()
link.last_good_response()
```
Sensor-side diagnostics:
```python
sensor.last_error()
sensor.last_error_text()
sensor.process_count()
sensor.success_count()
sensor.fail_count()
sensor.report()
```
---
Performance notes
AstroPUP is designed to stay lightweight.
The heartbeat feature is optional.
If you do not call:
```python
track_frame(frame_id)
```
then stale-data tracking does not affect your robot logic.
If you use heartbeat tracking, the extra cost is small:
one extra value in your packet;
one comparison on the Hub;
a few counters updated in memory.
The heaviest parts of a robot are usually camera processing, I2C sensor reading, line calculations, motor control, and debug printing.
Avoid heavy `print()` use during competition runs.
---
Version
Current version: v0.3.0
---
License
AstroPUP contains code derived from PUPRemote.
PUPRemote is distributed under the GPL / GPL-3.0 license.
AstroPUP is released under GPL-3.0-compatible terms and keeps attribution to the original PUPRemote project.
See `CREDITS.md` and `LICENSE` for details.
---
Disclaimer
AstroPUP is not affiliated with, endorsed by, or sponsored by LEGO, Pybricks, or Anton's Mindstorms.
LEGO, SPIKE, MINDSTORMS, Powered Up, and related names are trademarks of their respective owners.
