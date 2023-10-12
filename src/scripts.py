from classes.classes import Vacancy


def get_vacancies_by_salary(salary_range, vacancies):
    """
    Выводит названия вакансий в консоль по диапазону заработной платы
    """
    salary_from = salary_range[0]
    salary_to = salary_range[1]

    get_vac = []
    for vacancy_ in vacancies:
        if salary_from < vacancy_.salary < salary_to:
            get_vac.append(vacancy_)
    return get_vac


def get_vacancy_by_words(words, vacancies):
    vacan = []
    get_vac = []
    for vacancy_ in vacancies:
        for word in words:
            if word.lower() in (vacancy_.requirements.lower(), vacancy_.name.lower()):
                get_vac.append(vacancy_)
    return get_vac


def salary_range():
    """ """
    nom = input('Введите диапазон оклада через пробел\nНапример: 1000 20000 - ')
    try:
        range_ = [int(i) for i in nom.strip().split()]
        if len(range_) == 2:
            return range_
    except Exception:
        print(f"Неправильно введен диапазон")
        exit()


def show_top_n(vacancies):
    """Выводит в консоль информацию о первых н вакансиях"""
    try:
        n = int(input('Введите количество вакансий для просмотра '))
        if n <= len(vacancies):
            return vacancies[:n]
    except Exception:
        print('Число введено некорректно')
        exit()
