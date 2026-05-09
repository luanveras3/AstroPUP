# ============================================================
# AstroPUP Hub Generic Core v0.3.0
# Astrogenius from Brazil
# ============================================================
#
# Project: AstroPUP
# Module: AstroPUP Hub Generic Core
# Maintainer: Luan Veras
# Team Instagram: @astrogenius.team
#
# Purpose:
#   AstroPUP Hub is a generic, competition-oriented and
#   education-friendly single-file communication layer for LEGO
#   Pybricks hubs.
#
#   This file is intentionally generic.
#   It does NOT include robot-specific logic, camera-specific logic,
#   line-sensor logic, color maps, mission logic, or team strategy.
#
#   Project-specific behavior must be implemented in your own robot
#   files, such as main.py, robot.py, sensors.py, or a profile file.
#
# Typical hub-side usage:
#
#   from pybricks.parameters import Port
#   from astropup_hub import AstroPUPHub
#
#   link = AstroPUPHub(Port.C, profile="competition")
#
#   # Commands MUST match the sensor-side order, names and formats.
#   link.add_command("reset", "B")
#   link.add_command("state", "hh")
#
#   data = link.safe_call("state", default=(0, 0))
#
# Typical Pybricks multitask usage:
#
#   async def pup_loop():
#       while True:
#           await link.process_async()
#           await wait(0)
#
#   async def read_loop():
#       while True:
#           data = await link.safe_call_multitask("state", default=None)
#           await wait(0)
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
#   - safe_call()
#   - safe_call_multitask()
#   - standardized ASTRO_ERR_* error codes
#   - remote mode diagnostics
#   - generic command registration helpers
#   - competition/debug profiles
#   - readable reports with command registration order
#   - remote mode validation
#   - startup reports
#   - call/success/failure counters
#   - last good response storage
#   - optional frame/heartbeat tracking
#   - stale-data detection helpers
#
# Important:
#   This single-file version keeps the low-level PUPRemoteHub behavior
#   as close as possible to the original to preserve compatibility.
#   AstroPUP adds a safer and clearer layer above it.
#
# ============================================================

# Original PUPRemoteHub metadata.
__pupremote_author__ = "Anton Vanhoucke & Ste7an"
__pupremote_copyright__ = "Copyright 2023,2024 AntonsMindstorms.com"
__pupremote_license__ = "GPL / GPL-3.0"
__pupremote_version__ = "2.1"
__pupremote_status__ = "Production"

# AstroPUP project metadata.
__project__ = "AstroPUP"
__version__ = "0.3.0"
__author__ = "Luan Veras / Astrogenius"
__maintainer__ = "Luan Veras"
__instagram__ = "@astrogenius.team"
__team__ = "Astrogenius - Brazil"
__license__ = "GPL-3.0 compatible; includes code derived from PUPRemote"

import ustruct as struct
from pybricks.iodevices import PUPDevice
from pybricks.tools import wait, run_task
from micropython import const

MAX_PKT = const(16)

# Result holder indices
DONE = const(0)
RESULT = const(1)
ERROR = const(2)

# Dictionary keys
NAME = const(0)
SIZE = const(1)
TO_HUB_FORMAT = const(2)
FROM_HUB_FORMAT = const(3)
ARGS_TO_HUB = const(5)
ARGS_FROM_HUB = const(6)
CALLBACK = const(0)
CHANNEL = const(1)


def connect(port):
    """
    Connect to LMS-ESP32. Pass Port as a string ('A') or a number (1=Port.A)
    """
    global pr
    if isinstance(port, str):
        pyport = eval("Port." + port)
    if isinstance(port, int):
        pyport = eval("Port." + chr(64 + port))
    pr = PUPRemoteHub(pyport)


def call(*args):
    try:
        return pr.call(*args)
    except:
        print("Use the connect & add_channel or add_command blocks before call")
        raise


def add_channel(name, encoding):
    try:
        pr.add_channel(name, encoding)
    except:
        print("Use the connect command before adding a channel")
        raise


def add_command(name, to_hub, from_hub):
    try:
        pr.add_command(name, to_hub_fmt=to_hub, from_hub_fmt=from_hub)
    except:
        print("Use the connect command before adding a command")
        raise


def call_multitask(*args, **kwargs):
    try:
        return pr.call_multitask(*args, **kwargs)
    except:
        print(
            "Use the connect & add_channel or add_command blocks before call_multitask"
        )
        raise


def process_async():
    try:
        return pr.process_async()
    except:
        print("Use the connect command before starting process_async")
        raise


class PUPRemote:
    """Base class for PUPRemoteHub on Pybricks.

    Defines a list of commands and their formats. Contains encoding/decoding
    functions for communication between hub and sensor.

    Args:
        max_packet_size: Maximum packet size in bytes, defaults to 16 for Pybricks compatibility.
    """

    def __init__(self, max_packet_size=MAX_PKT):
        self.commands = []
        self.modes = {}
        self.max_packet_size = max_packet_size

    def add_channel(self, mode_name: str, to_hub_fmt: str = ""):
        """Define a data channel to read on the hub.

        Use this function with identical parameters on both the sensor and the hub.
        You can call a channel like a command, but to update the data on the sensor
        side, you need to `update_channel(<name>, *args)`.

        Args:
            mode_name: The name of the mode you defined on the sensor side.
            to_hub_fmt: The format string of the data sent from the sensor to the hub.
                Use 'repr' to receive any python object. Or use a struct format string.
                See https://docs.python.org/3/library/struct.html
        """
        self.add_command(mode_name, to_hub_fmt=to_hub_fmt, command_type=CHANNEL)

    def add_command(
        self,
        mode_name: str,
        to_hub_fmt: str = "",
        from_hub_fmt: str = "",
        command_type=CALLBACK,
    ):
        """Define a remote call.

        Use this function with identical parameters on both the sensor and the hub.

        Args:
            mode_name: The name of the mode you defined on the sensor side.
            to_hub_fmt: The format string of the data sent from the sensor to the hub.
                Use 'repr' to receive any python object. Or use a struct format string.
                See https://docs.python.org/3/library/struct.html
            from_hub_fmt: The format string of the data sent from the hub.
            command_type: CALLBACK or CHANNEL (internal).
        """
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

        # Build a dictionary of mode names and their index
        self.modes[mode_name] = len(self.commands) - 1

    def decode(self, fmt: str, data: bytes):
        if fmt == "repr":
            clean = data.rstrip(b"\x00")
            return (eval(clean),) if clean else ("",)
        else:
            size = struct.calcsize(fmt)
            data = struct.unpack(fmt, data[:size])
        return data

    def encode(self, size, format, *argv):
        if format == "repr":
            s = bytes(repr(*argv), "UTF-8")
        else:
            s = struct.pack(format, *argv)
        assert len(s) <= size, "Payload exceeds maximum packet size"
        return s


class PUPRemoteHub(PUPRemote):
    """Communicate with a PUPRemoteSensor from a Pybricks hub.

    Use on the hub side running Pybricks. Copy the commands you defined on the sensor
    side to the hub side using add_command() and add_channel().

    Args:
        port: The port to which the PUPRemoteSensor is connected (e.g., Port.A).
        max_packet_size: Set to 16 for Pybricks compatibility, defaults to 32.
    """

    def _int8_to_uint8(self, arr):
        return [((i + 128) & 0xFF) - 128 for i in arr]

    def __init__(self, port, max_packet_size=MAX_PKT):
        super().__init__(max_packet_size)
        self.port = port
        try:
            self.pup_device = PUPDevice(port)
        except OSError:
            self.pup_device = None
            print("Check wiring and remote script. Unable to connect on ", self.port)
            raise
        # Multitask stuff
        self._queue = []
        self._multitask_loop_running = False

    def add_command(
        self, mode_name, to_hub_fmt="", from_hub_fmt="", command_type=CALLBACK
    ):
        super().add_command(mode_name, to_hub_fmt, from_hub_fmt, command_type)
        # Check the newly added commands against the advertised modes.
        modes = self.pup_device.info()["modes"]
        n = len(self.commands) - 1  # Zero indexed mode number
        assert len(self.commands) <= len(modes), "More commands than on remote side"
        assert (
            mode_name == modes[n][0].rstrip()
        ), "Expected '{}' as mode {}, but got '{}'".format(
            modes[n][0].rstrip(), n, mode_name
        )
        assert (
            self.commands[-1][SIZE] == modes[n][1]
        ), "Different parameter size than on remote side. Check formats."

    def call(self, mode_name: str, *argv, wait_ms=0) -> Any:
        """Call a remote function on the sensor side.

        Args:
            mode_name: The name of the mode you defined on both sides.
            *argv: Arguments to pass to the remote function.
            wait_ms: Time to wait before reading after sending (optional).
                Defaults to 0ms. A good value is `struct.calcsize(from_hub_fmt) * 1.5` (ms)

        Returns:
            The return value from the remote function, or a tuple of values.

        Raises:
            AssertionError: If called during a multitask operation.
        """
        assert (
            not run_task()
        ), "Use 'call_multitask' instead of 'call', with multiple start blocks or multitask blocks"

        mode = self.modes[mode_name]
        size = self.commands[mode][SIZE]

        if FROM_HUB_FORMAT in self.commands[mode]:
            num_args = self.commands[mode][ARGS_FROM_HUB]
            if num_args >= 0:
                assert (
                    len(argv) == num_args
                ), "Expected {} argument(s) in call '{}'".format(num_args, mode_name)
            payl = self.encode(size, self.commands[mode][FROM_HUB_FORMAT], *argv)
            self.pup_device.write(
                mode,
                [
                    ((i + 128) & 0xFF) - 128
                    for i in tuple(payl + b"\x00" * (size - len(payl)))
                ],
            )
            wait(wait_ms)

        data = self.pup_device.read(mode)
        raw_data = bytes([b if b>=0 else b+256 for b in data])
        result = self.decode(self.commands[mode][TO_HUB_FORMAT], raw_data)
        # Convert tuple size 1 to single value
        return result[0] if len(result) == 1 else result

    async def call_multitask(self, command_name: str, *argv, wait_ms=0):
        """Call a remote function asynchronously for use with Pybricks multitask.

        Make sure to run process_async() as a separate task before using this.

        Args:
            command_name: The name of the command.
            *argv: Arguments to pass to the remote function.
            wait_ms: Time to wait before reading after sending. Defaults to 0ms.

        Returns:
            The return value from the remote function, or a tuple of values.
        """
        if not self._multitask_loop_running:
            raise AssertionError(
                "Start 'process_async' as a seperate task (coroutine) before using 'call_multitask()'"
            )

        result_holder = [False, None, None]  # [done, result, error]
        self._queue.append((command_name, argv, wait_ms, result_holder))

        while not result_holder[DONE]:
            await wait(1)  # cooperative multitasking

        if result_holder[ERROR]:
            raise result_holder[ERROR]
        return result_holder[RESULT]

    async def _execute_call(self, mode_name: str, *argv, wait_ms=0):
        mode = self.modes[mode_name]
        size = self.commands[mode][SIZE]

        if FROM_HUB_FORMAT in self.commands[mode]:
            num_args = self.commands[mode][ARGS_FROM_HUB]
            if num_args >= 0:
                assert len(argv) == num_args, "Args mismatch in {}".format(mode_name)
            payl = self.encode(size, self.commands[mode][FROM_HUB_FORMAT], *argv)
            await self.pup_device.write(
                mode,
                [
                    ((i + 128) & 0xFF) - 128
                    for i in tuple(payl + b"\x00" * (size - len(payl)))
                ],
            )
            await wait(wait_ms)

        data = await self.pup_device.read(mode)
        raw_data = bytes([b if b>=0 else b+256 for b in data])
        result = self.decode(self.commands[mode][TO_HUB_FORMAT], raw_data)
        # Convert tuple size 1 to single value
        return result[0] if len(result) == 1 else result

    async def process_async(self):
        """
        Process multitask MicroPUP calls in a queue to avoid EAGAIN or IOERR.
        """
        self._multitask_loop_running = True
        running = False
        while True:
            if self._queue and not running:
                running = True
                command_name, argv, wait_ms, result_holder = self._queue.pop(0)

                try:
                    result = await self._execute_call(
                        command_name, *argv, wait_ms=wait_ms
                    )
                    result_holder[RESULT] = result
                except Exception as e:
                    result_holder[ERROR] = e
                    print(e)
                    raise
                finally:
                    result_holder[DONE] = True
                    running = False
            await wait(1)

# ============================================================
# PART 2 - ASTROPUP HUB GENERIC EXTENSIONS
# ============================================================
#
# This section contains the Astrogenius additions created and
# maintained by Luan Veras (@luanveras3), Astrogenius - Brazil.
#
# It wraps the vendored PUPRemoteHub foundation above and adds
# safer calls, diagnostics, LMS presets, and competition/debug
# profiles without changing the low-level PUPRemote behavior.
#
# ============================================================

ASTRO_OK = 0
ASTRO_ERR_NOT_REGISTERED = 1
ASTRO_ERR_OS = 2
ASTRO_ERR_UNKNOWN = 3
ASTRO_ERR_STALE_DATA = 4
ASTRO_ERR_BAD_RESPONSE = 5
ASTRO_ERR_MODE_ORDER = 6
ASTRO_ERR_NOT_RUNNING_ASYNC = 7
ASTRO_ERR_FORMAT = 8
ASTRO_ERR_MODE_VALIDATION = 9

ASTRO_ERROR_TEXT = {
    ASTRO_OK: "ASTRO_OK",
    ASTRO_ERR_NOT_REGISTERED: "ASTRO_ERR_NOT_REGISTERED",
    ASTRO_ERR_OS: "ASTRO_ERR_OS",
    ASTRO_ERR_UNKNOWN: "ASTRO_ERR_UNKNOWN",
    ASTRO_ERR_STALE_DATA: "ASTRO_ERR_STALE_DATA",
    ASTRO_ERR_BAD_RESPONSE: "ASTRO_ERR_BAD_RESPONSE",
    ASTRO_ERR_MODE_ORDER: "ASTRO_ERR_MODE_ORDER",
    ASTRO_ERR_NOT_RUNNING_ASYNC: "ASTRO_ERR_NOT_RUNNING_ASYNC",
    ASTRO_ERR_FORMAT: "ASTRO_ERR_FORMAT",
    ASTRO_ERR_MODE_VALIDATION: "ASTRO_ERR_MODE_VALIDATION",
}


class AstroPUPHub:
    """AstroPUP hub-side wrapper for LEGO Pybricks + PUPRemote.

    Maintained by Luan Veras, Astrogenius - Brazil (@astrogenius.team).

    Use this class instead of raw PUPRemoteHub when you want:
    - safer synchronous and multitask calls;
    - standardized AstroPUP error codes;
    - remote mode diagnostics;
    - generic command registration helpers;
    - competition/debug profiles;
    - a single global AstroPUP file for the hub side.

    This generic core does not know your robot, camera, sensor,
    mission, color table, or state packet. You define those in
    your own project files.

    This class does not change the PUPRemote/LPF2 protocol. It only
    wraps PUPRemoteHub and handles errors in a more predictable way.
    """

    def __init__(self, port, profile="competition", debug=False, max_packet_size=16):
        self.port = port
        self.profile = profile
        self.debug = debug
        self.max_packet_size = max_packet_size

        self._pup = PUPRemoteHub(port, max_packet_size=max_packet_size)

        self._commands = {}
        self._command_order = []
        self._last_error = ASTRO_OK
        self._last_exception = None
        self._last_response = None
        self._last_good_response = None
        self._fail_count = 0
        self._success_count = 0
        self._call_count = 0
        self._last_heartbeat = None

        # Optional frame/heartbeat tracker.
        # AstroPUP Core does not assume where the frame_id is inside your packet.
        # Your project code calls track_frame(frame_id) when it wants stale-data tracking.
        self._last_frame_id = None
        self._current_frame_id = None
        self._frame_is_stale = False
        self._stale_count = 0
        self._fresh_count = 0
        self._same_frame_limit = 1
        self._same_frame_repeats = 0

    # --------------------------------------------------------
    # Command registration
    # --------------------------------------------------------
    def add_command(self, name, to_hub_fmt="", from_hub_fmt=""):
        """Register a command in the same order used by the remote sensor."""
        try:
            self._pup.add_command(name, to_hub_fmt=to_hub_fmt, from_hub_fmt=from_hub_fmt)
            self._commands[name] = (to_hub_fmt, from_hub_fmt)
            if name not in self._command_order:
                self._command_order.append(name)
            self._last_error = ASTRO_OK
            self._last_exception = None
            return True

        except AssertionError as e:
            # Most common causes:
            # - command name is not the same as the remote side;
            # - command order is different;
            # - format size does not match the advertised mode size.
            self._last_error = ASTRO_ERR_MODE_ORDER
            self._last_exception = e
            self._fail_count += 1
            if self.debug:
                print("ASTROPUP: command registration failed")
                print("command:", name)
                print("error:", e)
                print("remote modes:", self.remote_modes())
            raise

        except Exception as e:
            self._last_error = ASTRO_ERR_UNKNOWN
            self._last_exception = e
            self._fail_count += 1
            if self.debug:
                print("ASTROPUP: unknown error in add_command")
                print(e)
            raise

    def add_channel(self, name, to_hub_fmt=""):
        """Register a read-only data channel.

        This mirrors PUPRemoteHub.add_channel while keeping AstroPUP's
        command registry and diagnostics.
        """
        try:
            self._pup.add_channel(name, to_hub_fmt)
            self._commands[name] = (to_hub_fmt, "")
            if name not in self._command_order:
                self._command_order.append(name)
            self._last_error = ASTRO_OK
            self._last_exception = None
            return True

        except AssertionError as e:
            self._last_error = ASTRO_ERR_MODE_ORDER
            self._last_exception = e
            self._fail_count += 1
            if self.debug:
                print("ASTROPUP: channel registration failed")
                print("channel:", name)
                print("error:", e)
                print("remote modes:", self.remote_modes())
            raise

        except Exception as e:
            self._last_error = ASTRO_ERR_UNKNOWN
            self._last_exception = e
            self._fail_count += 1
            if self.debug:
                print("ASTROPUP: unknown error in add_channel")
                print(e)
            raise

    def register_commands(self, command_specs):
        """Register several commands from a generic command specification.

        command_specs must be an iterable of tuples. Supported forms:

            ("name", "to_hub_fmt")
            ("name", "to_hub_fmt", "from_hub_fmt")

        The order must be exactly the same as the sensor-side order.

        Example:
            link.register_commands([
                ("reset", "B"),
                ("state", "hh"),
            ])
        """
        for spec in command_specs:
            if len(spec) == 2:
                name, to_hub_fmt = spec
                from_hub_fmt = ""
            elif len(spec) == 3:
                name, to_hub_fmt, from_hub_fmt = spec
            else:
                self._last_error = ASTRO_ERR_FORMAT
                self._fail_count += 1
                raise ValueError("Command spec must be (name, to_hub_fmt) or (name, to_hub_fmt, from_hub_fmt).")
            self.add_command(name, to_hub_fmt, from_hub_fmt)

    def identity(self):
        """Return the AstroPUP identity string."""
        return (
            __project__
            + " Hub Generic Core v"
            + __version__
            + " | "
            + __team__
            + " | "
            + __instagram__
            + " | Based on "
            + __pupremote_author__
        )

    # --------------------------------------------------------
    # Synchronous calls
    # --------------------------------------------------------
    def call(self, name, *args, wait_ms=0):
        """Raw PUPRemoteHub call. It may raise errors."""
        return self._pup.call(name, *args, wait_ms=wait_ms)

    def safe_call(self, name, *args, default=None, wait_ms=0):
        """Safe synchronous call.

        If the call fails, this returns default and stores the error code.
        Use this outside Pybricks multitask routines.
        """
        self._call_count += 1

        if name not in self._commands:
            self._last_error = ASTRO_ERR_NOT_REGISTERED
            self._fail_count += 1
            return default

        try:
            response = self._pup.call(name, *args, wait_ms=wait_ms)
            self._last_error = ASTRO_OK
            self._last_exception = None
            self._last_response = response
            self._last_good_response = response
            self._success_count += 1
            return response

        except OSError as e:
            self._last_error = ASTRO_ERR_OS
            self._last_exception = e
            self._fail_count += 1
            return default

        except AssertionError as e:
            # Example: call() was used while a Pybricks multitask is running.
            self._last_error = ASTRO_ERR_NOT_RUNNING_ASYNC
            self._last_exception = e
            self._fail_count += 1
            return default

        except Exception as e:
            self._last_error = ASTRO_ERR_UNKNOWN
            self._last_exception = e
            self._fail_count += 1
            return default

    # --------------------------------------------------------
    # Async / multitask calls
    # --------------------------------------------------------
    async def process_async(self):
        """Process the internal PUPRemote async queue.

        Run this as a separate Pybricks multitask coroutine before using
        call_multitask() or safe_call_multitask().
        """
        await self._pup.process_async()

    async def call_multitask(self, name, *args, wait_ms=0):
        """Raw async call. It may raise errors."""
        return await self._pup.call_multitask(name, *args, wait_ms=wait_ms)

    async def safe_call_multitask(self, name, *args, default=None, wait_ms=0):
        """Safe Pybricks multitask call.

        If the call fails, this returns default and stores the error code.
        Use this when your robot is running process_async() in another task.
        """
        self._call_count += 1

        if name not in self._commands:
            self._last_error = ASTRO_ERR_NOT_REGISTERED
            self._fail_count += 1
            return default

        try:
            response = await self._pup.call_multitask(name, *args, wait_ms=wait_ms)
            self._last_error = ASTRO_OK
            self._last_exception = None
            self._last_response = response
            self._last_good_response = response
            self._success_count += 1
            return response

        except OSError as e:
            self._last_error = ASTRO_ERR_OS
            self._last_exception = e
            self._fail_count += 1
            return default

        except AssertionError as e:
            self._last_error = ASTRO_ERR_NOT_RUNNING_ASYNC
            self._last_exception = e
            self._fail_count += 1
            return default

        except Exception as e:
            self._last_error = ASTRO_ERR_UNKNOWN
            self._last_exception = e
            self._fail_count += 1
            return default

    # --------------------------------------------------------
    # Diagnostics
    # --------------------------------------------------------
    def remote_modes(self):
        """Return the modes advertised by the remote LPF2/PUP device."""
        try:
            return self._pup.pup_device.info()["modes"]
        except Exception as e:
            self._last_error = ASTRO_ERR_UNKNOWN
            self._last_exception = e
            return None

    def validate_remote_modes(self, strict=True):
        """Validate registered command names against remote modes.

        This checks names and order only. It intentionally does not
        enforce binary packet size because PUPRemote/Pybricks mode size
        reporting may include packing details that differ from the simple
        struct format string.

        Returns True when validation passes, False otherwise.
        """
        modes = self.remote_modes()

        if modes is None:
            self._last_error = ASTRO_ERR_MODE_VALIDATION
            if strict:
                raise AssertionError("AstroPUP could not read remote modes.")
            return False

        if len(self._command_order) > len(modes):
            self._last_error = ASTRO_ERR_MODE_VALIDATION
            msg = (
                "AstroPUP mode validation failed: hub registered "
                + str(len(self._command_order))
                + " commands but remote announced only "
                + str(len(modes))
                + " modes."
            )
            if strict:
                raise AssertionError(msg)
            return False

        for index, name in enumerate(self._command_order):
            remote_name = modes[index][0]

            if name != remote_name:
                self._last_error = ASTRO_ERR_MODE_VALIDATION
                msg = (
                    "AstroPUP mode validation failed at index "
                    + str(index)
                    + ": hub has '"
                    + str(name)
                    + "' but remote announced '"
                    + str(remote_name)
                    + "'."
                )
                if strict:
                    raise AssertionError(msg)
                return False

        self._last_error = ASTRO_OK
        return True

    def startup_report(self):
        """Return a readable startup report for debugging and pit checks."""
        modes = self.remote_modes()
        validation = self.validate_remote_modes(strict=False)

        text = "AstroPUP Startup Report\n"
        text += "Project: " + __project__ + "\n"
        text += "Version: " + __version__ + "\n"
        text += "Team: " + __team__ + "\n"
        text += "Instagram: " + __instagram__ + "\n"
        text += "Port: " + str(self.port) + "\n"
        text += "Profile: " + str(self.profile) + "\n"
        text += "Registered commands:\n"

        for i, name in enumerate(self._command_order):
            text += "  " + str(i) + " " + str(name) + "\n"

        text += "Remote modes:\n"

        if modes is None:
            text += "  <unavailable>\n"
        else:
            for i, mode in enumerate(modes):
                text += "  " + str(i) + " " + str(mode) + "\n"

        text += "Mode validation: " + ("OK" if validation else "FAILED") + "\n"
        text += "Frame tracker: optional\n"
        text += "Last error: " + self.last_error_text()
        return text

    def command_order(self):
        """Return registered commands in registration order."""
        return tuple(self._command_order)

    def call_count(self):
        return self._call_count

    def success_count(self):
        return self._success_count

    def fail_count(self):
        return self._fail_count

    def last_good_response(self):
        """Return the last successful response from safe_call or safe_call_multitask."""
        return self._last_good_response

    def print_remote_modes(self):
        """Print the remote mode list in a readable format."""
        modes = self.remote_modes()
        if modes is None:
            print("ASTROPUP: could not read remote modes")
            return
        print("ASTROPUP REMOTE MODES:")
        for i, mode in enumerate(modes):
            print(i, mode)

    def last_error(self):
        return self._last_error

    def last_error_text(self):
        return ASTRO_ERROR_TEXT.get(self._last_error, "ASTRO_ERR_UNDEFINED")

    def last_exception(self):
        return self._last_exception

    def last_response(self):
        return self._last_response

    def fail_count(self):
        return self._fail_count

    def commands(self):
        """Return registered commands in registration order."""
        return tuple(self._command_order)

    def is_alive(self):
        """Return True if the last AstroPUP operation completed successfully."""
        return self._last_error == ASTRO_OK

    def heartbeat_changed(self, heartbeat):
        """Check if a heartbeat/frame counter changed since the last check."""
        changed = heartbeat != self._last_heartbeat
        self._last_heartbeat = heartbeat
        if not changed:
            self._last_error = ASTRO_ERR_STALE_DATA
        return changed

    # --------------------------------------------------------
    # Optional frame / heartbeat tracking
    # --------------------------------------------------------
    def track_frame(self, frame_id, stale_after=1):
        """Track a project-defined frame_id/heartbeat value.

        This method is generic: AstroPUP does not know your packet layout.
        Your own robot code decides which value is the frame_id and passes it
        here after each successful read.

        Args:
            frame_id: Any comparable frame/heartbeat value.
            stale_after: Number of repeated identical frames allowed before
                is_stale() becomes True. Default is 1.

        Returns:
            True if the frame is fresh, False if it is stale/repeated.
        """
        self._current_frame_id = frame_id
        self._same_frame_limit = stale_after

        if self._last_frame_id is None:
            self._last_frame_id = frame_id
            self._frame_is_stale = False
            self._fresh_count += 1
            self._same_frame_repeats = 0
            return True

        if frame_id == self._last_frame_id:
            self._same_frame_repeats += 1

            if self._same_frame_repeats >= stale_after:
                self._frame_is_stale = True
                self._stale_count += 1
                self._last_error = ASTRO_ERR_STALE_DATA
                return False

            self._frame_is_stale = False
            return True

        self._last_frame_id = frame_id
        self._frame_is_stale = False
        self._same_frame_repeats = 0
        self._fresh_count += 1

        if self._last_error == ASTRO_ERR_STALE_DATA:
            self._last_error = ASTRO_OK

        return True

    def is_stale(self):
        """Return True if the last tracked frame_id was repeated/stale."""
        return self._frame_is_stale

    def stale_count(self):
        """Return how many stale/repeated frames were detected."""
        return self._stale_count

    def fresh_count(self):
        """Return how many fresh frame changes were detected."""
        return self._fresh_count

    def last_frame_id(self):
        """Return the last accepted fresh frame_id."""
        return self._last_frame_id

    def current_frame_id(self):
        """Return the most recently tracked frame_id, fresh or stale."""
        return self._current_frame_id

    def reset_frame_tracker(self):
        """Reset optional frame/heartbeat tracking state."""
        self._last_frame_id = None
        self._current_frame_id = None
        self._frame_is_stale = False
        self._stale_count = 0
        self._fresh_count = 0
        self._same_frame_repeats = 0

    def reset_errors(self):
        """Clear diagnostic error state without reconnecting the device."""
        self._last_error = ASTRO_OK
        self._last_exception = None
        self._fail_count = 0
        self._success_count = 0
        self._call_count = 0

    def report(self):
        """Return a compact diagnostic report."""
        return (
            "AstroPUPHub("
            + "project=" + __project__
            + ", version=" + __version__
            + ", team=" + __team__
            + ", maintainer=" + __maintainer__
            + ", port=" + str(self.port)
            + ", profile=" + str(self.profile)
            + ", last_error=" + self.last_error_text()
            + ", calls=" + str(self._call_count)
            + ", success=" + str(self._success_count)
            + ", fail_count=" + str(self._fail_count)
            + ", stale=" + str(self._frame_is_stale)
            + ", stale_count=" + str(self._stale_count)
            + ", last_frame_id=" + str(self._last_frame_id)
            + ", commands_order=" + str(self._command_order)
            + ")"
        )
