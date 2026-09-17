from fastapi import HTTPException
from utils.Exception import genral_exception_handler, http_exception_handler, integrity_exception_handler, sqlalchemy_error_handler
from sqlalchemy.exc import IntegrityError,SQLAlchemyError

def register_exception_handlers(app):
    app.add_exception_handler(HTTPException,http_exception_handler)
    app.add_exception_handler(IntegrityError,integrity_exception_handler)
    app.add_exception_handler(SQLAlchemyError,sqlalchemy_error_handler)
    app.add_exception_handler(Exception,genral_exception_handler)