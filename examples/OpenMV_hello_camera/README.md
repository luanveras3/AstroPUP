# 06 - OpenMV Hello Camera

The simplest possible AstroPUP example for OpenMV.

The OpenMV camera takes snapshots, prints a local message, and returns a frame counter to the LEGO hub.  
The LEGO hub prints its own message and prints the value received from the OpenMV.

This example does not detect colors or objects.  
It only confirms that the OpenMV + AstroPUP + LPF2 + Pybricks communication path is working.

## Architecture

```text
OpenMV Camera  ->  AstroPUP / LPF2  ->  LEGO Hub running Pybricks
```

## Copy to the OpenMV

Copy these files to the OpenMV board:

```text
src/astropup_sensor.py
src/lpf2.py
examples/OpenMV_hello_camera/openmv_main.py  ->  main.py
```

## Copy to the LEGO hub

Copy these files to the LEGO hub Pybricks project:

```text
src/astropup_hub.py
examples/OpenMV_hello_camera/hub_main.py
```

## Command

| Command | Format | Meaning |
| --- | --- | --- |
| `hello` | `h` | returns a simple frame counter from the OpenMV |

Both sides must register the same command name and format.
