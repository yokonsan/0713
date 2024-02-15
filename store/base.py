from typing import Union, Dict


class Store:

    async def save(self, platform: str, actor_fans: Dict[str, str]):
        raise NotImplementedError

    async def get(self, platform: str, actor: Union[str, int]):
        raise NotImplementedError

    async def get_all(self, platform: str):
        raise NotImplementedError
