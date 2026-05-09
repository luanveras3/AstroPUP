from astropup_hub import AstroPUPHub, ASTRO_ERR_STALE_DATA, ASTRO_OK


def make_hub_without_hardware():
    hub = AstroPUPHub.__new__(AstroPUPHub)
    hub._last_error = ASTRO_OK
    hub._last_exception = None
    hub._last_frame_id = None
    hub._current_frame_id = None
    hub._frame_is_stale = False
    hub._stale_count = 0
    hub._fresh_count = 0
    hub._same_frame_limit = 1
    hub._same_frame_repeats = 0
    return hub


def test_track_frame_detects_fresh_and_stale_frames():
    hub = make_hub_without_hardware()

    assert hub.track_frame(1) is True
    assert hub.is_stale() is False
    assert hub.fresh_count() == 1
    assert hub.stale_count() == 0

    assert hub.track_frame(2) is True
    assert hub.is_stale() is False
    assert hub.fresh_count() == 2
    assert hub.last_frame_id() == 2
    assert hub.current_frame_id() == 2

    assert hub.track_frame(2) is False
    assert hub.is_stale() is True
    assert hub.stale_count() == 1
    assert hub.last_error() == ASTRO_ERR_STALE_DATA


def test_reset_frame_tracker_clears_state():
    hub = make_hub_without_hardware()

    hub.track_frame(10)
    hub.track_frame(10)
    assert hub.is_stale() is True

    hub.reset_frame_tracker()

    assert hub.is_stale() is False
    assert hub.stale_count() == 0
    assert hub.fresh_count() == 0
    assert hub.last_frame_id() is None
    assert hub.current_frame_id() is None
