# Hub-side snippet for a Pybricks multitask project.

Robot.sensor.add_command("state", "hhhBhhhh")

res = await Robot.sensor.safe_call_multitask("state", default=None)

if res is not None and len(res) == 8:
    frame_id, Robot.erro, Robot.junction, Robot.button, Robot.c1, Robot.c2, Robot.c3, Robot.c4 = res

    Robot.sensor.track_frame(frame_id, stale_after=3)

    if Robot.sensor.is_stale():
        # Your project decides what to do:
        # slow down, stop, ignore, retry, etc.
        pass
