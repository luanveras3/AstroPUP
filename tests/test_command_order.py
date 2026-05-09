from astropup_hub import AstroPUPHub, ASTRO_OK


def make_hub_without_hardware():
    hub = AstroPUPHub.__new__(AstroPUPHub)
    hub._command_order = []
    hub._commands = {}
    hub._last_error = ASTRO_OK
    return hub


def test_command_order_returns_registered_order():
    hub = make_hub_without_hardware()

    hub._command_order.extend(["reset", "state", "debug"])

    assert hub.command_order() == ("reset", "state", "debug")
    assert hub.commands() == ("reset", "state", "debug")
