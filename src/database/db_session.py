import sqlalchemy
import sqlalchemy.orm as orm

from src.database.modelbase import SQLAlchemyBase

factory = None


def global_init(db_file: str):
    global factory

    if factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("No DB file specified")

    connection = "sqlite:///" + db_file.strip()
    print(f'Connecting to DB with {connection}')

    engine = sqlalchemy.create_engine(connection, echo=True)
    factory = orm.sessionmaker(bind=engine)

    from src.database.tweet import Tweet
    SQLAlchemyBase.metadata.create_all(engine)
