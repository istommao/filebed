from .sanic_motor import BaseModel


class File(BaseModel):
    __coll__ = 'Files'
    # name:str
    # type:str
    # size:int
    # path:str
    # create_at:int Unix时间戳
