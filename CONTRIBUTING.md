# Contributing to AstroPUP

Thank you for your interest in contributing to AstroPUP.

AstroPUP is a lightweight safety and diagnostics layer built on top of PUPRemote for communication between LEGO Pybricks hubs and external MicroPython devices.

The goal is to keep AstroPUP simple, generic, reliable, and useful for the robotics community.

---

## Core principle

Please keep AstroPUP generic.

The core library should not include robot-specific logic such as:

- competition missions
- line sensor interpretation
- camera-specific logic
- color tables
- robot movement strategies
- team-specific code
- WRO / FLL / OBR-specific decisions

Robot-specific code should live in examples, user projects, profiles, or separate application files.

Good places for user-specific logic:

```text
main.py
robot.py
sensors.py
profiles.py
examples/
```

AstroPUP core should focus only on:

- communication
- safety
- diagnostics
- validation
- counters
- heartbeat / stale-data tracking
- MicroPython / Pybricks compatibility

---

## Development setup

Clone the repository:

```bash
git clone https://github.com/luanveras3/AstroPUP.git
cd AstroPUP
```

Install test dependencies:

```bash
pip install pytest
```

Run tests:

```bash
pytest -q
```

---

## Automated tests

AstroPUP includes automated tests that run on normal CPython through GitHub Actions.

These tests validate internal logic such as:

- module imports
- command order helpers
- heartbeat / stale-data tracking
- sensor-side frame ID helpers

Automated tests do not validate real LPF2 / Powered Up hardware communication.

For hardware validation, use:

```text
docs/HARDWARE_TEST_CHECKLIST.md
```

---

## Hardware testing

Changes that affect LPF2 / Powered Up communication should be tested with real hardware whenever possible.

Recommended hardware test path:

```text
External MicroPython device  <-->  LEGO Hub running Pybricks
```

Examples of external devices:

- LMS-ESP32
- OpenMV
- ESP32
- RP2040
- other MicroPython boards capable of LPF2 / Powered Up communication

Before reporting that hardware communication is working, please document:

- LEGO hub model
- Pybricks version
- external device model
- AstroPUP version
- port used
- wiring details
- example used
- result observed

---

## Pull request guidelines

Before opening a pull request:

- keep changes focused
- run `pytest -q`
- update documentation if behavior changes
- update examples if needed
- avoid breaking MicroPython / Pybricks compatibility
- avoid adding heavy dependencies
- preserve attribution to PUPRemote and Anton's Mindstorms
- keep robot-specific logic out of the core library

---

## Code style

AstroPUP should remain:

- simple
- readable
- MicroPython-friendly
- Pybricks-friendly
- beginner-friendly
- suitable for education and competition robotics

Prefer clear code over clever code.

Avoid features that make the library harder to understand or harder to run on constrained MicroPython devices.

---

## Credit and license

AstroPUP is built on top of PUPRemote by Anton's Mindstorms.

Any contribution must preserve the existing attribution and remain compatible with the repository license.

Please see:

```text
LICENSE
CREDITS.md
```
