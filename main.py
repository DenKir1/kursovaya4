
from classes.classes import HeadHunterAPI, SuperJobAPI, JsonManager, Vacancy
from src.scripts import salary_range, show_top_n, get_vacancies_by_salary, get_vacancy_by_words


def main():
    platform = [HeadHunterAPI, SuperJobAPI]
    player_choice = input(f"""На каком сайте будем искать?
Введите 0 - для HeadHunter, или 1 - для SuperJob, иначе для всего списка сайтов: """)
    player_find = input("Введите название профессии для поиска: ").capitalize()
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

    print(vacancies)

    json_saver = JsonManager()
    json_saver.save_to(vacancies)
    json_saver.sort_vacancies_by_salary()
    vac1 = Vacancy.from_json("data.json")
    print(vac1)

    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filtered_vacancies = get_vacancy_by_words(filter_words, vacancies)
    json_saver.save_to(filtered_vacancies)
    print(filtered_vacancies)

    filter_salary = salary_range()
    filtered_vacancies = get_vacancies_by_salary(filter_salary, filtered_vacancies)
    json_saver.save_to(filtered_vacancies)
    print(filtered_vacancies)


    show_quantity = show_top_n(filtered_vacancies)
    print(show_quantity)
    json_saver = JsonManager()
    json_saver.save_to(show_quantity)


if __name__ == "__main__":
    main()
