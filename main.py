from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sql_database = 'sqlite:///base.db'
engine = create_engine(sql_database, echo=True)


Base = declarative_base()


class Vac(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    vac = Column(String)
    text = Column(String)
    salary = Column(Integer)

    def __init__(self, city, vac, text, salary):
        self.city = city
        self.vac = vac
        self.text = text
        self.salary = salary

    def __str__(self):
        return f'{self.id}, {self.city}, {self.vac}, {self.text}, {self.salary}'


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

vac_1 = Vac('Москва', 'Программист Python', 'Знание языка Python, знание SQL, Flask, Django', 120000)
vac_2 = Vac('Санкт-Петербург', 'Программист 1С', 'Знание 1С', 180000)

session.add(vac_1)
session.add(vac_2)
session.commit()

vac_query = session.query(Vac)
for vac in vac_query:
    print(vac)
