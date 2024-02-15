import pytest

from store.file import File


@pytest.fixture
def file_obj():
    return File()


@pytest.fixture
async def test_save(file_obj):
    await file_obj.save("QQ 音乐", {"陈楚生": "988295"})


@pytest.mark.asyncio
@pytest.mark.parametrize("platform, actor, expect", [
    ("QQ 音乐", "陈楚生", "988295"),
    ("QQ 音乐", "陈楚生", "9882951")
])
async def test_get(file_obj, platform, actor, expect):
    res = await file_obj.get(platform, actor)
    assert res == expect


@pytest.mark.asyncio
async def test_get_all(file_obj):
    await file_obj.get_all("QQ 音乐")
