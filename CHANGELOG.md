# Changelog

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
