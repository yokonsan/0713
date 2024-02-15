import os
from typing import Union, Dict

from aiohttp import ClientSession

from spiders import SpiderBase
from util import fetch


class Weibo(SpiderBase):
    NAME = "weibo"
    ACTORS = {
        "1296234914": "陈楚生",
        "1296241304": "苏醒",
        "1660399881": "张远",
        "1377828950": "王铮亮",
        "1240959311": "陆虎",
        "1292500037": "王栎鑫"
    }
    cookies = os.getenv("WEIBO_COOKIES")

    async def get_fans_num(self, session: ClientSession, actor: Union[str, int]):
        url = "https://weibo.com/ajax/profile/info"
        params = {
            "uid": actor,
        }
        res = await fetch.fetch_json(session, url, method=fetch.FetchMethod.get, params=params)
        return str(res["data"]["user"]["followers_count"])

    def get_actors(self):
        return self.ACTORS

    def get_headers(self) -> Dict:
        headers = super().get_headers()
        headers.update({
            "Cookie": self.cookies
        })
        return headers
