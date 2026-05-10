# 05 - ESP32 Hello World

The simplest possible AstroPUP example for ESP32.

The ESP32 prints a local message and returns a small number to the LEGO hub.  
The LEGO hub prints its own message and prints the value received from the ESP32.

This example is only for confirming that the basic AstroPUP / LPF2 communication path is working.

## Architecture

```text
ESP32  ->  AstroPUP / LPF2  ->  LEGO Hub running Pybricks
```

## Copy to the ESP32

Copy these files to the ESP32:

```text
src/astropup_sensor.py
src/lpf2.py
examples/05_esp32_hello_world/esp32_main.py  ->  main.py
```

## Copy to the LEGO hub

Copy these files to the LEGO hub Pybricks project:

```text
src/astropup_hub.py
examples/05_esp32_hello_world/hub_main.py
```

## Command

| Command | Format | Meaning |
| --- | --- | --- |
| `hello` | `h` | returns a simple number from the ESP32 |

Both sides must register the same command name and format.
