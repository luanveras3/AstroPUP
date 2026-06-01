# LMS-ESP32 UART Bridge

Use the LMS-ESP32 as a **transparent bridge** between an external device that talks UART and the LEGO hub. The LMS-ESP32 does no processing - it only forwards the data.

```text
External device  --UART-->  LMS-ESP32  --LPF2/AstroPUP-->  LEGO Hub
```

Use this pattern whenever:

- The thing you want to read does not talk LPF2 (most cameras, most generic boards, custom electronics).
- The thing you want to read does not need to know anything about LEGO.
- You want to keep your robot logic on the hub and the data-producing logic on the external device.

The `LMS_ESP32_camera_bridge` example is the same pattern with an OpenMV camera in the place of the external device.

## Line protocol

The external device sends ASCII lines terminated by `\n`. Each line has two integers:

```text
value,frame_id\n
```

- `value` - any 16-bit signed integer (`-32768 .. 32767`)
- `frame_id` - a counter the external device increments every send (0 .. 32767). The hub uses it to spot a frozen external device.

This is plain text. No extra library required. Easy to debug with a serial terminal.

## Files

| File | Where it runs |
| --- | --- |
| `external_device_simulator.py` | any MicroPython board (stand-in for your real device) |
| `lms_esp32_bridge.py` | the LMS-ESP32, becomes `main.py` |
| `hub_main.py` | the LEGO hub Pybricks project |

## Wiring

| From | To |
| --- | --- |
| External device UART TX | LMS-ESP32 GPIO 16 (UART RX) |
| External device UART RX | LMS-ESP32 GPIO 17 (UART TX) - only needed if your device reads back from the hub |
| GND | GND |
| LMS-ESP32 flat LPF2 cable | any LEGO hub port |

**TX always goes to RX**. Picking the same pin name on both sides will not work.

The GPIO 16 / 17 default in `lms_esp32_bridge.py` is a sensible choice (free GPIOs, not strapping pins, not the LPF2 link). If you need different pins, change the constants at the top of `lms_esp32_bridge.py`. Avoid GPIO 0, 2, 12 and 15 (strapping) and the pins exposed by `from lms_esp32 import RX_PIN, TX_PIN` (those are reserved for the hub link).

## Copy to the external device

Use whatever workflow your board needs. As a starting point:

```text
examples/LMS_ESP32_uart_bridge/external_device_simulator.py  ->  main.py on the external board
```

Replace its body with your real sensor reading. Keep the line protocol.

## Copy to the LMS-ESP32

```text
src/astropup_sensor.py
examples/LMS_ESP32_uart_bridge/lms_esp32_bridge.py  ->  main.py
```

`lpf2.py` is **not** needed on the LMS-ESP32 - the firmware provides it.

## Copy to the LEGO hub

```text
src/astropup_hub.py
examples/LMS_ESP32_uart_bridge/hub_main.py
```

## Command

| Command | Format | Returns | Meaning |
| --- | --- | --- | --- |
| `state` | `hh` | `(value, frame_id)` | last value received from the external device, plus its frame counter |

The hub uses `track_frame(frame_id)` + `is_stale()` to warn when the external device stops sending new frames - a stuck or disconnected device is detected automatically.
