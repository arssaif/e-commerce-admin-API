from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from .. import crud, schemas, database
from typing import List, Any

router = APIRouter(prefix="/sales", tags=["sales"])
get_db = lambda: database.SessionLocal()

@router.post("/", response_model=schemas.Sale)
def record_sale(s: schemas.SaleCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db, s)

@router.get("/", response_model=list[schemas.Sale])
def query_sales(
    start: datetime   = Query(..., description="ISO start datetime"),
    end:   datetime   = Query(..., description="ISO end datetime"),
    product_id: Optional[int] = Query(
        None, description="Filter by product ID"
    ),
    category_id: Optional[int] = Query(
        None, description="Filter by category ID"
    ),
    db: Session = Depends(get_db),
):
    return crud.get_sales(db, start, end, product_id, category_id)

@router.get(
    "/revenue/",
    response_model=List[schemas.RevenueItem],
    summary="Get revenue grouped by period"
)
def revenue_report(
    start: datetime = Query(...),
    end: datetime   = Query(...),
    period: str     = Query(
        "daily",
        regex="^(daily|weekly|monthly|yearly)$",
        description="Group by this interval"
    ),
    category_id: Optional[int] = Query(
        None, description="Filter by category ID"
    ),
    db: Session = Depends(get_db),
):
    return crud.get_revenue_grouped(db, start, end, period, category_id)

@router.get(
    "/revenue/compare/",
    response_model=schemas.RevenueCompare,
    summary="Compare revenue between two date ranges"
)
def compare_periods(
    p1_start: datetime,
    p1_end:   datetime,
    p2_start: datetime,
    p2_end:   datetime,
    period: str = Query(
        "monthly",
        regex="^(daily|weekly|monthly|yearly)$",
        description="Group by this interval"
    ),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    r1 = crud.get_revenue_grouped(db, p1_start, p1_end, period, category_id)
    r2 = crud.get_revenue_grouped(db, p2_start, p2_end, period, category_id)
    return {"period1": r1, "period2": r2}
