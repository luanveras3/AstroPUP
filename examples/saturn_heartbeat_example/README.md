# Saturn-style heartbeat example

This example shows how a project can add its own packet layout outside AstroPUP Core.

Old packet:

```python
(error, junction, button, c1, c2, c3, c4)
"hhBhhhh"
```

New packet with heartbeat:

```python
(frame_id, error, junction, button, c1, c2, c3, c4)
"hhhBhhhh"
```

The `frame_id` is project-specific. AstroPUP only provides helpers to generate and track it.
