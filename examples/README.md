# AstroPUP Examples

This folder contains small example projects showing how to use AstroPUP with a LEGO hub running Pybricks and external MicroPython devices.

The examples are intentionally organised from very simple communication checks to more complete computer-vision and bridge patterns.

---

## Before using the examples

### LEGO Hub side

For every hub-side example, copy this file to your Pybricks project:

```text
src/astropup_hub.py
```

The hub program usually imports it like this:

```python
from astropup_hub import AstroPUPHub
```

### External device side

For every external MicroPython device example, copy this file to the device:

```text
src/astropup_sensor.py
```

The external device program usually imports it like this:

```python
from astropup_sensor import AstroPUPSensor
```

Some devices also need:

```text
src/lpf2.py
```

Typical file requirements:

| Device / Environment | Files usually needed |
| --- | --- |
| LEGO Hub with Pybricks | `astropup_hub.py` |
| LMS-ESP32 with PUPRemote firmware | `astropup_sensor.py` |
| Generic ESP32 MicroPython | `astropup_sensor.py` + `lpf2.py` |
| OpenMV | `astropup_sensor.py` + `lpf2.py` |
| RP2040 MicroPython | `astropup_sensor.py` + `lpf2.py` |

---

## Important rule

The hub side and the external device side must register commands in the same:

1. order
2. names
3. formats

Example:

### Sensor side

```python
link.add_command("hello", "h", callback=hello)
```

### Hub side

```python
link.add_command("hello", "h")
```

If the command order or format does not match, communication will fail or return unexpected values.

---

## Recommended learning order

Start with the simplest examples first.

### Foundations

| Order | Example | Purpose |
| --- | --- | --- |
| 1 | `ESP32_hello_world` | Minimal generic-ESP32 communication test |
| 2 | `OpenMV_hello_camera` | Minimal OpenMV camera + communication test |
| 3 | `basic_sensor` | Generic minimal hub/sensor pair |
| 4 | `startup_diagnostics` | Startup report and mode validation |
| 5 | `pybricks_multitask_hub` | Pybricks multitask reading example |
| 6 | `heartbeat_stale_demo` | Heartbeat and stale-data detection |
| 7 | `astrogenius_style_bridge` | Realistic packet shape with multiple values |

### LMS-ESP32 (Anton's Mindstorms board)

| Order | Example | Purpose |
| --- | --- | --- |
| 8 | `LMS_ESP32_hello_world` | Minimal example for the pre-flashed LMS-ESP32 board |
| 9 | `LMS_ESP32_uart_bridge` | Use the LMS-ESP32 as a transparent UART bridge for any external device |
| 10 | `LMS_ESP32_camera_bridge` | Full chain: OpenMV camera -> LMS-ESP32 bridge -> LEGO hub |

The LMS-ESP32 examples skip `lpf2.py` because the board ships pre-flashed with PUPRemote firmware that already provides it.

---

## Example descriptions

### `ESP32_hello_world`

The simplest ESP32 example. The ESP32 prints a local message and returns a small number to the LEGO hub. Use this first to confirm that the ESP32, LPF2 wiring, AstroPUP and Pybricks hub communication are working.

### `OpenMV_hello_camera`

The simplest OpenMV example. The OpenMV camera takes snapshots, prints a local message, and returns a frame counter to the LEGO hub. This example does not detect colors or objects - it only confirms that the OpenMV camera loop and AstroPUP communication are working.

### `basic_sensor`

A minimal complete pair using a generic external sensor/device and a LEGO hub. Use this when you want a clean basic example that is not tied to ESP32 or OpenMV specifically.

### `startup_diagnostics`

Shows how to use `startup_report()` and `validate_remote_modes()`. Use this when the hub and external device connect, but values do not look correct.

### `pybricks_multitask_hub`

Shows how to use AstroPUP with Pybricks multitasking. Useful when your robot needs to keep reading external data while also running other robot actions.

### `heartbeat_stale_demo`

Demonstrates AstroPUP heartbeat / stale-data tracking. Use this to check whether the hub is receiving fresh data or repeating old frames.

### `astrogenius_style_bridge`

A more realistic bridge-style example. It shows how a project can send a packet with multiple values, such as `frame_id, error, junction, button, c1, c2, c3, c4`. This is only a pattern - robot-specific meanings should stay outside AstroPUP Core.

### `LMS_ESP32_hello_world`

Minimal example for the **LMS-ESP32** board (Anton's Mindstorms ESP32 with built-in LPF2/WeDo connector and pre-flashed PUPRemote firmware). Highlights the conveniences of the board: no firmware flashing, no `lpf2.py` copy, and a flat LPF2 cable straight into the LEGO hub.

### `LMS_ESP32_uart_bridge`

Use the LMS-ESP32 as a **transparent UART bridge** for any external device (another MicroPython board, an Arduino, a custom sensor with UART). The external device sends `value,frame_id\n` over UART, the LMS-ESP32 forwards it to the hub. Includes an `external_device_simulator.py` so you can try the pattern without a second device.

### `LMS_ESP32_camera_bridge`

Full chain showing an **OpenMV camera reaching the LEGO hub through an LMS-ESP32 bridge**. The OpenMV does all the computer vision (`find_blobs`, drawing, thresholds) and only sends a small result line. The LMS-ESP32 forwards. The hub never talks to the camera directly. Generic blob tracker - not tied to any competition.

---

## Hardware testing

Automated tests do not replace real hardware validation.

After copying and running an example, validate the real communication path with:

```text
docs/HARDWARE_TEST_CHECKLIST.md
```

---

## Notes

AstroPUP Core should remain generic.

Do not put robot-specific mission logic, color tables, camera strategy, line sensor interpretation, or competition code inside the core library.

Keep project-specific code in your own files, such as:

```text
main.py
robot.py
sensors.py
profiles.py
```
