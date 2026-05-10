\# AstroPUP Examples



This folder contains small example projects showing how to use AstroPUP with a LEGO hub running Pybricks and external MicroPython devices.



The examples are intentionally organized from very simple communication checks to more complete diagnostic and bridge patterns.



\---



\## Before using the examples



\### LEGO Hub side



For every hub-side example, copy this file to your Pybricks project:



```text

src/astropup\_hub.py

```



The hub program usually imports it like this:



```python

from astropup\_hub import AstroPUPHub

```



\---



\### External device side



For every external MicroPython device example, copy this file to the device:



```text

src/astropup\_sensor.py

```



The external device program usually imports it like this:



```python

from astropup\_sensor import AstroPUPSensor

```



Some devices also need:



```text

src/lpf2.py

```



Typical file requirements:



| Device / Environment | Files usually needed |

| --- | --- |

| LEGO Hub with Pybricks | `astropup\_hub.py` |

| LMS-ESP32 with PUPRemote firmware | `astropup\_sensor.py` |

| Generic ESP32 MicroPython | `astropup\_sensor.py` + `lpf2.py` |

| OpenMV | `astropup\_sensor.py` + `lpf2.py` |

| RP2040 MicroPython | `astropup\_sensor.py` + `lpf2.py` |



\---



\## Important rule



The hub side and the external device side must register commands in the same:



1\. order

2\. names

3\. formats



Example:



\### Sensor side



```python

link.add\_command("hello", "h", callback=hello)

```



\### Hub side



```python

link.add\_command("hello", "h")

```



If the command order or format does not match, communication may fail or return unexpected values.



\---



\## Recommended learning order



Start with the simplest examples first.



| Order | Example | Purpose |

| --- | --- | --- |

| 1 | `esp32\_hello\_world` | Minimal ESP32 communication test |

| 2 | `openmv\_hello\_camera` | Minimal OpenMV camera + communication test |

| 3 | `basic\_sensor` | Generic minimal hub/sensor pair |

| 4 | `startup\_diagnostics` | Startup report and mode validation |

| 5 | `pybricks\_multitask\_hub` | Pybricks multitask reading example |

| 6 | `heartbeat\_stale\_demo` | Heartbeat and stale-data detection |

| 7 | `astrogenius\_style\_bridge` | More realistic bridge-style example |



\---



\## Example descriptions



\### `esp32\_hello\_world`



The simplest ESP32 example.



The ESP32 prints a local message and returns a small number to the LEGO hub.



Use this first to confirm that the ESP32, LPF2 wiring, AstroPUP, and Pybricks hub communication are working.



\---



\### `openmv\_hello\_camera`



The simplest OpenMV example.



The OpenMV camera takes snapshots, prints a local message, and returns a frame counter to the LEGO hub.



This example does not detect colors or objects. It only confirms that the OpenMV camera loop and AstroPUP communication are working.



\---



\### `basic\_sensor`



A minimal complete pair using a generic external sensor/device and a LEGO hub.



Use this when you want a clean basic example that is not tied to ESP32 or OpenMV specifically.



\---



\### `startup\_diagnostics`



Shows how to use:



```python

startup\_report()

validate\_remote\_modes()

```



Use this when the hub and external device connect, but values do not look correct.



\---



\### `pybricks\_multitask\_hub`



Shows how to use AstroPUP with Pybricks multitasking.



Useful when your robot needs to keep reading external data while also running other robot actions.



\---



\### `heartbeat\_stale\_demo`



Demonstrates AstroPUP heartbeat / stale-data tracking.



Use this to check whether the hub is receiving fresh data or repeating old frames.



\---



\### `astrogenius\_style\_bridge`



A more realistic bridge-style example.



It shows how a project can send a packet with multiple values, such as:



```text

frame\_id, error, junction, button, c1, c2, c3, c4

```



This is only an example pattern. Robot-specific meanings should stay outside AstroPUP Core.



\---



\## Hardware testing



Automated tests do not replace real hardware validation.



After copying and running an example, validate the real communication path with:



```text

docs/HARDWARE\_TEST\_CHECKLIST.md

```



\---



\## Notes



AstroPUP Core should remain generic.



Do not put robot-specific mission logic, color tables, camera strategy, line sensor interpretation, or competition code inside the core library.



Keep project-specific code in your own files, such as:



```text

main.py

robot.py

sensors.py

profiles.py

```



