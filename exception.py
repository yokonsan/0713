from enum import Enum
from typing import Union


class ErrorCode(Enum):
    BAD_REQUEST_ERROR = 10
    MISS_REQUIRED_VARIABLE_ERROR = 11
    MAX_RETRY_ERROR = 12
    REQUEST_PARAMS_ERROR = 13


class SuccessCode(Enum):
    SUCCESS = 0


ReturnCode = Union[ErrorCode, SuccessCode]


class APPBaseException(Exception):
    code: ErrorCode
    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class MaxRetryError(APPBaseException):
    """请求最大重试错误"""
    code = ErrorCode.MAX_RETRY_ERROR


class RequestParamsError(APPBaseException):
    """请求参数异常"""
    code = ErrorCode.REQUEST_PARAMS_ERROR
