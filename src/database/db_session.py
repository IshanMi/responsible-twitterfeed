import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import sessionmaker
from src.database.modelbase import SQLAlchemyBase


def create_session_maker(conn: str) -> sessionmaker:
    engine = sqlalchemy.create_engine(conn, echo=False)
    session_maker = orm.sessionmaker(bind=engine)

    SQLAlchemyBase.metadata.create_all(engine)
    return session_maker
