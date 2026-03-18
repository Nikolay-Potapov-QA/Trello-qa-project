from pydantic import BaseModel, Field

class BoardModel(BaseModel):
    id: str
    name: str
    closed: bool
    url: str

class CardModel(BaseModel):
    id: str
    name: str
    idList: str
    closed: bool
    idBoard: str

class ListModel(BaseModel):
    id: str
    name: str
    closed: bool
    idBoard: str