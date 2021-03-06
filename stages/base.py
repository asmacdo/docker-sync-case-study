from gettext import gettext as _
import asyncio


class Stage:
    """
    The base class for all Stages API stages.

    To make a stage, inherit from this class and implement :meth:`__call__` on the subclass.
    """

    async def __call__(self, in_q, out_q):
        """
        The coroutine that is run as part of this stage.

        Args:
            in_q (:class:`asyncio.Queue`): The queue to receive items from the previous stage.
            out_q (:class:`asyncio.Queue`): The queue to put handled items into for the next stage.

        Returns:
            The coroutine that runs this stage.

        """
        raise NotImplementedError(_('A plugin writer must implement this method'))

    @staticmethod
    async def batches(in_q, minsize=1):
        """
        Asynchronous iterator yielding batches of :class:`DeclarativeContent` from `in_q`.

        The iterator will try to get as many instances of
        :class:`DeclarativeContent` as possible without blocking, but
        at least `minsize` instances.

        Args:
            in_q (:class:`asyncio.Queue`): The queue to receive
                :class:`~pulpcore.plugin.stages.DeclarativeContent` objects from.
            minsize (int): The minimum batch size to yield (unless it is the final batch)

        Yields:
            A list of :class:`DeclarativeContent` instances

        Examples:
            Used in stages to get large chunks of declarative_content instances from
            `in_q`::

                class MyStage(Stage):
                    async def __call__(self, in_q, out_q):
                        async for batch in self.batches(in_q):
                            for declarative_content in batch:
                                # process declarative content
                                await out_q.put(declarative_content)
                        await out_q.put(None)

        """
        batch = []
        shutdown = False

        def add_to_batch(batch, content):
            if content is None:
                return True
            batch.append(content)
            return False

        while not shutdown:
            content = await in_q.get()
            shutdown = add_to_batch(batch, content)
            while not shutdown:
                try:
                    content = in_q.get_nowait()
                except asyncio.QueueEmpty:
                    break
                else:
                    shutdown = add_to_batch(batch, content)
            if batch and (len(batch) >= minsize or shutdown):
                yield batch
                batch = []


def run_pipeline(stages):
    """
    All we are going to do is n
    """
    pipeline = create_pipeline(stages)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pipeline)


async def create_pipeline(stages, maxsize=100):
    futures = []
    in_q = None
    for stage in stages:
        out_q = asyncio.Queue(maxsize=maxsize)
        try:
            futures.append(asyncio.ensure_future(stage(in_q, out_q)))
        except Exception as e:
            print("Failed Stage:")
            print(stage)
        in_q = out_q

    try:
        await asyncio.gather(*futures)
    except Exception:
        # One of the stages raised an exception, cancel all stages...
        pending = []
        for task in futures:
            if not task.done():
                task.cancel()
                pending.append(task)
        # ...and run until all Exceptions show up
        if pending:
            await asyncio.wait(pending, timeout=60)
        raise
