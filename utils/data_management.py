from sqlalchemy import create_engine, Column, Integer, String, Float, Table, MetaData, Date, ForeignKey
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "sqlite:///./data/database.db"

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

rr_categories_table = Table(
    "rr_categories",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("weight", Float),
)

rr_items_table = Table(
    "rr_items",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("category_id", Integer, ForeignKey("rr_categories.id")),
    Column("name", String, index=True),
    Column("weight", Float),
    Column("start_date", Date),
    Column("end_date", Date),
)

employee_project_table = Table(
    "employee_project",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("employee_id", Integer, ForeignKey("employees.id")),
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("rr_item_id", Integer, ForeignKey("rr_items.id")),
    Column("allocation_rate", Float),
)

def init_db():
    db_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///", ""))
    os.makedirs(db_dir, exist_ok=True)
    metadata.create_all(bind=engine)