import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import sessionmaker
from src.database.modelbase import SQLAlchemyBase


def create_session(db_file: str) -> sessionmaker:
    connection = "sqlite:///" + db_file.strip()
    print(f'Connecting to DB @ {connection}')

    engine = sqlalchemy.create_engine(connection, echo=True)
    session_maker = orm.sessionmaker(bind=engine)

    SQLAlchemyBase.metadata.create_all(engine)
    return session_maker
