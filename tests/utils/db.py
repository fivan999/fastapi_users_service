from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from src.db.base import Base


def recreate_db_tables(engine: Engine) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def clear_db_tables(db_sessionmaker: sessionmaker) -> None:
    session = db_sessionmaker()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(text(f"DELETE FROM {table.name};"))
        session.execute(
            text(f"ALTER SEQUENCE {table.name}_id_seq RESTART WITH 1;")
        )
    session.commit()
    session.close()
