from typing import Union

from aiohttp import ClientSession

from spiders import SpiderBase
from util import fetch


class Bilibili(SpiderBase):
    NAME = "bilibili"
    ACTORS = {
        "1498266696": "陈楚生",
        "24659626": "苏醒",
        "1938665582": "张远",
        "1923632848": "王铮亮",
        "408384315": "陆虎",
        "701402278": "王栎鑫"
    }

    async def get_fans_num(self, session: ClientSession, actor: Union[str, int]):
        url = "https://api.bilibili.com/x/relation/stat"
        params = {
            "vmid": actor,
        }
        res = await fetch.fetch_json(session, url, method=fetch.FetchMethod.get, params=params)
        return str(res["data"]["follower"])

    def get_actors(self):
        return self.ACTORS
