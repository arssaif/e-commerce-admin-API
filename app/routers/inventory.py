from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/inventory", tags=["inventory"])
get_db = lambda: database.SessionLocal()

@router.get("/", response_model=list[schemas.Inventory])
def read_inventory(db: Session = Depends(get_db)):
    return crud.get_inventory(db)

@router.put("/{product_id}", response_model=schemas.Inventory)
def set_inventory(product_id: int, qty: int, db: Session = Depends(get_db)):
    return crud.update_inventory(db, product_id, qty)
