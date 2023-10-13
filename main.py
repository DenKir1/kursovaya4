
from classes.classes import HeadHunterAPI, SuperJobAPI, JsonManager, Vacancy
from src.scripts import salary_range, show_top_n, get_vacancies_by_salary, get_vacancy_by_words


def main():
    platform = [HeadHunterAPI, SuperJobAPI]
    player_choice = input(f"""На каком сайте будем искать?
Введите 0 - для HeadHunter, или 1 - для SuperJob, иначе для всего списка сайтов: """)
    player_find = input("Введите название профессии для поиска: ")
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    if player_choice == "0":
        api = platform[0]()
        vacancy_raw = api.get_vacancies(player_find)
        vacancies = api.format_vacancies()
    elif player_choice == "1":
        api = platform[1]()
        vacancy_raw = api.get_vacancies(player_find)
        vacancies = api.format_vacancies()
    else:
        hh_api = platform[0]()
        sj_api = platform[1]()
        hh_vacancies = hh_api.get_vacancies(player_find)
        superjob_vacancies = sj_api.get_vacancies(player_find)
        vacancies = hh_api.format_vacancies() + sj_api.format_vacancies()

    # Создание экземпляра класса JsonManager для сохранения в файл
    json_saver = JsonManager()
    json_saver.save_to(vacancies)

    # Начнем фильтрацию по ключевым словам и зарплате
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ")
    vacancies_filtered = get_vacancy_by_words(filter_words, vacancies)
    json_saver.save_to(vacancies_filtered)
    print(vacancies_filtered)

    filter_salary = salary_range()
    vacancies_ranged = get_vacancies_by_salary(filter_salary, vacancies_filtered)
    json_saver.save_to(vacancies_ranged)
    print(vacancies_ranged)

    # Отсортируем файл по зарплате
    json_saver.sort_vacancies_by_salary()
    show_top = show_top_n(vacancies_ranged)

    # Сохраним в файл N топов
    json_saver.save_to(show_top)
    json_saver.sort_vacancies_by_salary()

    # Минутка юмора
    vacancy_one = Vacancy("Надоедливый тип", "<https://hh.ru/vacancy/123456>", 42, "Опыт работы от 3 лет...")
    json_saver.add_vacancy(vacancy_one)
    vac_read1 = json_saver.read_from()
    print(vac_read1)
    json_saver.delete_vacancy(vacancy_one)
    vac_read2 = json_saver.read_from()
    print(vac_read2)


if __name__ == "__main__":
    main()
