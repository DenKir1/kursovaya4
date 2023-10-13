import os
import requests
import json
# from datetime import datetime
from abc import ABC, abstractmethod


class Vacancy:
    """Класс Вакансий"""

    def __init__(self, name, url, salary, requirements):
        if isinstance(name, str):
            self.name = name
        else:
            self.name = "Noname"

        if isinstance(url, str):
            self.url = url
        else:
            self.url = None

        if isinstance(requirements, str):
            self.requirements = requirements
        else:
            self.requirements = ""

        if isinstance(salary, int):
            self.salary = salary
        else:
            self.salary = 0

    def __eq__(self, other):
        return self.url == other.url

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __repr__(self):
        return f'{self.name} {self.salary} {self.url}\n'

    def show_info(self):
        """Печать подробной информации"""
        print(self.name)
        print(self.url)
        print(f'Заработная плата {self.salary}')
        print(self.requirements)

    def to_json(self):
        """Преобразует Vacancy в JSON"""
        return {
            'name': self.name,
            'url': self.url,
            'salary': self.salary,
            'requirements': self.requirements,
        }

    @classmethod
    def from_json(cls, file):
        """Считывает данные из файла и приводит его к списку Vacancy"""
        with open(file, 'r', encoding='utf-8') as f:
            vacancies = json.load(f)
        output = []
        for vacancy in vacancies:
            tmp = cls(vacancy['name'], vacancy['url'], vacancy['salary'], vacancy['requirements'])
            output.append(tmp)
        return output


class API(ABC):
    """Абстрактный класс API"""
    @abstractmethod
    def get_vacancies(self, words):
        pass

    @abstractmethod
    def format_vacancies(self):
        pass


class HeadHunterAPI(API):
    def __init__(self):
        self.params = {
            'per_page': 100,
            'page': 1
        }
        self.url = 'https://api.hh.ru/vacancies/'
        self.vacancies = []

    def get_vacancies(self, words):
        """Запрос по API """
        self.params['text'] = words
        req = requests.get(self.url, params=self.params)
        vacancies = json.loads(req.text)['items']
        self.vacancies = vacancies
        return vacancies

    def format_vacancies(self):
        """Создает список Vacancy из ответа API"""
        result = []
        for vacancy in self.vacancies:
            if vacancy['salary'] is None:
                salary_ = 0
            elif vacancy['salary']['to']:
                salary_ = int(vacancy['salary']['to'])
            elif vacancy['salary']['from']:
                salary_ = int(vacancy['salary']['from'])
            else:
                salary_ = 0

            tmp = Vacancy(vacancy['name'], f'https://hh.ru/vacancy/{vacancy["id"]}', salary_,
                          vacancy['snippet']['requirement'])
            result.append(tmp)
        return result


class SuperJobAPI(API):
    def __init__(self):
        self.headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': os.getenv("API_SJ"),
        }
        self.params = {
            'count': 100,
            'page': 1,
        }
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.vacancies = []

    def get_vacancies(self, words):
        """Запрос по API """
        self.params['keywords'] = words
        req = requests.get(self.url, params=self.params, headers=self.headers)
        vacancies = json.loads(req.text)['objects']
        self.vacancies = vacancies
        return vacancies

    def format_vacancies(self):
        """Создает список Vacancy из ответа API"""
        result = []
        for vacancy in self.vacancies:
            if vacancy['payment_to']:
                salary_ = int(vacancy['payment_to'])
            elif vacancy['payment_from']:
                salary_ = int(vacancy['payment_from'])
            else:
                salary_ = 0
            tmp = Vacancy(vacancy['profession'], vacancy['link'], salary_, vacancy['candidat'])
            result.append(tmp)
        return result


class FileManager(ABC):
    """Абстрактный менеджер"""
    @abstractmethod
    def check_vacancy(self, vacancy):
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def save_to(self, vacancies):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JsonManager(FileManager, Vacancy):
    """Менеджер JSON"""
    def __init__(self):
        self.file = 'data.json'
        with open(self.file, 'w', encoding='utf-8') as json_file:
            json.dump([], json_file, ensure_ascii=False, indent=4)

    def check_vacancy(self, vacancy: Vacancy):
        """Проверяет наличие одинаковых вакансий"""
        vacancies = self.read_from()
        return vacancy not in vacancies

    def read_from(self):
        """Считывает данные файла и возвращает список типа Vacancy"""
        vacancies = Vacancy.from_json(self.file)
        return vacancies

    def save_to(self, vacancies):
        """Записывает вакансии в файл"""
        vac = []
        if vacancies:
            vac = [i.to_json() for i in vacancies]
        with open(self.file, 'w', encoding='utf-8') as json_file:
            json.dump(vac, json_file, ensure_ascii=False, indent=4)
        print(f"Вакансии сохранены в файл {self.file}")

    def add_vacancy(self, vacancy):
        """Добавляет вакансию в файл"""
        if self.check_vacancy(vacancy):
            vacancies = self.read_from()
            vacancies.append(vacancy)
            vac = [i.to_json() for i in vacancies]
            with open(self.file, 'w', encoding='utf-8') as json_file:
                json.dump(vac, json_file, ensure_ascii=False, indent=4)
            print(f"{vacancy} - добавлено в файл {self.file}")

    def delete_vacancy(self, vacancy: Vacancy):
        """Удаляет вакансию их файла по совпадению URL"""
        vacancies = self.read_from()
        for vacancy_ in vacancies:
            if vacancy_ == vacancy:
                vacancies.remove(vacancy)
        vac = [i.to_json() for i in vacancies]
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(vac, f, ensure_ascii=False, indent=4)
        print(f"{vacancy} - удалено из файла {self.file}")

    def sort_vacancies_by_salary(self):
        """
        Сортирует вакансии по заработной плате (от большего к меньшему)
        """
        vacancies = Vacancy.from_json(self.file)
        vacancies.sort(reverse=True)
        vac = [i.to_json() for i in vacancies]
        with open(self.file, 'w', encoding='utf-8') as file:
            json.dump(vac, file, ensure_ascii=False, indent=4)
        print(f"Файл {self.file} отсортирован.")
