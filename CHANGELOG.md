# Changelog
All notable changes to AstroPUP will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/), and this project follows GPL-3.0-compatible licensing due to its PUPRemote foundation.

---

## v0.3.1
### Added

- Added automated tests with `pytest`.
- Added GitHub Actions workflow for continuous testing.
- Added hardware validation checklist in `docs/HARDWARE_TEST_CHECKLIST.md`.
- Added basic import tests for AstroPUP modules.
- Added tests for heartbeat / stale-data tracking.
- Added tests for sensor-side frame ID helpers.
- Added tests for command order helper behavior.

### Fixed

- Removed or fixed unresolved `Any` type annotation in `astropup_hub.py` to improve CPython test compatibility while keeping MicroPython / Pybricks compatibility.

### Notes

- Automated tests validate AstroPUP's internal logic only.
- Real LPF2 / Powered Up communication must still be tested with physical hardware.

---

## v0.3.0

Added:

- optional frame / heartbeat tracking;
- `track_frame(frame_id)`;
- `is_stale()`;
- `stale_count()`;
- `fresh_count()`;
- `last_frame_id()`;
- `current_frame_id()`;
- `reset_frame_tracker()`;
- sensor-side `next_frame_id()`;
- sensor-side `current_frame_id()`;
- sensor-side `reset_frame_id()`;
- heartbeat guide.

## v0.2.1

Added:

- `validate_remote_modes()`;
- `startup_report()`;
- `command_order()`;
- `call_count()`;
- `success_count()`;
- `fail_count()`;
- `last_good_response()`;
- improved diagnostics.

## v0.2.0

Changed:

- made AstroPUP Core generic;
- removed robot-specific presets from the core;
- separated project-specific command formats from the generic files.

## v0.1.x

Initial AstroPUP Hub and Sensor wrappers based on PUPRemote.
