import asyncio
from typing import Callable, Coroutine, Any, TypeVar, Dict

from aiohttp import ClientError, ClientSession, hdrs
from loguru import logger

from exception import MaxRetryError

T = TypeVar("T")


class MaxRetry:
    def __init__(self, max_retry: int = 0):
        self.max_retry = max_retry

    def __call__(
            self, connect_once: Callable[..., Coroutine[Any, Any, T]]
    ) -> Callable[..., Coroutine[Any, Any, T]]:
        async def connect_n_times(*args: Any, **kwargs: Any) -> T:
            retry = self.max_retry + 1
            while retry:
                try:
                    return await connect_once(*args, **kwargs)
                except ClientError as e:
                    await asyncio.sleep(1)
                    logger.warning(f"请求失败（{e.__class__.__name__}），正在重试，剩余 {retry - 1} 次")
                except asyncio.TimeoutError:
                    logger.warning(f"请求超时，正在重试，剩余 {retry - 1} 次")
                finally:
                    retry -= 1
            raise MaxRetryError("超出最大重试次数")

        return connect_n_times


class FetchMethod:
    get = hdrs.METH_GET
    post = hdrs.METH_POST
    put = hdrs.METH_PUT


@MaxRetry(2)
async def fetch_text(
        session: ClientSession,
        url: str,
        method: str = FetchMethod.post, **kwargs
) -> Dict:
    logger.debug(f"Fetch text: {url}")
    async with session.request(method, url, **kwargs) as resp:
        if not resp.ok:
            raise ClientError("fetch error")
        return await resp.text()


@MaxRetry(2)
async def fetch_json(
        session: ClientSession,
        url: str,
        method: str = FetchMethod.post, **kwargs
) -> Dict:
    logger.debug(f"Fetch json: {url}")
    async with session.request(method, url, **kwargs) as resp:
        if not resp.ok:
            raise ClientError("fetch error")
        return await resp.json()