from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import  FLOAT, DATE , String


DeclarativeBase = declarative_base()

DATABASE = {
    "drivername": "postgres",
    "host": 'localhost',
    "port": '5432',
    "username": 'postgres',
    "password": 'weakpassword',
    "database": 'tutorialdb',
}

def db_connect() -> Engine:
    """
    Creates database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE))


def create_items_table(engine: Engine):
    """
    Create the Items table
    """
    DeclarativeBase.metadata.create_all(engine)


class Items(DeclarativeBase):
    """
    Defines the items model
    """

    __tablename__ = "mystocklists"
    # Left hand side is the original API key name
    id = Column("id", Integer, primary_key=True)
    Date = Column("transaction_date", DATE)
    Symbol = Column("symbol", String)
    Volume = Column("volume", FLOAT)
    High = Column("open_value", FLOAT)
    Low = Column("high_value", FLOAT)
    Monthly_Adjusted_Value = Column("low_value", FLOAT)
    Open = Column("price", FLOAT)
    Dividend_Amount = Column("dividend_amount", FLOAT)