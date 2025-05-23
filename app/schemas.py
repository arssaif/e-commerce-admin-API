from pydantic import BaseModel
from datetime import datetime
from typing import List, Any

class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    id: int
    model_config = {"from_attributes": True}

class ProductBase(BaseModel):
    name: str
    category_id: int
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    category: Category | None
    model_config = {"from_attributes": True}

class InventoryBase(BaseModel):
    product_id: int
    quantity: int

class Inventory(InventoryBase):
    id: int
    last_updated: datetime
    product: Product
    model_config = {"from_attributes": True}

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    sold_at: datetime

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    product: Product
    model_config = {"from_attributes": True}

class RevenueItem(BaseModel):
    period: Any      # int for week/month/year or date for daily
    revenue: float

class RevenueCompare(BaseModel):
    period1: List[RevenueItem]
    period2: List[RevenueItem]