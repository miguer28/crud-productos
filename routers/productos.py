from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import get_session
from models import (Producto, ProductoCrear,
                     ProductoActualizar, ProductoLeer)
 
router = APIRouter(prefix="/products", tags=["products"])
 
 # CREATE
@router.post("/", response_model=ProductoLeer, status_code=201)
def crear(datos: ProductoCrear, session: Session = Depends(get_session)):
    producto = Producto.model_validate(datos)
    session.add(producto)
    session.commit()
    session.refresh(producto)  # recupera el id generado
    return producto
      
# READ ALL (paginado y filtrable)
@router.get("/", response_model=list[ProductoLeer])
def listar(session: Session = Depends(get_session),
           offset: int = 0,
           limit: int = Query(default=20, le=100),
           categoria: str | None = None):
    consulta = select(Producto)
    if categoria:
        consulta = consulta.where(Producto.categoria == categoria)
    return session.exec(consulta.offset(offset).limit(limit)).all()


# READ ONE
@router.get("/{producto_id}", response_model=ProductoLeer)
def obtener(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

 # UPDATE (parcial)
@router.patch("/{producto_id}", response_model=ProductoLeer)
def actualizar(producto_id: int, cambios: ProductoActualizar,
                session: Session = Depends(get_session)):
     producto = session.get(Producto, producto_id)
     if not producto:
         raise HTTPException(status_code=404, detail="Producto no encontrado")
     datos = cambios.model_dump(exclude_unset=True)
     for campo, valor in datos.items():
         setattr(producto, campo, valor)
     session.add(producto)
     session.commit()
     session.refresh(producto)
     return producto

 # DELETE
@router.delete("/{producto_id}", status_code=204)
def eliminar(producto_id: int, session: Session = Depends(get_session)):
     producto = session.get(Producto, producto_id)
     if not producto:
         raise HTTPException(status_code=404, detail="Producto no encontrado")
     session.delete(producto)
     session.commit()
