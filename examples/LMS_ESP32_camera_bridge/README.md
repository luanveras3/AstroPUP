# LMS-ESP32 Camera Bridge

Full chain showing an OpenMV camera reaching a LEGO hub through an LMS-ESP32 bridge.

```text
OpenMV (vision)  --UART-->  LMS-ESP32 (bridge)  --LPF2/AstroPUP-->  LEGO Hub
```

The OpenMV does **all** the computer vision (`find_blobs`, thresholds, drawing) and only sends a small result line over UART. The LMS-ESP32 reads that line and re-publishes it to the hub through AstroPUP. The hub never talks to the camera directly.

Use this pattern when:

- You also need the LMS-ESP32 for other things (extra sensors, longer cables, future Wi-Fi).
- You want a clean separation: vision logic on the camera, robot logic on the hub.

If your camera can plug **directly** into a LEGO hub port and you do not need an ESP32 in between, the simpler topology is `OpenMV_hello_camera` (direct) or any of the direct examples - no bridge needed.

> This example uses a **generic** color blob tracker. It is intentionally not tied to any competition. If you need rescue / OBR specific logic (silver victims, green triangle, state machine), that material is delivered separately under consultancy.

## Files

| File | Where it runs |
| --- | --- |
| `openmv_blob_tracker.py` | OpenMV, becomes `main.py` |
| `lms_esp32_bridge.py` | LMS-ESP32, becomes `main.py` |
| `hub_main.py` | LEGO hub Pybricks project |

## Wiring

| From | To |
| --- | --- |
| OpenMV P4 (TX) | LMS-ESP32 GPIO 16 (UART RX) |
| OpenMV P5 (RX) | LMS-ESP32 GPIO 17 (UART TX) |
| OpenMV GND | LMS-ESP32 GND |
| OpenMV 3.3V | LMS-ESP32 3.3V |
| LMS-ESP32 flat LPF2 cable | any LEGO hub port |

**TX always goes to RX**. Picking the same pin name on both sides will not work.

Default ESP32 pins (16/17) can be changed at the top of `lms_esp32_bridge.py`. Avoid GPIO 0, 2, 12 and 15 (strapping) and the pins exposed by `from lms_esp32 import RX_PIN, TX_PIN` (those carry the LPF2 link to the hub).

## Line protocol (OpenMV -> LMS-ESP32)

Plain ASCII, terminated by `\n`:

```text
found,cx,cy,area,frame_id\n
```

- `found`  - `0` or `1`
- `cx,cy`  - center of the blob in pixels
- `area`   - blob area in pixels
- `frame_id` - increments every camera frame (0 .. 32767, wraps)

## AstroPUP command (LMS-ESP32 -> hub)

| Command | Format | Returns | Meaning |
| --- | --- | --- | --- |
| `vision` | `Bhhhh` | `(found, cx, cy, area, frame_id)` | latest vision result the LMS-ESP32 received |

The hub uses `track_frame(frame_id)` + `is_stale()` to detect a stuck camera (same `frame_id` arriving over and over).

## Tuning checklist

1. Open `openmv_blob_tracker.py` in the OpenMV IDE.
2. Use Tools > Machine Vision > Threshold Editor under the real lighting to set `TARGET_THRESHOLD` for whatever object you want to track.
3. Adjust `MIN_AREA` so small noise blobs are ignored but the real target still passes.
4. Auto gain and white balance are disabled in the file - leave them off so the thresholds stay stable.
5. If you change the ESP32 UART pins, mirror the change at the top of `lms_esp32_bridge.py`.

## Copy to the OpenMV

```text
examples/LMS_ESP32_camera_bridge/openmv_blob_tracker.py  ->  main.py
```

The OpenMV in this topology does **not** need `astropup_sensor.py` or `lpf2.py` - it only talks UART.

## Copy to the LMS-ESP32

```text
src/astropup_sensor.py
examples/LMS_ESP32_camera_bridge/lms_esp32_bridge.py  ->  main.py
```

`lpf2.py` is **not** needed - the LMS-ESP32 firmware provides it.

## Copy to the LEGO hub

```text
src/astropup_hub.py
examples/LMS_ESP32_camera_bridge/hub_main.py
```
