
import asyncio as aio
import concurrent.futures as cf
from functools import partial
from collections.abc import Awaitable
from typing import Union, TypeVar


T = TypeVar("T")


async def async_wait(future: Union[cf.Future[T], aio.Future[T], Awaitable[T]],
                     timeout: Union[int, float, None] = None) -> T:
    if aio.isfuture(future) or isinstance(future, Awaitable):
        # async await for the future object, with optional timeout
        if timeout is None:
            return await future
        else:
            async with aio.timeout(timeout):
                return await future

    #
    # an interruptable, asynchronous wait, using an asyncio
    # event activated via callback onto the concurrent future
    #
    complete_evt = aio.Event()

    def cb_evt(evt: aio.Event, loop: aio.AbstractEventLoop, _: cf.Future):
        loop.call_soon_threadsafe(evt.set)
        
    cb = partial(cb_evt, complete_evt, aio.get_running_loop())
    future.add_done_callback(cb)
    if timeout is None:
        await complete_evt.wait()
    else:
        async with aio.timeout(timeout):
            await complete_evt.wait()
    return future.result(0)
