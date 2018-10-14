import asyncio
from stages import Stage

import logging
log = logging.getLogger("DummyStage")


class HelloStage(Stage):
    def __init__(self, sleep=False):
        self.sleep = sleep

    async def __call__(self, unused_in_q, out_q):
        await out_q.put("Hello")
        if self.sleep:
            await asyncio.sleep(1)
        await out_q.put("World")
        await out_q.put(None)  # Indicates this stage is finished


class PrintStage(Stage):
    async def __call__(self, in_q, out_q):
        while True:
            print_this = await in_q.get()
            if print_this is None:
                break
            else:
                print(print_this)
        await out_q.put(None)


class PrintAndPassStage(Stage):
    async def __call__(self, in_q, out_q):
        while True:
            print_this = await in_q.get()
            if print_this is None:
                break
            else:
                print(print_this)
                await out_q.put(print_this)
        await out_q.put(None)
