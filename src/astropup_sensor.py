# ============================================================
# AstroPUP Sensor Generic Core v0.3.0
# Astrogenius from Brazil
# ============================================================
#
# Project: AstroPUP
# Module: AstroPUP Sensor Generic Core
# Maintainer: Luan Veras
# Team Instagram: @astrogenius.team
#
# Purpose:
#   AstroPUP Sensor is a generic, competition-oriented and
#   education-friendly single-file communication layer for external
#   MicroPython devices that emulate LEGO LPF2/PUP devices.
#
#   This file is intentionally generic.
#   It does NOT include robot-specific logic, camera-specific logic,
#   line-sensor logic, color maps, mission logic, or team strategy.
#
#   Project-specific behavior must be implemented in your own sensor
#   program, such as main.py, robot_sensor.py, or a profile file.
#
# Typical sensor-side usage:
#
#   from astropup_sensor import AstroPUPSensor
#
#   def reset():
#       return 1
#
#   def state():
#       return (123, 1)
#
#   sensor = AstroPUPSensor(profile="competition")
#
#   # Commands MUST match the hub-side order, names and formats.
#   sensor.add_command("reset", "B", callback=reset)
#   sensor.add_command("state", "hh", callback=state)
#
#   while True:
#       sensor.safe_process()
#
# Original foundation:
#   PUPRemote by Anton's Mindstorms
#   Original project: https://github.com/antonvh/PUPRemote
#   Original authors: Anton Vanhoucke & Ste7an
#
# License and attribution:
#   This file includes code derived from PUPRemote.
#   PUPRemote is distributed under the GPL/GPL-3.0 license.
#   AstroPUP keeps attribution to the original project and adds
#   Astrogenius-specific improvements on top.
#
# AstroPUP generic additions:
#   - callback-based add_command()
#   - add_callback()
#   - safe_process()
#   - standardized ASTRO_ERR_* error codes
#   - command order diagnostics
#   - competition/debug profiles
#   - readable reports
#   - process/failure counters
#   - command registration order helpers
#   - optional frame_id generator for heartbeat/stale-data systems
#
# Important:
#   This single-file version keeps the low-level PUPRemote behavior
#   as close as possible to the original to preserve compatibility.
#   AstroPUP adds a safer and clearer layer above it.
#
# ============================================================

__version__ = "0.3.0"
__project__ = "AstroPUP"
__team__ = "Astrogenius - Brazil"
__instagram__ = "@astrogenius.team"
__maintainer__ = "Luan Veras"
__foundation__ = "PUPRemote by Anton's Mindstorms"

# ============================================================
# PART 1 - VENDORED PUPREMOTE SENSOR FOUNDATION
# ============================================================
#
# This section is based on PUPRemote by Anton's Mindstorms.
# It keeps the sensor-side LPF2/PUPRemote behavior close to the
# original project to preserve compatibility with Pybricks hubs.
#
# AstroPUP change in this section:
#   PUPRemoteSensor.add_command() accepts an optional callback.
#   This avoids depending only on eval(mode_name), making the code
#   easier to understand and safer to maintain.
#
# ============================================================

try:
    from micropython import const
except ImportError:
    def const(x):
        return x

try:
    import asyncio
except ImportError:
    asyncio = None

try:
    import struct
except ImportError:
    import ustruct as struct

try:
    from collections import deque
except ImportError:
    deque = None

import lpf2

MAX_PKT = const(16)
MAX_COMMANDS = const(16)
MAX_COMMAND_QUEUE_LENGTH = const(10)

DONE = const(0)
RESULT = const(1)
ERROR = const(2)

NAME = const(0)
SIZE = const(1)
TO_HUB_FORMAT = const(2)
FROM_HUB_FORMAT = const(3)
CALLABLE = const(4)
ARGS_TO_HUB = const(5)
ARGS_FROM_HUB = const(6)

WEDO_ULTRASONIC = const(35)
SPIKE_COLOR = const(61)
SPIKE_ULTRASONIC = const(62)

CALLBACK = const(0)
CHANNEL = const(1)


class PUPRemote:
    """Base command/format encoder used by PUPRemoteSensor."""

    def __init__(self, max_packet_size=MAX_PKT):
        self.commands = []
        self.modes = {}
        self.max_packet_size = max_packet_size

    def add_channel(self, mode_name, to_hub_fmt=""):
        self.add_command(mode_name, to_hub_fmt=to_hub_fmt, command_type=CHANNEL)

    def add_command(self, mode_name, to_hub_fmt="", from_hub_fmt="", command_type=CALLBACK):
        if to_hub_fmt == "repr" or from_hub_fmt == "repr":
            msg_size = self.max_packet_size
            num_args_from_hub = -1
            num_args_to_hub = -1
        else:
            size_to_hub_fmt = struct.calcsize(to_hub_fmt)
            size_from_hub_fmt = struct.calcsize(from_hub_fmt)
            msg_size = max(size_to_hub_fmt, size_from_hub_fmt)
            num_args_to_hub = len(
                struct.unpack(to_hub_fmt, bytearray(struct.calcsize(to_hub_fmt)))
            )
            num_args_from_hub = len(
                struct.unpack(from_hub_fmt, bytearray(struct.calcsize(from_hub_fmt)))
            )

        assert len(self.commands) < MAX_COMMANDS, "Command limit exceeded"
        assert msg_size <= self.max_packet_size, "Payload exceeds maximum packet size"

        self.commands.append(
            {
                NAME: mode_name,
                TO_HUB_FORMAT: to_hub_fmt,
                SIZE: msg_size,
                ARGS_TO_HUB: num_args_to_hub,
            }
        )

        if command_type == CALLBACK:
            self.commands[-1][FROM_HUB_FORMAT] = from_hub_fmt
            self.commands[-1][ARGS_FROM_HUB] = num_args_from_hub

        self.modes[mode_name] = len(self.commands) - 1

    def decode(self, fmt, data):
        if fmt == "repr":
            clean = bytearray([c for c in data if c != 0])
            if clean:
                return (eval(clean),)
            return ("",)
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, data[:size])

    def encode(self, size, fmt, *argv):
        if fmt == "repr":
            s = bytes(repr(*argv), "UTF-8")
        else:
            s = struct.pack(fmt, *argv)
        assert len(s) <= size, "Payload exceeds maximum packet size"
        return s


class PUPRemoteSensor(PUPRemote):
    """Sensor-side PUPRemote device emulator."""

    def __init__(self, sensor_id=SPIKE_ULTRASONIC, power=False, max_packet_size=MAX_PKT, **kwargs):
        super().__init__(max_packet_size)
        self.connected = False
        self.power = power
        self.mode_names = []
        self.max_packet_size = max_packet_size
        self.lpup = lpf2.LPF2([], sensor_id=sensor_id, max_packet_size=max_packet_size)

        if deque is not None:
            self._callback_queue = deque((), MAX_COMMAND_QUEUE_LENGTH)
        else:
            self._callback_queue = []

        if asyncio is not None:
            self._callback_lock = asyncio.Lock()
        else:
            self._callback_lock = None

    def add_command(self, mode_name, to_hub_fmt="", from_hub_fmt="", command_type=CALLBACK, callback=None):
        super().add_command(mode_name, to_hub_fmt, from_hub_fmt, command_type)

        writeable = 0

        if command_type == CALLBACK:
            if callback is not None:
                self.commands[-1][CALLABLE] = callback
            else:
                # Original PUPRemote behavior: function name must match mode name.
                # AstroPUP recommends passing callback=your_function explicitly.
                self.commands[-1][CALLABLE] = eval(mode_name)

        if from_hub_fmt != "":
            writeable = lpf2.ABSOLUTE

        max_mode_name_len = 5 if self.power else 11
        assert len(mode_name) <= max_mode_name_len, "Name length must be <= {} with power={}".format(
            max_mode_name_len, self.power
        )

        lpf2_mode_name = mode_name
        if self.power:
            lpf2_mode_name = (
                mode_name.encode("ascii")
                + b" " * (5 - len(mode_name))
                + b"\x00\x80\x00\x00\x00\x05\x04"
            )

        self.lpup.modes.append(
            self.lpup.mode(
                lpf2_mode_name,
                self.commands[-1][SIZE],
                lpf2.DATA8,
                writeable,
            )
        )

    def _send_response(self, mode, result):
        num_args = self.commands[mode][ARGS_TO_HUB]

        if result is None:
            assert num_args <= 0, "{}() did not return value(s)".format(
                self.commands[mode][NAME]
            )
            return

        if not isinstance(result, tuple):
            result = (result,)

        if num_args >= 0:
            assert num_args == len(result), "{}() returned {} value(s) instead of expected {}".format(
                self.commands[mode][NAME], len(result), num_args
            )

        pl = self.encode(
            self.commands[mode][SIZE],
            self.commands[mode][TO_HUB_FORMAT],
            *result,
        )
        self.lpup.send_payload(pl, mode)

    def process(self):
        """Process hub communication once. Call frequently in the main loop."""
        data = self.lpup.heartbeat()
        if data is not None:
            pl, mode = data
            if CALLABLE in self.commands[mode]:
                args = self.decode(self.commands[mode][FROM_HUB_FORMAT], pl)
                result = self.commands[mode][CALLABLE](*args)
                self._send_response(mode, result)
        return self.lpup.connected

    def update_channel(self, mode_name, *argv):
        mode = self.modes[mode_name]
        pl = self.encode(
            self.commands[mode][SIZE],
            self.commands[mode][TO_HUB_FORMAT],
            *argv
        )
        self.lpup.update_payload(pl, mode)

    async def _heartbeat_loop(self, interval_ms):
        while True:
            data = self.lpup.heartbeat()
            if data:
                async with self._callback_lock:
                    self._callback_queue.append(data)
            await asyncio.sleep(interval_ms / 1000)

    async def _process_callbacks(self):
        while True:
            await asyncio.sleep(0)
            async with self._callback_lock:
                if self._callback_queue:
                    pl, mode = self._callback_queue.popleft()
                else:
                    continue

            if CALLABLE in self.commands[mode]:
                args = self.decode(self.commands[mode][FROM_HUB_FORMAT], pl)
                result = await self.commands[mode][CALLABLE](*args)
                self._send_response(mode, result)

    async def process_async(self, interval_ms=50):
        hb_task = asyncio.create_task(self._heartbeat_loop(interval_ms))
        cb_task = asyncio.create_task(self._process_callbacks())
        await asyncio.gather(hb_task, cb_task)


# ============================================================
# PART 2 - ASTROPUP SENSOR EXTENSIONS
# ============================================================
#
# This section contains Astrogenius additions for safer setup,
# clearer diagnostics, and easier command registration.
#
# ============================================================

ASTRO_OK = const(0)
ASTRO_ERR_UNKNOWN = const(1)
ASTRO_ERR_COMMAND = const(2)
ASTRO_ERR_PROCESS = const(3)


class AstroPUPSensor(PUPRemoteSensor):
    """Astrogenius sensor-side wrapper for LPF2/PUPRemote devices."""

    def __init__(self, sensor_id=SPIKE_ULTRASONIC, power=False, max_packet_size=MAX_PKT, profile="competition", debug=False):
        super().__init__(sensor_id=sensor_id, power=power, max_packet_size=max_packet_size)
        self.profile = profile
        self.debug = debug
        self._last_error = ASTRO_OK
        self._last_exception = None
        self._process_count = 0
        self._fail_count = 0
        self._success_count = 0
        self._command_order = []

        # Optional project-level frame/heartbeat counter.
        # AstroPUP Core does not force this into any packet.
        # Your project callback may call next_frame_id() and include it in its own return tuple.
        self._frame_id = 0

    def add_command(self, mode_name, to_hub_fmt="", from_hub_fmt="", command_type=CALLBACK, callback=None):
        try:
            super().add_command(
                mode_name,
                to_hub_fmt=to_hub_fmt,
                from_hub_fmt=from_hub_fmt,
                command_type=command_type,
                callback=callback,
            )
            self._command_order.append(mode_name)
            self._last_error = ASTRO_OK
            self._last_exception = None
        except Exception as e:
            self._last_error = ASTRO_ERR_COMMAND
            self._last_exception = e
            if self.debug:
                print("ASTROPUP SENSOR COMMAND ERROR:", e)
            raise

    def add_callback(self, mode_name, to_hub_fmt="", callback=None, from_hub_fmt=""):
        """Clearer AstroPUP name for registering a remote command callback."""
        self.add_command(
            mode_name,
            to_hub_fmt=to_hub_fmt,
            from_hub_fmt=from_hub_fmt,
            command_type=CALLBACK,
            callback=callback,
        )

    def safe_process(self):
        """Process communication once without crashing the user loop."""
        try:
            connected = self.process()
            self._process_count += 1
            self._success_count += 1
            self._last_error = ASTRO_OK
            self._last_exception = None
            return connected
        except Exception as e:
            self._last_error = ASTRO_ERR_PROCESS
            self._last_exception = e
            self._fail_count += 1
            if self.debug:
                print("ASTROPUP SENSOR PROCESS ERROR:", e)
            return False

    def register_commands(self, command_specs):
        """Register several commands from a generic command specification.

        command_specs must be an iterable of tuples. Supported forms:

            ("name", "to_hub_fmt", callback)
            ("name", "to_hub_fmt", "from_hub_fmt", callback)

        The order must be exactly the same as the hub-side order.

        Example:
            sensor.register_commands([
                ("reset", "B", reset),
                ("state", "hh", state),
            ])
        """
        for spec in command_specs:
            if len(spec) == 3:
                mode_name, to_hub_fmt, callback = spec
                from_hub_fmt = ""
            elif len(spec) == 4:
                mode_name, to_hub_fmt, from_hub_fmt, callback = spec
            else:
                self._last_error = ASTRO_ERR_COMMAND
                raise ValueError("Command spec must be (name, to_hub_fmt, callback) or (name, to_hub_fmt, from_hub_fmt, callback).")
            self.add_command(
                mode_name,
                to_hub_fmt=to_hub_fmt,
                from_hub_fmt=from_hub_fmt,
                callback=callback,
            )

    def identity(self):
        """Return the AstroPUP identity string."""
        return (
            __project__
            + " Sensor Generic Core v"
            + __version__
            + " | "
            + __team__
            + " | "
            + __instagram__
            + " | Based on "
            + __foundation__
        )

    def commands(self):
        """Return registered commands in registration order."""
        return tuple(self._command_order)

    def command_order(self):
        """Return registered commands in registration order."""
        return tuple(self._command_order)

    def process_count(self):
        return self._process_count

    def success_count(self):
        return self._success_count

    def fail_count(self):
        return self._fail_count

    # --------------------------------------------------------
    # Optional frame / heartbeat helper
    # --------------------------------------------------------
    def next_frame_id(self, max_value=32767):
        """Increment and return a generic frame_id.

        This is optional. AstroPUP does not force a frame_id into any packet.
        Your own callback can include this value in its return tuple.

        The default max_value is 32767 so it is safe for a signed 16-bit "h"
        field if your project uses that format.
        """
        self._frame_id += 1

        if self._frame_id > max_value:
            self._frame_id = 0

        return self._frame_id

    def current_frame_id(self):
        """Return the current optional frame_id value."""
        return self._frame_id

    def reset_frame_id(self, value=0):
        """Reset the optional frame_id counter."""
        self._frame_id = value

    def reset_errors(self):
        """Clear diagnostic error state without reconnecting the device."""
        self._last_error = ASTRO_OK
        self._last_exception = None
        self._process_count = 0
        self._success_count = 0
        self._fail_count = 0

    def last_error(self):
        return self._last_error

    def last_error_text(self):
        if self._last_error == ASTRO_OK:
            return "ASTRO_OK"
        if self._last_error == ASTRO_ERR_UNKNOWN:
            return "ASTRO_ERR_UNKNOWN"
        if self._last_error == ASTRO_ERR_COMMAND:
            return "ASTRO_ERR_COMMAND"
        if self._last_error == ASTRO_ERR_PROCESS:
            return "ASTRO_ERR_PROCESS"
        return "ASTRO_ERR_UNDEFINED"

    def report(self):
        return (
            "AstroPUPSensor("
            + "project=" + __project__
            + ", version=" + __version__
            + ", team=" + __team__
            + ", instagram=" + __instagram__
            + ", profile=" + str(self.profile)
            + ", last_error=" + self.last_error_text()
            + ", process_count=" + str(self._process_count)
            + ", success=" + str(self._success_count)
            + ", fail_count=" + str(self._fail_count)
            + ", frame_id=" + str(self._frame_id)
            + ", commands_order=" + str(self._command_order)
            + ")"
        )
