from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from .. import crud, schemas, database

router = APIRouter(prefix="/sales", tags=["sales"])
get_db = lambda: database.SessionLocal()

@router.post("/", response_model=schemas.Sale)
def record_sale(s: schemas.SaleCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db, s)

@router.get("/", response_model=list[schemas.Sale])
def query_sales(
    start: datetime = Query(...),
    end: datetime = Query(...),
    db: Session = Depends(get_db)
):
    return crud.get_sales(db, start, end)
