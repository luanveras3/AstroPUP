# 03 Heartbeat / Stale-Data Demo

This example demonstrates:

```python
sensor.next_frame_id()
link.track_frame(frame_id)
link.is_stale()
link.stale_count()
```

To simulate stale data:

1. Open `sensor_main.py`.
2. Change:

```python
FREEZE_FRAME = False
```

to:

```python
FREEZE_FRAME = True
```

Expected Hub output:

```text
fresh: False
stale: True
stale_count: increasing
```
