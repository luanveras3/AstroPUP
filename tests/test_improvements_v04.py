"""
Tests for AstroPUP v0.4.0 improvements:
  - safe_literal() replacing eval() in the data path
  - AstroPUPHub auto-reconnect on consecutive failures
  - resolve_port() replacing eval("Port." + ...)

Run with:  pytest -q
These tests use the mocks in conftest.py and need no hardware.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
import conftest  # noqa: F401  (installs micropython/pybricks/lpf2 mocks)

sys.path.insert(0, str(ROOT / "src"))

import astropup_hub
from astropup_hub import AstroPUPHub, safe_literal, resolve_port, ASTRO_OK, ASTRO_ERR_OS


# ---------------------------------------------------------------
# safe_literal: parses good data, never executes code
# ---------------------------------------------------------------

def test_safe_literal_parses_basic_types():
    assert safe_literal(b"123") == 123
    assert safe_literal(b"-45") == -45
    assert safe_literal(b"3.14") == 3.14
    assert safe_literal(b"'hello'") == "hello"
    assert safe_literal(b"True") is True
    assert safe_literal(b"None") is None
    assert safe_literal(b"") == ""


def test_safe_literal_parses_tuples_and_lists():
    assert safe_literal(b"(1, 2, 3)") == (1, 2, 3)
    assert safe_literal(b"[10, 20]") == [10, 20]
    assert safe_literal(b"(1, 'two', 3.0)") == (1, "two", 3.0)


def test_safe_literal_does_not_execute_code():
    # The whole point: a malicious/corrupted payload must NOT run.
    # eval() would raise or execute; safe_literal returns it as plain text.
    payload = b"__import__('os').system('echo pwned')"
    result = safe_literal(payload)
    assert isinstance(result, str)
    assert result == "__import__('os').system('echo pwned')"


def test_safe_literal_handles_garbage_bytes():
    # Non-UTF8 / noise on the wire must not crash.
    assert safe_literal(b"\xff\xfe\x00") == ""


# ---------------------------------------------------------------
# resolve_port: no more eval("Port." + ...)
# ---------------------------------------------------------------

def test_resolve_port_letters_and_numbers():
    from pybricks.parameters import Port
    assert resolve_port("A") is Port.A
    assert resolve_port("c") is Port.C        # case-insensitive
    assert resolve_port(2) is Port.B          # 1 -> A, 2 -> B
    assert resolve_port(Port.D) is Port.D     # already a Port


def test_resolve_port_rejects_unknown():
    import pytest
    with pytest.raises(ValueError):
        resolve_port("Z")
    with pytest.raises(ValueError):
        resolve_port(99)


# ---------------------------------------------------------------
# Auto-reconnect
# ---------------------------------------------------------------

def _make_hub():
    from pybricks.parameters import Port
    from pybricks.iodevices import PUPDevice
    # Pre-advertise the modes the test will register so add_command's
    # mode-validation assertions are satisfied (also covers reconnect,
    # which builds a new PUPDevice instance internally).
    PUPDevice.advertised_modes = [("state", 4)]
    hub = AstroPUPHub(Port.C, profile="competition", debug=False)
    hub.add_command("state", "hh")
    return hub


def test_reconnect_triggers_after_threshold(monkeypatch):
    hub = _make_hub()
    hub.reconnect_after(3)

    # Force every underlying call to fail with OSError.
    def boom(*a, **k):
        raise OSError("link down")
    hub._pup.call = boom

    # Count how many times reconnect() is invoked.
    calls = {"n": 0}
    real_reconnect = hub.reconnect
    def counting_reconnect():
        calls["n"] += 1
        return real_reconnect()
    hub.reconnect = counting_reconnect

    # 3 failures -> exactly one reconnect attempt, streak resets.
    for _ in range(3):
        hub.safe_call("state", default=(0, 0))

    assert calls["n"] == 1
    # After a successful reconnect the error state is cleared back to OK.
    assert hub.last_error() == ASTRO_OK
    assert hub.reconnect_count() == 1


def test_success_resets_fail_streak():
    hub = _make_hub()
    hub.reconnect_after(3)

    seq = {"i": 0}
    def flaky(*a, **k):
        seq["i"] += 1
        if seq["i"] <= 2:
            raise OSError("blip")
        return (7, 8)
    hub._pup.call = flaky

    hub.safe_call("state", default=None)   # fail 1
    hub.safe_call("state", default=None)   # fail 2
    assert hub.consecutive_fails() == 2

    result = hub.safe_call("state", default=None)  # success
    assert result == (7, 8)
    assert hub.consecutive_fails() == 0
    assert hub.reconnect_count() == 0       # never crossed threshold


def test_reconnect_can_be_disabled():
    hub = _make_hub()
    hub.reconnect_after(0)                   # disabled

    def boom(*a, **k):
        raise OSError("down")
    hub._pup.call = boom

    for _ in range(10):
        hub.safe_call("state", default=None)

    assert hub.reconnect_count() == 0        # never reconnected
