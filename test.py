from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import registry, sessionmaker


class Vac(object):
    pass


def loadSession():
    engine = create_engine('sqlite:///base.db', echo=True)
    metadata = MetaData()
    vac_params = Table('vacancies', metadata, autoload_with=engine)

    print(type(vac_params), vac_params.unique_params)

    mapper_reg = registry()
    mapper_reg.map_imperatively(Vac, vac_params)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == '__main__':
    session = loadSession()
    vacs_query = session.query(Vac).all()

    for vac in vacs_query:
        print(vac)
