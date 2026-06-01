"""
Test helpers for running AstroPUP tests on normal CPython.

These mocks allow GitHub Actions to import AstroPUP files without a real
LEGO hub, Pybricks firmware, LMS-ESP32, OpenMV, or LPF2 hardware.
"""

import sys
import types
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


# MicroPython compatibility -------------------------------------------------

micropython = types.ModuleType("micropython")
micropython.const = lambda value: value
sys.modules.setdefault("micropython", micropython)

sys.modules.setdefault("ustruct", struct)


# Pybricks compatibility ----------------------------------------------------

pybricks = types.ModuleType("pybricks")
pybricks_iodevices = types.ModuleType("pybricks.iodevices")
pybricks_tools = types.ModuleType("pybricks.tools")
pybricks_parameters = types.ModuleType("pybricks.parameters")


class _Port:
    """Stand-in for pybricks.parameters.Port enum."""
    A = "Port.A"
    B = "Port.B"
    C = "Port.C"
    D = "Port.D"
    E = "Port.E"
    F = "Port.F"


pybricks_parameters.Port = _Port


class FakePUPDevice:
    """Small fake PUPDevice used only for unit tests.

    Tests that exercise add_command (which validates against advertised
    modes) can populate FakePUPDevice.advertised_modes with a list of
    (name, size) tuples before constructing the hub. Any new instance
    created afterwards — including those built during auto-reconnect —
    snapshots the same list, so the validation lines up across reconnects.
    """

    advertised_modes = []

    def __init__(self, port=None):
        self.port = port
        self.writes = []
        self._modes = list(FakePUPDevice.advertised_modes)
        self._read_data = {}

    def info(self):
        return {"modes": self._modes}

    def write(self, mode, data):
        self.writes.append((mode, data))

    def read(self, mode):
        return self._read_data.get(mode, [0] * 16)


def wait(ms=0):
    return None


def run_task(*args, **kwargs):
    return False


pybricks_iodevices.PUPDevice = FakePUPDevice
pybricks_tools.wait = wait
pybricks_tools.run_task = run_task

sys.modules.setdefault("pybricks", pybricks)
sys.modules.setdefault("pybricks.iodevices", pybricks_iodevices)
sys.modules.setdefault("pybricks.tools", pybricks_tools)
sys.modules.setdefault("pybricks.parameters", pybricks_parameters)
# Make 'pybricks' behave as a package so 'from pybricks.parameters import Port' works.
pybricks.__path__ = []
pybricks.iodevices = pybricks_iodevices
pybricks.tools = pybricks_tools
pybricks.parameters = pybricks_parameters


# LPF2 compatibility --------------------------------------------------------

lpf2 = types.ModuleType("lpf2")
lpf2.DATA8 = 0
lpf2.ABSOLUTE = 1


class FakeLPF2:
    def __init__(self, modes=None, sensor_id=None, max_packet_size=16, **kwargs):
        self.modes = modes if modes is not None else []
        self.sensor_id = sensor_id
        self.max_packet_size = max_packet_size
        self.connected = False
        self.payloads = []

    def mode(self, name, size, data_type, writable):
        return (name, size, data_type, writable)

    def heartbeat(self):
        return None

    def send_payload(self, payload, mode):
        self.payloads.append(("send", mode, payload))

    def update_payload(self, payload, mode):
        self.payloads.append(("update", mode, payload))


lpf2.LPF2 = FakeLPF2
sys.modules.setdefault("lpf2", lpf2)
