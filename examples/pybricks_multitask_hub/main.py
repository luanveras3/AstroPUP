from pybricks.parameters import Port
from pybricks.tools import wait, multitask, run_task
from astropup_hub import AstroPUPHub

link = AstroPUPHub(Port.C, profile="competition", debug=False)

link.add_command("reset", "B")
link.add_command("state", "hh")

async def pup_loop():
    while True:
        await link.process_async()
        await wait(0)

async def read_loop():
    while True:
        data = await link.safe_call_multitask("state", default=None)

        if data is not None:
            value_1, value_2 = data
            # Use your values here.

        await wait(0)

async def main():
    await multitask(
        pup_loop(),
        read_loop(),
    )

run_task(main())
