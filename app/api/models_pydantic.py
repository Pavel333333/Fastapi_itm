from pydantic import BaseModel

class Image(BaseModel):
    id: int

class DocDeleteRequest(BaseModel):
    id: int

class ResponseModel(BaseModel):
    message: str
    detail: str
