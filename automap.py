import json
from enum import Enum

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class Item(str, Enum):
    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'


engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/test")

Base = automap_base()
Base.prepare(engine, reflect=True)
Product = Base.classes.products
session = Session(engine)

app = FastAPI()


class ProductModel(BaseModel):
    name: str
    quantity: int = Field(lt=101)


@app.post("/")
async def welcome(product: ProductModel):
    print(product)
    session.add(Product(**product.dict()))
    session.commit()
    return product
    # return json.loads(product)
    # return "<h3>Welcome Broo..!!</h3>"


@app.get('/item/{item_name}')
async def item(item_name: Item):
    return item_name.value


@app.get('/file/{file_path:path}')
async def get_file(file_path: str):
    return file_path


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
