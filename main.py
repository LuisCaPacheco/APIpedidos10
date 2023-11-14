from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

usuarios = {}

pedidos = {}

class Order(BaseModel):
    product: str
    quantity: int
    customer: str

class Usuario(BaseModel):
    id: uuid.UUID
    nombre: str
    email: Optional[str] = None

class Pedido(BaseModel):
    id: uuid.UUID
    usuario_id: uuid.UUID
    descripcion: str
    entregado: bool = False


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

def get_usuario(id: uuid.UUID):
    usuario = usuarios.get(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.post("/usuarios/")
def crear_usuario(usuario: Usuario):
    usuarios[usuario.id] = usuario
    return usuario

@app.post("/pedidos/")
def crear_pedido(pedido: Pedido, usuario: Usuario = Depends(get_usuario)):
    pedido.usuario_id = usuario.id
    pedidos[pedido.id] = pedido
    return pedido

@app.get("/pedidos/{pedido_id}")
def obtener_pedido(pedido_id: uuid.UUID):
    pedido = pedidos.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

