import requests
from datetime import datetime
import json
import os
from abc import ABC, abstractmethod

# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
superjob_api = SuperJobAPI()

# Получение вакансий с разных платформ
hh_vacancies = hh_api.get_vacancies("Python")
superjob_vacancies = superjob_api.get_vacancies("Python")

# Создание экземпляра класса для работы с вакансиями
vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")

# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()
json_saver.add_vacancy(vacancy)
json_saver.get_vacancies_by_salary("100 000-150 000 руб.")
json_saver.delete_vacancy(vacancy)

# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = ["HeadHunter", "SuperJob"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()

class Vacancy:
    def __init__(self, name, page, top_n):
        self.name = name
        self.page = page
        self.top_n = top_n

    def __repr__(self):
        return f'{self.name}'

class HH(Vacancy, APIManager):
    def __init__(self, name, page, top_n):
        super().__init__(name, page, top_n)
        self.url = 'https://api.hh.ru'


    def get_vacancies(self):
        """Выгрузка данных по 'HH' по запросам пользователя и возвращается словарь"""

        data = requests.get(f'{self.url}/vacancies', params={'text': self.name, 'page': self.page, 'per_page': self.top_n}).json()
        return data

    def load_vacancy(self):
        """Проходим циклом по словарю берем из словаря только нужные нам данные и записываем их в переменную 'vacancies' """
        data = self.get_vacancies()
        vacancies = []
        for vacancy in data.get('items', []):
            published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            vacancy_info = {
                'id': vacancy['id'],
                'name': vacancy['name'],
                'solary_ot': vacancy['salary']['from'] if vacancy.get('salary') else None,
                'solary_do': vacancy['salary']['to'] if vacancy.get('salary') else None,
                'responsibility': vacancy['snippet']['responsibility'],
                'data': published_at.strftime("%d.%m.%Y")
            }
            vacancies.append(vacancy_info)

        return vacancies

class Super_job(Vakancy, APIManager):
    def __init__(self, name, page, top_n):
        super().__init__(name, page, top_n)
        self.url = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancies(self):
        """Выгрузка данных по 'Super_job' по запросам пользователя  по АПИ - ключу и возвращается словарь"""

        headers = {
                    'X-Api-App-Id': os.getenv('API_KEY_SJ'),
                }
        data = requests.get(self.url, headers=headers,params={'keywords': self.name, 'page': self.page, 'count': self.top_n}).json()
        return data

    def load_vacancy(self):
        """Проходим циклом по словарю берем из словаря только нужные нам данные и записываем их в переменную 'vacancy_list_SJ' """
        data = self.get_vacancies()
        vacancy_list_SJ = []
        for i in data['objects']:
            published_at = datetime.fromtimestamp(i.get('date_published', ''))
            super_job = {
                'id': i['id'],
                'name': i.get('profession', ''),
                'solary_ot': i.get('payment_from', '') if i.get('payment_from') else None,
                'solary_do': i.get('payment_to') if i.get('payment_to') else None,
                'responsibility': i.get('candidat').replace('\n', '').replace('•', '') if i.get('candidat') else None,
                'data': published_at.strftime("%d.%m.%Y"),

            }
            vacancy_list_SJ.append(super_job)
        return vacancy_list_SJ

def job_vacancy():
    """Основной код проекта, после внесения пользователем данных, данные сортируются согласно запросу пользователя и вносятся в json файл
       далее выбирается площадка для поиска вакансий если пользователь хочет еще просмотреть вакансии нажимает 'y' и подгружаются новые вакансии
       и перезаписывается файл json и так до бесконечности"""
    name = input('Введите вакансию: ')
    top_n = input('Введите кол-во вакансий: ')
    page = int(input('Введите страницу: '))
    hh_instance = HH(name, page, top_n)
    sj_instance = Super_job(name, page, top_n)
    combined_dict = {'HH': hh_instance.load_vacancy(), 'SJ': sj_instance.load_vacancy()}


    with open('Super_job.json', 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=2)


    platforma = input('введите платформу для поиска: (1 - HH, 2 - SJ, 3 - обе платформы)  ')

    if platforma =='3':
        while True:
            hh_instance.page = page
            sj_instance.page = page
            hh_data = hh_instance.load_vacancy()
            sj_data = sj_instance.load_vacancy()

            combined_dict['HH'] = hh_data
            combined_dict['SJ'] = sj_data

            with open('Super_job.json', 'w', encoding='utf-8') as file:
                json.dump(combined_dict, file, ensure_ascii=False, indent=2)

            for platform, data in combined_dict.items():
                print(f"\n \033Платформа: {platform}")
                for item in data:
                    print(f"id - {item['id']}\nДолжность - {item['name']}\nЗ.п от - {item['solary_ot']}\nЗ.п до - {item['solary_do']}\nОписание - {item['responsibility']}\nДата - {item['data']}\n")

            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break
    elif platforma =='1':
        while True:
            hh_instance.page = page
            sj_instance.page = page
            hh_data = hh_instance.load_vacancy()

            combined_dict['HH'] = hh_data

            with open('Super_job.json', 'w', encoding='utf-8') as file:
                json.dump(combined_dict, file, ensure_ascii=False, indent=2)

            for platform in combined_dict['HH']:
                print(f"\nid - {platform['id']}\nДолжность - {platform['name']}\nЗ.п от - {platform['solary_ot']}\nЗ.п до - {platform['solary_ot']}\nОписание - {platform['responsibility']}\nДата - {platform['data']}\n")
            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break

    elif platforma =='2':
        while True:
            hh_instance.page = page
            sj_instance.page = page
            hh_data = hh_instance.load_vacancy()
            sj_data = sj_instance.load_vacancy()

            combined_dict['HH'] = hh_data
            combined_dict['SJ'] = sj_data

            with open('Super_job.json', 'w', encoding='utf-8') as file:
                json.dump(combined_dict, file, ensure_ascii=False, indent=2)

            for platform in combined_dict['SJ']:
                print(f"\nid - {platform['id']}\nДолжность - {platform['name']}\nЗ.п от - {platform['solary_ot']}\nЗ.п до - {platform['solary_do']}\nОписание - {platform['responsibility']}\nДата - {platform['data']}\n")

            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break

job_vacancy()