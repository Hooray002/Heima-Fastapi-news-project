import traceback
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

async def http_exception_handler(
    request: Request,
    exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

async def integrity_exception_handler(
        request: Request,
        exc: IntegrityError
):
    error_msg = str(exc.orig)

    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据约束冲突，请检查输入"

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"code": status.HTTP_409_CONFLICT, "message": detail, "data": None},
    )

async def sqlalchemy_error_handler(
        request: Request,
        exc: SQLAlchemyError
):
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": f"数据库操作失败: {str(exc)}",
            "data": None
        }
    )

async def genral_exception_handler(
    request: Request,
    exc: Exception
):
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }
    )