from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        from_attributes = True


class IntId(BaseModel):
    id: int
