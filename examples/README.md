# AstroPUP Better Examples

These examples are meant to replace the first simple examples in the repository.

Important:

- Copy `src/astropup_hub.py` to the LEGO Hub project folder when using hub examples.
- Copy `src/astropup_sensor.py` to the external MicroPython device when using sensor examples.
- The Hub and Sensor must register commands in the same order, with the same names, and the same formats.
- Keep AstroPUP Core generic. Put robot-specific packet formats and meanings in your own project files.

Recommended repository fix before using these examples:

- Make sure the Hub file is named `astropup_hub.py`, not `astropup.hub.py`.

Example order:

1. `00_basic_counter_pair` — simplest complete pair: external sensor + Pybricks hub.
2. `01_startup_diagnostics` — shows startup_report and mode validation.
3. `02_pybricks_multitask_reader` — safe_call_multitask example.
4. `03_heartbeat_stale_demo` — proves heartbeat/stale-data detection.
5. `04_saturn_style_bridge` — project-style example based on a line sensor + external values packet.
