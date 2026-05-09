# AstroPUP Hardware Test Checklist

This checklist is for manual tests with real hardware.

Automated tests validate AstroPUP's internal logic on GitHub Actions.
This checklist validates the real LPF2 / Powered Up / Pybricks communication path.

## Basic setup

- [ ] Copy `src/astropup_hub.py` to the LEGO hub Pybricks project.
- [ ] Copy `src/astropup_sensor.py` to the external MicroPython device.
- [ ] Copy `src/lpf2.py` if the external device does not already include it.
- [ ] Connect the external device to the selected LEGO hub port.
- [ ] Use common GND and correct LPF2 wiring.
- [ ] Start the external device program before starting the hub program.

## Basic communication

- [ ] Run `examples/00_basic_counter_pair/sensor_main.py` on the external device.
- [ ] Run `examples/00_basic_counter_pair/hub_main.py` on the LEGO hub.
- [ ] Confirm the hub receives changing values.
- [ ] Confirm there are no mode order errors.

## Diagnostics

- [ ] Run the startup diagnostics example.
- [ ] Confirm `startup_report()` prints the expected command order.
- [ ] Confirm `validate_remote_modes()` returns `True`.

## Heartbeat

- [ ] Run the heartbeat demo.
- [ ] Confirm fresh frames are detected when `frame_id` changes.
- [ ] Confirm stale frames are detected when `frame_id` repeats.

## Notes

Record hardware, firmware, and wiring details here:

```text
Hub:
Pybricks version:
External device:
AstroPUP version:
Port:
Wiring:
Result:
```
