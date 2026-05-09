# 04 Saturn-Style Bridge

This is not AstroPUP Core.

This shows how a real robot project can define its own packet outside the generic library.

Packet:

```python
(frame_id, line_error, junction, button, c1, c2, c3, c4)
```

Format:

```python
"hhhBhhhh"
```

This is useful for robots that combine:

- line sensor data;
- button data;
- camera or external controller values;
- optional heartbeat tracking.
