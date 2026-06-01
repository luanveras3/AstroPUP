# LMS-ESP32 Hello World

The simplest possible AstroPUP example for the **LMS-ESP32** board (the ESP32 from Anton's Mindstorms that comes with a built-in LPF2/WeDo connector and pre-flashed MicroPython + PUPRemote firmware).

The LMS-ESP32 prints a local message and returns a small counter to the LEGO hub through AstroPUP.

This example is only for confirming that the basic AstroPUP / LPF2 communication path is working on the LMS-ESP32.

## Why a dedicated LMS-ESP32 example?

The board has a couple of conveniences that a generic ESP32 does not:

- It ships **pre-flashed** with MicroPython and the PUPRemote firmware. No need to flash anything.
- It has a **built-in LPF2/WeDo connector** wired to a 6-pin header. You plug the flat cable straight into the LEGO hub.
- You do **not** need to copy `lpf2.py` to the board - the firmware already exposes it.

If you have a generic ESP32 (DevKit, WROOM, etc.) instead, use the `ESP32_hello_world` example - that one shows the wiring and the extra files you need.

## Architecture

```text
LMS-ESP32  --LPF2/AstroPUP-->  LEGO Hub running Pybricks
```

## Wiring

| From | To |
| --- | --- |
| LMS-ESP32 6-pin header | Flat LPF2 cable (ships with the board) |
| Other end of the flat cable | Any port on the LEGO hub |

That is it. The flat cable carries power, ground, RX and TX in a single connector.

## Copy to the LMS-ESP32

```text
src/astropup_sensor.py
examples/LMS_ESP32_hello_world/lms_esp32_main.py  ->  main.py
```

You do **not** need `lpf2.py` on the LMS-ESP32 - the firmware provides it.

## Copy to the LEGO hub

```text
src/astropup_hub.py
examples/LMS_ESP32_hello_world/hub_main.py
```

## Command

| Command | Format | Returns | Meaning |
| --- | --- | --- | --- |
| `hello` | `h` | `(counter,)` | a small running counter from the LMS-ESP32 |

Both sides must register the same command name, format and order.

## What to expect

- The hub prints `Hello from LEGO Hub!` every second.
- The LMS-ESP32 prints `Hello from LMS-ESP32! Call: N` whenever the hub asks for `hello`.
- The hub prints the value it received.

If the hub keeps printing `No answer from LMS-ESP32.`, run through `docs/HARDWARE_TEST_CHECKLIST.md`.
