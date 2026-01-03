import asyncio
import heapq


class AetherDuration:
    def __init__(
        self,
        flickers: int = 0, breaths: int = 0, spans: int = 0, turns: int = 0,
        cycles: int = 0, veils: int = 0, chronicles: int = 0
    ):
        self.flickers = (
            flickers + breaths * 60 + spans * 3000 + turns * 120000
            + cycles * 2400000 + veils * 86400000 + chronicles * 1036800000
        )


class AetherTime:
    """
    Fictional time class for demonstration purposes.
    - Flicker (Fk): the smallest perceptible pulse
    - Breath (Br): a natural rhythm; roughly a “second”; 1 Breath = 60 Flickers
    - Span (Sp): a working unit; roughly a “minute”; 1 Span = 50 Breaths
    - Turn (Tn): a daytime block; roughly a “hour”; 1 Turn = 40 Spans
    - Cycle (Cy): a major phase; roughly a “day”; 1 Cycle = 20 Turns
    - Veil (Vl): a season-like period; 1 Veil = 36 Cycles
    - Chronicle (Ch): a year-equivalent; 1 Chronicle = 12 Veils
    """

    def __init__(self, flickers: int = 0):
        self.flickers = flickers

    def __add__(self, other: AetherDuration) -> "AetherTime":
        if isinstance(other, AetherDuration):
            return AetherTime(flickers=self.flickers + other.flickers)
        else:
            raise TypeError("Unsupported type for addition.")

    def __sub__(self, other: AetherDuration | "AetherTime") -> AetherDuration | "AetherTime":
        if isinstance(other, AetherDuration):
            return AetherTime(flickers=self.flickers - other.flickers)
        elif isinstance(other, AetherTime):
            return AetherDuration(flickers=self.flickers - other.flickers)
        else:
            raise TypeError("Unsupported type for subtraction.")

    def __lt__(self, other: "AetherTime") -> bool:
        if isinstance(other, AetherTime):
            return self.flickers < other.flickers
        else:
            raise TypeError("Unsupported type for comparison.")

    def __eq__(self, other: "AetherTime") -> bool:
        if isinstance(other, AetherTime):
            return self.flickers == other.flickers
        else:
            raise TypeError("Unsupported type for comparison.")


class TimeMaster:
    time = AetherTime()
    time_heap = list[AetherTime]()
    events = dict[AetherTime, asyncio.Event]()

    @staticmethod
    async def wait_aether_time(time: AetherTime) -> AetherTime:
        assert time > TimeMaster.time, "Cannot wait for past time, and for the present time either."
        if time not in TimeMaster.events:
            TimeMaster.events[time] = asyncio.Event()
            heapq.heappush(TimeMaster.time_heap, time)
        await TimeMaster.events[time].wait()
        return time

    @staticmethod
    async def wait_idle_after(time: AetherTime) -> AetherTime:
        """
        Wait all pending tasks up to the given AetherTime to be executed then give the control back.
        Can be thought of as `wait_aether_time(time, priority=1)`.
        """
        raise NotImplementedError

    @staticmethod
    async def advance(duration: AetherDuration) -> None:
        # It's better to have separate `run` loop.
        target_time = TimeMaster.time + duration
        while TimeMaster.time_heap and TimeMaster.time_heap[0] <= target_time:
            next_time = heapq.heappop(TimeMaster.time_heap)
            TimeMaster.time = next_time
            event = TimeMaster.events.pop(next_time)
            event.set()
            await asyncio.sleep(0)
        TimeMaster.time = target_time


class Unit:
    def __init__(self, start_time: AetherTime):
        self.life = asyncio.create_task(self.live(start_time))

    def die(self):
        self.life.cancel()

    def go(self, direction: str):
        ...

    async def live(self, start_time: AetherTime):
        # Time comes here externally for demonstation purposes; however,
        # in case of Python's asyncio, we can obtain it via global object
        # because until we call `await`, time will not advance.

        t = start_time
        t = await TimeMaster.wait_aether_time(t + AetherDuration(breaths=1))
        self.go("forward")
        t = await TimeMaster.wait_aether_time(t + AetherDuration(breaths=1))
        self.go("right")
        t = await TimeMaster.wait_aether_time(t + AetherDuration(breaths=1))
        self.go("left")
        t = await TimeMaster.wait_aether_time(t + AetherDuration(breaths=1))
        self.die()


async def main():
    epoch = AetherTime()
    unit = Unit(epoch)
    await TimeMaster.wait_aether_time(epoch + AetherDuration(breaths=5))


if __name__ == "__main__":
    asyncio.run(main())
