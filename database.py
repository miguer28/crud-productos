from sqlmodel import SQLModel, create_engine, Session

SQLITE_URL = "sqlite:///crud.db"
engine = create_engine(SQLITE_URL, echo=False,
                       connect_args={"check_same_thread": False})

def crear_db_y_tablas():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session