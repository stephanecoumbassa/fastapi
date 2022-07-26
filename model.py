from typing import Union
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class Coord(BaseModel):
    password: str
    lat: float
    lon: float
    zoom: Optional[int] = None


class CoordOut(BaseModel):
    lat: float
    lon: float
    zoom: Optional[int] = None


class Todo(BaseModel):
    name: str
    due_date: str
    description: str


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
