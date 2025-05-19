import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import database, models
from app.database import engine

# ensure all tables are created
models.Base.metadata.create_all(bind=engine)

def get_or_create_category(db, name):
    cat = db.query(models.Category).filter_by(name=name).first()
    if not cat:
        cat = models.Category(name=name)
        db.add(cat)
        db.commit()
        db.refresh(cat)
    return cat

def populate():
    db: Session = database.SessionLocal()

    # categories
    names = ["Electronics", "Clothing", "Home", "Fashion"]
    category = [get_or_create_category(db, n) for n in names]
    db.add_all(category); db.commit()

    # products
    prods = []
    for c in category:
        for i in range(1, 6):
            p = models.Product(
                name=f"{c.name} Item {i}", category_id=c.id,
                price=round(random.uniform(10, 200), 2)
            )
            prods.append(p)
    db.add_all(prods); db.commit()

    # inventory entries
    for p in prods:
        inv = models.Inventory(
            product_id=p.id,
            quantity=random.randint(10, 100),
            last_updated=datetime.now()
        )
        db.add(inv)
    db.commit()

    # sales history (last 30 days)
    for _ in range(100):
        p = random.choice(prods)
        qty = random.randint(1, 5)
        sale = models.Sale(
            product_id=p.id,
            quantity=qty,
            total_price=round(qty * p.price, 2),
            sold_at=datetime.now() - timedelta(days=random.randint(0,29))
        )
        db.add(sale)
        # update inventory
        inv = db.query(models.Inventory).filter_by(product_id=p.id).first()
        inv.quantity = max(inv.quantity - qty, 0)
        inv.last_updated = datetime.now()
    db.commit()
    db.close()

if __name__ == "__main__":
    populate()
    print("Demo data loaded")
