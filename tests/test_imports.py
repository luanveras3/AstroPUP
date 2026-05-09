def test_astropup_modules_import():
    import astropup_hub
    import astropup_sensor

    assert astropup_hub.__project__ == "AstroPUP"
    assert astropup_sensor.__project__ == "AstroPUP"
