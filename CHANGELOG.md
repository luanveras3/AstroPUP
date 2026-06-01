# Changelog
All notable changes to AstroPUP will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/), and this project follows GPL-3.0-compatible licensing due to its PUPRemote foundation.

## v0.4.0
### Security / robustness

- Removed `eval()` from the data path. The `"repr"` format now decodes through a new `safe_literal()` parser that handles numbers, strings, booleans, `None`, tuples, and lists without executing arbitrary code. A corrupted or hostile payload on the wire can no longer run code on either side.
- Replaced `eval("Port." + ...)` in `connect()` with a `resolve_port()` lookup table that accepts a letter, a number, or an already-built `Port`. This also fixes a latent bug where `Port` was used without being imported.

### Added

- `AstroPUPHub` automatic reconnection. After N consecutive failed `safe_call()` invocations (default 5), the hub rebuilds the underlying `PUPDevice` and re-registers every command in the original order. A successful call resets the failure streak.
  - `hub.reconnect_after(n)` to change the threshold (pass `0` to disable).
  - `hub.reconnect()` to force a reconnection manually.
  - `hub.reconnect_count()` to inspect how many times the link rebuilt itself.
  - `hub.consecutive_fails()` to read the current failure streak.
- `tests/test_improvements_v04.py` covering `safe_literal`, `resolve_port`, and the auto-reconnect flow.
- `tests/conftest.py` now mocks `pybricks.parameters.Port` and lets tests pre-populate `FakePUPDevice.advertised_modes` so reconnect tests can register commands.

### Notes

- Reconnect is enabled by default. Pass `reconnect_after=0` (or call `hub.reconnect_after(0)`) if you want the old fail-fast behaviour.
- The `"repr"` data format is still supported but `struct` formats (`B`, `h`, `hh`, `hhhh`...) are recommended for any production link.

---

## v0.3.2
### Added

- Added minimal ESP32 Hello World example.
- Added minimal OpenMV Hello Camera example.

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
