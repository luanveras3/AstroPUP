# Security Policy

AstroPUP is an educational and robotics communication helper library.

It is designed for LEGO Pybricks hubs and external MicroPython devices using LPF2 / Powered Up communication through the PUPRemote foundation.

---

## Supported versions

AstroPUP is currently in active early development.

| Version | Supported |
| --- | --- |
| v0.3.x | Yes |
| v0.2.x and earlier | No |

---

## Reporting a vulnerability or serious reliability issue

If you find a security issue, unsafe behavior, or serious reliability problem, please open a GitHub issue with as much detail as possible.

Please include:

- AstroPUP version
- LEGO hub model
- Pybricks version
- external device used
- external device firmware
- port used
- wiring / connection details
- minimal code example
- observed behavior
- expected behavior
- steps to reproduce the problem

---

## Hardware safety

AstroPUP does not control motors, batteries, power distribution, or physical wiring by itself.

Users are responsible for safe hardware usage, including:

- correct wiring
- correct voltage
- common ground where required
- safe battery usage
- safe mechanical design
- testing robots in a controlled environment

Always test communication and robot behavior carefully before using AstroPUP in a competition run or with moving mechanisms.

---

## Public issue guidance

When opening a public issue, please avoid sharing:

- private personal information
- private school information
- student information
- passwords, keys, or tokens
- sensitive network information

For normal bugs, examples, documentation issues, or feature requests, a regular GitHub issue is appropriate.
