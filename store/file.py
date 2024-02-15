import json
from typing import Union, Dict

import aiofiles

from store.base import Store


def file_prepare(method):
    async def wrapper(*args, **kwargs):
        try:
            return await method(*args, **kwargs)
        except FileNotFoundError:
            _, platform, *_ = args
            async with aiofiles.open(File().filename.format(platform), "w") as f:
                await f.write("{}")

            return await method(*args, **kwargs)
    return wrapper


class File(Store):
    filename = "data/{}-fans.json"

    @file_prepare
    async def save(self, platform: str, actor_fans: Dict[str, str]):
        body = await self.get_all(platform)
        body.update(actor_fans)

        async with aiofiles.open(self.filename.format(platform), "w") as f:
            await f.write(json.dumps(body, ensure_ascii=False))

    @file_prepare
    async def get(self, platform: str, actor: Union[str, int]) -> str:
        async with aiofiles.open(self.filename.format(platform), "r") as f:
            body = json.loads(await f.read())
            return body.get(actor)

    @file_prepare
    async def get_all(self, platform: str) -> Dict[str, str]:
        async with aiofiles.open(self.filename.format(platform), "r") as f:
            body = json.loads(await f.read() or "{}")
            return body
