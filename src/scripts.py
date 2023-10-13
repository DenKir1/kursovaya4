from classes.classes import Vacancy


def get_vacancies_by_salary(salary_range, vacancies):
    """Отбор вакансий по диапазону заработной платы"""
    salary_from = salary_range[0]
    salary_to = salary_range[1]

    get_vac = []
    for vacancy_ in vacancies:
        if salary_from < vacancy_.salary < salary_to:
            get_vac.append(vacancy_)
    return get_vac


def get_vacancy_by_words(words, vacancies):
    """Отбор по ключевым словам"""
    get_vac = []
    for vacancy_ in vacancies:
        if vacancy_.requirements:
            vacancy_words = vacancy_.requirements + vacancy_.name
            flag = True
            for word in words.split(" "):
                if word.lower() in vacancy_words.lower():
                    if flag:
                        get_vac.append(vacancy_)
                        flag = False
    return get_vac


def salary_range():
    """Создает список из введенного диапазона оклада через пробел"""
    nom = input('Введите диапазон оклада через пробел\nНапример: 1000 20000 - ')
    try:
        range_ = [int(i) for i in nom.strip().split()]
        if len(range_) == 2:
            return range_
    except Exception:
        print("Неправильно введен диапазон")
        exit()


def show_top_n(vacancies):
    """Выводит в консоль информацию о первых N вакансиях"""
    try:
        n = int(input('Введите количество вакансий для просмотра '))
        if n <= len(vacancies):
            for i in vacancies[:n]:
                i.show_info()
                return vacancies[:n]
    except Exception:
        print('Число введено некорректно')
        exit()
