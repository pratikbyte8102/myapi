from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables
from routers import items, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(items.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}