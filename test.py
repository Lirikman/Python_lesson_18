from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker


class Vac(object):
    pass


def loadSession(db):
    engine = create_engine(f'sqlite:///{db}', echo=True)
    metadata = MetaData(engine)
    vac_params = Table('vacancies', metadata, autoload=True)

    print(type(vac_params), vac_params.unique_params)

    mapper(Vac, vac_params)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == '__main__':
    db = 'my_database.db'
    session = loadSession(db)
    vac_query = session.query(Vac).all()

    for vac in vac_query:
        print(vac)
