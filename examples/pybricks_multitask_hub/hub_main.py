# AstroPUP example: Pybricks multitask reader
#
# Runs on the LEGO Hub with Pybricks.
#
# Use this pattern when your robot uses Pybricks multitasking.
# One task must keep process_async() alive.
# Another task can read using safe_call_multitask().

from pybricks.parameters import Port
from pybricks.tools import wait, multitask, run_task
from astropup_hub import AstroPUPHub

link = AstroPUPHub(Port.C, profile="competition", debug=False)

link.add_command("reset", "B")
link.add_command("state", "hB")


async def pup_loop():
    while True:
        await link.process_async()
        await wait(0)


async def read_loop():
    while True:
        data = await link.safe_call_multitask("state", default=None)

        if data is not None:
            counter, status = data
            print("counter:", counter, "status:", status)
        else:
            print("read failed:", link.last_error_text())

        await wait(200)


async def main():
    print(link.startup_report())

    await multitask(
        pup_loop(),
        read_loop(),
    )


run_task(main())
