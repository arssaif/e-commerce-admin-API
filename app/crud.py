from sqlalchemy.orm import Session, joinedload
from . import models, schemas
from datetime import datetime

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

def get_sales(db: Session, start: datetime, end: datetime):
    return db.query(models.Sale).filter(models.Sale.sold_at.between(start, end)).all()

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
