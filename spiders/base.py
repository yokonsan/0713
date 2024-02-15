import asyncio
from typing import Dict, Union

import aiohttp
from aiohttp import ClientSession
from loguru import logger

from store import store
from util.fake import user_agents


class SpiderBase:
    NAME = ""
    ENABLE = True
    ACTORS = {}

    async def run_once(self, actor: Union[str, int]):
        logger.debug(f"crawler {self.NAME}[{self.ACTORS[actor]}] start at once")

        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers=self.get_headers()
        ) as session:
            fans = await self.get_fans_num(session, actor)

            logger.debug(f"crawler {self.NAME}[{self.ACTORS[actor]}] end, fans: {fans}")
            return {self.ACTORS[actor]: fans}

    async def __call__(self, *args, **kwargs):
        while True:
            logger.debug(f"crawler {self.NAME} loop start...")
            actor_fans = {}
            for actor in self.get_actors():
                data = await self.run_once(actor)
                actor_fans.update(data)

            await store.save(self.NAME, actor_fans)
            await asyncio.sleep(60 * 5)

    async def get_fans_num(self, session: ClientSession, actor: Union[str, int]):
        raise NotImplementedError

    def get_actors(self):
        raise NotImplementedError

    def get_headers(self) -> Dict:
        """请求头"""
        return {
            "User-Agent": user_agents[0],
        }
