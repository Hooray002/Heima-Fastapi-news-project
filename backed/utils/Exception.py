import traceback
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from starlette import status

DEBUG_MODE = True

async def http_exception_handler(
    request: Request,
    exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code":exc.status_code,
            "message":exc.detail,
            "data": None
        }
    )

async def integrity_exception_handler(
        request: Request,
        exc: IntegrityError
):
    error_msg = str(exc.orig)

    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail="用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        detail="关联数据不存在"
    else:
        detaiil="数据约束冲突，请检查输入"

async def sqlalchemy_error_handler(
        request: Request,
        exc: SQLAlchemyError
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code":500,
            "message": "数据库操作失败，请稍候重试",
            "date":None
        }
    )

async def genral_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }
    )