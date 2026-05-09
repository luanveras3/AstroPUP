from astropup_sensor import AstroPUPSensor


def make_sensor_without_hardware():
    sensor = AstroPUPSensor.__new__(AstroPUPSensor)
    sensor._frame_id = 0
    return sensor


def test_next_frame_id_increments():
    sensor = make_sensor_without_hardware()

    assert sensor.current_frame_id() == 0
    assert sensor.next_frame_id() == 1
    assert sensor.next_frame_id() == 2
    assert sensor.current_frame_id() == 2


def test_next_frame_id_wraps_to_zero():
    sensor = make_sensor_without_hardware()
    sensor.reset_frame_id(2)

    assert sensor.next_frame_id(max_value=3) == 3
    assert sensor.next_frame_id(max_value=3) == 0


def test_reset_frame_id_sets_custom_value():
    sensor = make_sensor_without_hardware()

    sensor.reset_frame_id(100)
    assert sensor.current_frame_id() == 100
