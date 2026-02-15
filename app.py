from fastapi import FastAPI
from config.db import engine, Base
from routes import item
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Items",
    description="Ejercicio práctico de API REST con FastAPI, SQLAlchemy y SQlite para Kalmy",
    docs_url="/docs"
)

app.include_router(item.router)