from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True, pool_size=6, max_overflow=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Создает и возвращает объект сессии базы данных.
    Используется в контексте менеджера (например, в FastAPI).

    :yield: Объект сессии базы данных (Session).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
