# 00 Basic Counter Pair

This is the smallest useful AstroPUP example.

It uses two commands:

```python
reset -> "B"
state -> "hB"
```

Sensor returns:

```python
(counter, status)
```

Hub reads:

```python
counter, status = link.safe_call("state")
```

Use this example first to confirm that AstroPUP is installed correctly on both sides.
