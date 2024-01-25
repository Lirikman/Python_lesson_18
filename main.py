import random
import requests
from flask import Flask, render_template, request, redirect
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
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


# vac_1 = Vac('Москва', 'Программист Python', 'Знание языка Python, знание SQL, Flask, Django', 120000)
# vac_2 = Vac('Санкт-Петербург', 'Программист 1С', 'Знание 1С', 180000)


# session.add(vac_1)
# session.add(vac_2)
# session.commit()

# vac_query = session.query(Vac)
# for vac in vac_query:
#    print(vac)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/parsing.html')
def parsing():
    return render_template('parsing.html')


@app.route('/base.html', methods=['POST', 'GET'])
def base():
    if request.method == "POST":
        # Парсинг HH.RU
        area = request.form['city']
        city = ''
        if area == '4':
            city = 'Новосибирск'
        elif area == '54':
            city = 'Красноярск'
        elif area == '68':
            city = 'Омск'
        elif area == '90':
            city = 'Томск'
        vac_text = request.form['vac']
        url = 'https://api.hh.ru/vacancies'
        params = {'text': f'NAME:({vac_text})', 'area': area}
        result = requests.get(url, params=params).json()
        total_pages = result['pages']
        vac_json = []
        # Расчёт средней заработной платы
        for i in range(total_pages):
            url = 'https://api.hh.ru/vacancies'
            params = {'text': f'NAME:({vac_text})', 'area': area, 'page': i, 'per_page': 20}
            vac_json.append(requests.get(url, params=params).json())
        all_salary = 0
        all_vac = 0
        for i in vac_json:
            items = i['items']
            count_vac = 0
            summ_salary = 0
            for j in items:
                if j['salary'] is not None:
                    s = j['salary']
                    if s['from'] is not None:
                        count_vac += 1
                        summ_salary += s['from']
            all_salary += summ_salary
            all_vac += count_vac
        average_salary = all_salary // all_vac
        # Выбор 4 рандомных навыков
        all_skills = []
        for i in vac_json:
            items = i['items']
            for j in items:
                if j['snippet'] is not None:
                    k = j['snippet']
                    if k['requirement'] is not None:
                        all_skills.append(k['requirement'])
        list_tmp = []
        for i in all_skills:
            text = i.find('Требования:')
            if text is not None:
                list_tmp.append(i[i.find('Требования: ') + 1:])
        skills = []
        for i in list_tmp:
            temp = str(i).split('.')
            for j in temp:
                if len(j) < 5:
                    temp.remove(j)
                temp.pop()
                for k in temp:
                    skills.append(k)
        for i in skills:
            text = str(i).split('.')
            if len(text) > 5:
                if text[0] == 'Опыт':
                    skills.remove(i)
        random_skills = random.sample(skills, 4)
        skill_1 = random_skills[0]
        skill_2 = random_skills[1]
        skill_3 = random_skills[2]
        skill_4 = random_skills[3]
        skill_txt = str(skill_1) + '\n' + str(skill_2) + '\n' + str(skill_3) + '\n' + str(skill_4)

        s = Vac(city=city, vac=vac_text, text=skill_txt, salary=average_salary)

        try:
            session.add(s)
            session.commit()
            return redirect('base.html')
        except:
            session.rollback()
            return 'Ошибка добавления записи в БД'
    else:
        all_str = session.query(Vac).all()
        all_id = [x.id for x in session.query(Vac).distinct()]
        return render_template('base.html', all_str=all_str, all_id=all_id)


@app.route('/delete.html', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        check_none = session.query(Vac).all()
        if len(check_none) > 0:
            number = request.form['number']
            record = session.query(Vac).filter(Vac.id == number).first()
            try:
                session.delete(record)
                session.commit()
                return redirect('base.html')
            except:
                return 'Ошибка удаления записи из БД'
        else:
            return redirect('base.html')
    else:
        all_str = session.query(Vac).all()
        return render_template('base.html', all_str=all_str)


if __name__ == '__main__':
    app.run(debug=True)
