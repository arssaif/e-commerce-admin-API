from sqlalchemy.orm import Session, joinedload
from . import models, schemas
from datetime import datetime
from sqlalchemy import func, extract

# Products
def create_product(db: Session, p: schemas.ProductCreate):
    db_p = models.Product(**p.dict())
    db.add(db_p)
    db.commit()
    db.refresh(db_p)
    return db_p

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Product)
        .options(joinedload(models.Product.category))
        .offset(skip)
        .limit(limit)
        .all()
    )

# Sales
def create_sale(db: Session, s: schemas.SaleCreate):
    db_s = models.Sale(**s.dict())
    db.add(db_s)
    # update inventory
    inv = db.query(models.Inventory).filter_by(product_id=s.product_id).first()
    if inv:
        inv.quantity -= s.quantity
        inv.last_updated = datetime.now()
    db.commit()
    db.refresh(db_s)
    return db_s

def get_sales(
    db: Session,
    start: datetime,
    end: datetime,
    product_id: int | None    = None,
    category_id: int | None   = None,
):
    # join through Product so we can filter on category
    q = db.query(models.Sale).join(models.Product)

    # base date‐range filter
    q = q.filter(models.Sale.sold_at.between(start, end))

    if product_id is not None:
        q = q.filter(models.Sale.product_id == product_id)

    if category_id is not None:
        q = q.filter(models.Product.category_id == category_id)

    return q.all()

def get_revenue_grouped(
    db: Session,
    start: datetime,
    end: datetime,
    period: str,           # "daily", "weekly", "monthly", "yearly"
    category_id: int | None = None,
):
    sale = models.Sale
    prod = models.Product

    # pick the right grouping function
    if period == "daily":
        grp = func.date(sale.sold_at)
    elif period == "weekly":
        # ISO week number; you could also group by year+week combo
        grp = extract("week", sale.sold_at)
    elif period == "monthly":
        grp = extract("month", sale.sold_at)
    else:  # yearly
        grp = extract("year", sale.sold_at)

    q = (
      db.query(
        grp.label("period"),
        func.sum(sale.total_price).label("revenue")
      )
      .join(prod)
      .filter(sale.sold_at.between(start, end))
    )

    if category_id:
        q = q.filter(prod.category_id == category_id)

    q = q.group_by("period").order_by("period")
    return [{"period": r.period, "revenue": float(r.revenue)} for r in q]

# Inventory
def get_inventory(db: Session):
    return db.query(models.Inventory).all()

def update_inventory(db: Session, product_id: int, qty: int):
    inv = db.query(models.Inventory).filter_by(product_id=product_id).first()
    if inv:
        inv.quantity = qty
        inv.last_updated = datetime.now()
    else:
        inv = models.Inventory(product_id=product_id, quantity=qty, last_updated=datetime.now())
        db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv
