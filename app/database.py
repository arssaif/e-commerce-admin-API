import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load from .env or defaults
# Ste proper db if want: "mysql+pymysql://root:password@localhost:3306/ecomdb"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecom.db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
