import asyncio
from typing import Callable,List, Optional

class Worker:
    def __init__(self, frequency = 60) -> None:
        self._frequency = frequency
        self._task : Optional[asyncio.Task] = None

    def start_acquisition(self, callback: Callable[[str], None]):
        if self._task is None:
            self._task = asyncio.create_task(self._acquisition_task(callback))
        else:
            print("Task already running")
    def stop_acquisition(self):
        if self._task is not None:
            self._task.cancel()
            self._task = None
        else:
            print("No acquisition task is running.")

    async def _acquisition_task(self, callback: Callable[[str], None]):
        counter = 0
        try:
            while True:
                counter += 1
                value = f"Counter: {counter}"
                callback(value)
                await asyncio.sleep(1/self._frequency)
        except asyncio.CancelledError:
            print("Acquisition task canceled.")