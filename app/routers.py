from typing import Union, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

from exception import ReturnCode, SuccessCode
from store import store

router = APIRouter()


class ResponseBase(BaseModel):
    code: ReturnCode = SuccessCode.SUCCESS
    message: str = ""
    data: Union[Dict, List] = {}


@router.get("/{platform}")
async def fans(platform: str):
    data = await store.get_all(platform.lower())
    return ResponseBase(data=data)
