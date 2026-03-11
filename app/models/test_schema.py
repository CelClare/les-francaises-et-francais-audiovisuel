from pydantic import BaseModel

class TestItemCreate(BaseModel):
    name: str

class TestItemRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True