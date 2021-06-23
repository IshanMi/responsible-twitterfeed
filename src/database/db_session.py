import sqlalchemy
import sqlalchemy.orm as orm

factory = None


def global_init(db_file: str):
    global factory

    if factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("No DB file specified")

    connection = ""
    engine = sqlalchemy.create_engine(connection, echo=True)
    factory = orm.sessionmaker(bind=engine)