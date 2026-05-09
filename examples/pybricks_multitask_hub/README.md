# 02 Pybricks Multitask Reader

Use this when your robot already uses Pybricks `async`, `await`, `multitask`, and `run_task`.

Important pattern:

```python
async def pup_loop():
    while True:
        await link.process_async()
        await wait(0)
```

Then other tasks can use:

```python
await link.safe_call_multitask("state", default=None)
```
