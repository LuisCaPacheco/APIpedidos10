from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.templating import Jinja2Templates

app = FastAPI()

class Order(BaseModel):
    product: str
    quantity: int
    customer: str

orders = []

templates = Jinja2Templates(directory="templates")

@app.post("/orders/")
def create_order(order: Order):
    orders.append(order)
    return {"Order ID": len(orders)}

@app.get("/orders/")
def read_orders():
    return orders

@app.get("/order_form")
def order_form(request: Request):
    return templates.TemplateResponse("order_form.html", {"request": request})