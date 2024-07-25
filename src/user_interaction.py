from prettytable import PrettyTable
from src.connector import Connector
from src.entities import Vacancy
from typing import List, Optional


def filter_vacancies_by_keyword(vacancies: List[Vacancy], keyword: str) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевому слову в названии вакансии.

    :param vacancies: Список вакансий.
    :param keyword: Ключевое слово для фильтрации.
    :return: Список вакансий, содержащих ключевое слово.
    """
    return [vac for vac in vacancies if keyword.lower() in vac.name.lower()]


def start_user_interaction(connector: Connector) -> None:
    """
    Запускает взаимодействие с пользователем через консоль, предлагая различные действия с вакансиями.

    :param connector: Объект Connector для работы с вакансиями.
    """
    while True:
        try:
            print(
                'Действия:\n'
                '1. Получить топ вакансий\n'
                '2. Удалить вакансию\n'
                '3. Фильтровать вакансии по ключевым словам\n'
                '4. Сортировать вакансии\n'
                '5. Просмотр деталей вакансии\n'
                '0. Выйти'
            )
            user_command = input('Введите номер команды: ').strip()

            if user_command == '1':
                print_top_vacancies(connector)
            elif user_command == '2':
                delete_vacancy(connector)
            elif user_command == '3':
                filter_vacancies(connector)
            elif user_command == '4':
                sort_vacancies(connector)
            elif user_command == '5':
                view_vacancy_details(connector)
            elif user_command == '0':
                print("Выход из программы. До свидания!")
                return
            else:
                print("Некорректная команда, попробуйте еще раз.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def print_top_vacancies(connector: Connector) -> None:
    """
    Печатает топ N вакансий, отсортированных по зарплате.

    :param connector: Объект Connector для работы с вакансиями.
    """
    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N: ").strip())
        vacancies = connector.get_vacancies()

        t = PrettyTable(['Название', 'Ссылка', 'Зарплата, от', 'Зарплата, до', 'Валюта'])
        for vac in sorted(vacancies)[:top_n]:
            t.add_row([vac.name, vac.url, vac.salary_from or '- ', vac.salary_to or '- ', vac.salary_currency])
        print(t)
    except ValueError:
        print("Некорректный ввод. Пожалуйста, введите число.")
    except Exception as e:
        print(f"Произошла ошибка при получении топ вакансий: {e}")


def delete_vacancy(connector: Connector) -> None:
    """
    Удаляет вакансию по названию.

    :param connector: Объект Connector для работы с вакансиями.
    """
    try:
        name = input("Введите название вакансии для удаления: ").strip()
        vacancies = connector.get_vacancies()
        vacancy_found = False
        for vac in vacancies:
            if vac.name.lower() == name.lower():
                confirm = input(f"Вы уверены, что хотите удалить вакансию '{vac.name}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    connector.remove_vacancy(vac)
                    print(f"Вакансия '{vac.name}' удалена")
                else:
                    print("Удаление отменено")
                vacancy_found = True
                break
        if not vacancy_found:
            print(f"Вакансия '{name}' не найдена")
    except Exception as e:
        print(f"Произошла ошибка при удалении вакансии: {e}")


def filter_vacancies(connector: Connector) -> None:
    """
    Фильтрует вакансии по ключевому слову.

    :param connector: Объект Connector для работы с вакансиями.
    """
    try:
        keyword = input("Введите ключевое слово для фильтрации вакансий: ").strip()
        vacancies = connector.get_vacancies()
        filtered_vacancies = filter_vacancies_by_keyword(vacancies, keyword)

        if filtered_vacancies:
            print(f"Найдено {len(filtered_vacancies)} вакансий, содержащих ключевое слово '{keyword}':")
            t = PrettyTable(['Название', 'Ссылка', 'Зарплата, от', 'Зарплата, до', 'Валюта'])
            for vac in filtered_vacancies:
                t.add_row([vac.name, vac.url, vac.salary_from or '- ', vac.salary_to or '- ', vac.salary_currency])
            print(t)
        else:
            print(f"Вакансии, содержащие ключевое слово '{keyword}', не найдены.")
    except Exception as e:
        print(f"Произошла ошибка при фильтрации вакансий: {e}")


def sort_vacancies(connector: Connector) -> None:
    """
    Сортирует вакансии по выбранному критерию.

    :param connector: Объект Connector для работы с вакансиями.
    """
    try:
        print(
            'Сортировка по:\n'
            '1. Названию\n'
            '2. Зарплате от\n'
            '3. Зарплате до'
        )
        sort_option = input("Выберите критерий сортировки: ").strip()

        vacancies = connector.get_vacancies()
        if sort_option == '1':
            sorted_vacancies = sorted(vacancies, key=lambda vac: vac.name)
        elif sort_option == '2':
            sorted_vacancies = sorted(vacancies, key=lambda vac: (vac.salary_from or 0))
        elif sort_option == '3':
            sorted_vacancies = sorted(vacancies, key=lambda vac: (vac.salary_to or 0))
        else:
            print("Некорректный выбор. Попробуйте еще раз.")
            return

        t = PrettyTable(['Название', 'Ссылка', 'Зарплата, от', 'Зарплата, до', 'Валюта'])
        for vac in sorted_vacancies:
            t.add_row([vac.name, vac.url, vac.salary_from or '- ', vac.salary_to or '- ', vac.salary_currency])
        print(t)
    except Exception as e:
        print(f"Произошла ошибка при сортировке вакансий: {e}")


def view_vacancy_details(connector: Connector) -> None:
    """
    Просматривает детали вакансии по названию.

    :param connector: Объект Connector для работы с вакансиями.
    """
    try:
        name = input("Введите название вакансии для просмотра деталей: ").strip()
        vacancies = connector.get_vacancies()
        vacancy_found = False
        for vac in vacancies:
            if vac.name.lower() == name.lower():
                t = PrettyTable(['Поле', 'Значение'])
                t.add_row(['Название', vac.name])
                t.add_row(['Ссылка', vac.url])
                t.add_row(['Зарплата, от', vac.salary_from or '-'])
                t.add_row(['Зарплата, до', vac.salary_to or '-'])
                t.add_row(['Валюта', vac.salary_currency])
                print(t)
                vacancy_found = True
                break
        if not vacancy_found:
            print(f"Вакансия '{name}' не найдена")
    except Exception as e:
        print(f"Произошла ошибка при просмотре деталей вакансии: {e}")


def filter_vacancies_by_salary():
    return None
