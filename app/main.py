from fastapi import FastAPI
from .database import engine, Base
from .routers import products, sales, inventory

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Admin API")

@app.get("/")
async def root():
    return {"E-commerce Admin API up and running....\n /"
                       "Swagger UI: http://127.0.0.1:8000/docs\n /"
                        "ReDoc: http://127.0.0.1:8000/redoc"}

app.include_router(products.router)
app.include_router(sales.router)
app.include_router(inventory.router)
