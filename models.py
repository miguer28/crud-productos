from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class ProductoBase(SQLModel):
    nombre: str = Field(index=True, min_length=1, max_length=120)
    descripcion: Optional[str] = None
    precio: float = Field(gt=0)                 # debe ser > 0
    stock: int = Field(default=0, ge=0)         # no negativo
    categoria: Optional[str] = Field(default=None, index=True)
    imagen_url: Optional[str] = None            # <--- AGREGAR ESTA LÍNEA

# Tabla real en la base de datos
class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creado_en: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # ✅ corregido aquí

# Datos que envía el cliente al crear
class ProductoCrear(ProductoBase):
    pass

# Datos al actualizar (todos opcionales: actualización parcial)
class ProductoActualizar(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    categoria: Optional[str] = None

# Datos que devuelve la API
class ProductoLeer(ProductoBase):
    id: int
    creado_en: datetime   