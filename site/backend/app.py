from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import User, Product, Order, init_db

app = FastAPI()

init_db()

class ProductIn(BaseModel):
    name: str
    description: str = ''
    price: float

@app.get('/products')
def list_products():
    return Product.get_all()

@app.post('/products')
def create_product(p: ProductIn):
    prod = Product.create(p.dict())
    return prod