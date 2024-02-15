import json
from typing import Dict, Union

from aiohttp import ClientSession

from spiders import SpiderBase
from util import fetch


class QQMusic(SpiderBase):
    NAME = "qq-music"
    ACTORS = {
        "002PZBgg1S9xPX": "陈楚生",
        "000b7B7h1fXzaM": "苏醒",
        "004PjYVG2cjyBK": "张远",
        "001iaSfi07zuSE": "王铮亮",
        "004gbMvP356XaI": "陆虎",
        "000TprbQ0R4aGb": "王栎鑫"
    }

    async def get_fans_num(self, session: ClientSession, actor: Union[str, int]):
        url = "https://c.y.qq.com/rsc/fcgi-bin/fcg_order_singer_getnum.fcg"
        params = {
            "format": "json",
            "outCharset": "utf-8",
            "singermid": actor,
            "utf8": "1"
        }
        res = await fetch.fetch_text(session, url, method=fetch.FetchMethod.get, params=params)
        res = json.loads(res)
        return str(res["num"])

    def get_actors(self):
        return self.ACTORS

    def get_headers(self) -> Dict:
        headers = super().get_headers()
        headers.update({
            "Referer": "https://y.qq.com/",
            "Accept": "application/json"
        })
        return headers
