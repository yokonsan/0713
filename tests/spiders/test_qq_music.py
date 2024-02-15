import pytest

from spiders.qq_music import QQMusic


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "actor", [
        "002PZBgg1S9xPX"
    ]
)
async def test_run_once(actor):
    spider = QQMusic()
    res = await spider.run_once(actor)
    assert int(res) > 1000
