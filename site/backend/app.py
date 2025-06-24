from fastapi import FastAPI
from pydantic import BaseModel
from models import Product, Order, init_db
from models import DBSession

app = FastAPI(title="Jarvis API")
init_db()

class ProductIn(BaseModel):
    name: str
    description: str = ''
    price: float

class OrderIn(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1

@app.get('/api/products', tags=["Produtos"])
def list_products():
    return Product.get_all()

@app.post('/api/products', tags=["Produtos"])
def create_product(p: ProductIn):
    return Product.create(p.dict())

@app.get('/api/orders', tags=["Pedidos"])
def list_orders():
    session = DBSession()
    return session.query(Order).all()

@app.post('/api/orders', tags=["Pedidos"])
def create_order(order: OrderIn):
    session = DBSession()
    new_order = Order(**order.dict())
    session.add(new_order)
    session.commit()
    return new_order
