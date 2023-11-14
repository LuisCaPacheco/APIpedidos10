from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()


usuarios = {}

pedidos = {}

class Usuario(BaseModel):
    id: uuid.UUID
    nombre: str
    email: Optional[str] = None

class Pedido(BaseModel):
    id: uuid.UUID
    usuario_id: uuid.UUID
    descripcion: str
    entregado: bool = False

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