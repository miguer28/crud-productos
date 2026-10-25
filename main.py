from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import crear_db_y_tablas
from routers import productos

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()          # crea las tablas al iniciar
    yield

app = FastAPI(title="CRUD de Productos", lifespan=lifespan)

app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],        # en producción: la URL de su frontend
     allow_methods=["*"],
     allow_headers=["*"],
 )

app.include_router(productos.router)

@app.get("/")
def raiz():
    return {"mensaje": "API CRUD activa. Visita /docs"}


 

