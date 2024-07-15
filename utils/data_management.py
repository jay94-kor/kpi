from sqlalchemy import create_engine, Column, Integer, String, Float, Table, MetaData
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///data/database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

projects_table = Table(
    "projects",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("cost", Float),
    Column("budget", Float),
    Column("margin", Float),
)

employees_table = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
)

def init_db():
    metadata.create_all(bind=engine)
