import os
from sqlmodel import create_engine, SQLModel, text, Session
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
engine = create_engine(os.getenv("DATABASE_ENGINE"),
                       pool_size=int(os.getenv("DATABASE_POOL_SIZE", 10)))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def check_availability() -> bool:
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print("Database not available")
        return False
