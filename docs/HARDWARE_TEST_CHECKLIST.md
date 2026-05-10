# AstroPUP Hardware Test Checklist

This checklist is for manual tests with real hardware.

Automated tests validate AstroPUP's internal logic on GitHub Actions. This checklist validates the real LPF2 / Powered Up / Pybricks communication path.

---

## Basic setup

- [ ] Copy `src/astropup_hub.py` to the LEGO hub Pybricks project.
- [ ] Copy `src/astropup_sensor.py` to the external MicroPython device.
- [ ] Copy `src/lpf2.py` if the external device does not already include it.
- [ ] Connect the external device to the selected LEGO hub port.
- [ ] Use common GND and correct LPF2 wiring.
- [ ] Start the external device program before starting the hub program.

---

## Quick hardware test: ESP32

Use this when testing a generic ESP32 MicroPython board.

- [ ] Copy `src/astropup_sensor.py` to the ESP32.
- [ ] Copy `src/lpf2.py` to the ESP32.
- [ ] Copy `examples/esp32_hello_world/esp32_main.py` to the ESP32 as `main.py`.
- [ ] Copy `src/astropup_hub.py` to the LEGO hub Pybricks project.
- [ ] Copy `examples/esp32_hello_world/hub_main.py` to the LEGO hub Pybricks project.
- [ ] Connect the ESP32 to the selected LEGO hub port.
- [ ] Run the ESP32 program.
- [ ] Run the hub program.
- [ ] Confirm the ESP32 prints `Hello from ESP32`.
- [ ] Confirm the hub prints `ESP32 answered`.

---

## Quick hardware test: OpenMV

Use this when testing an OpenMV camera.

- [ ] Copy `src/astropup_sensor.py` to the OpenMV board.
- [ ] Copy `src/lpf2.py` to the OpenMV board.
- [ ] Copy `examples/openmv_hello_camera/openmv_main.py` to the OpenMV as `main.py`.
- [ ] Copy `src/astropup_hub.py` to the LEGO hub Pybricks project.
- [ ] Copy `examples/openmv_hello_camera/hub_main.py` to the LEGO hub Pybricks project.
- [ ] Connect the OpenMV to the selected LEGO hub port.
- [ ] Run the OpenMV program.
- [ ] Run the hub program.
- [ ] Confirm the OpenMV prints `Hello from OpenMV camera`.
- [ ] Confirm the hub prints `OpenMV answered`.

---

## Generic basic communication test

Use this after the hello examples.

- [ ] Run `examples/basic_sensor/sensor_main.py` on the external device.
- [ ] Run `examples/basic_sensor/hub_main.py` on the LEGO hub.
- [ ] Confirm the hub receives changing values.
- [ ] Confirm there are no mode order errors.

---

## Diagnostics

- [ ] Run `examples/startup_diagnostics/hub_main.py` on the LEGO hub.
- [ ] Confirm `startup_report()` prints the expected command order.
- [ ] Confirm `validate_remote_modes()` returns `True`.

---

## Heartbeat

- [ ] Run `examples/heartbeat_stale_demo/sensor_main.py` on the external device.
- [ ] Run `examples/heartbeat_stale_demo/hub_main.py` on the LEGO hub.
- [ ] Confirm fresh frames are detected when `frame_id` changes.
- [ ] Confirm stale frames are detected when `frame_id` repeats.

---

## Bridge-style packet

Use this only after basic communication is stable.

- [ ] Run `examples/astrogenius_style_bridge/sensor_lms_main_example.py` on the external device.
- [ ] Run `examples/astrogenius_style_bridge/hub_read_example.py` on the LEGO hub.
- [ ] Confirm the hub receives a full packet.
- [ ] Confirm the packet format matches on both sides.
- [ ] Confirm robot-specific meanings are documented outside AstroPUP Core.

---

## Notes

Record hardware, firmware, and wiring details here:

```text
Hub:
Pybricks version:
External device:
External firmware:
AstroPUP version:
Hub port:
Wiring:
Example used:
Result:
```
