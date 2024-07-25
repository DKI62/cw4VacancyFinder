from pathlib import Path
from src.api import HHVacanciesAPI
from src.config import DATA_DIR
from src.connector import JsonConnector
from src.user_interaction import start_user_interaction

VACANCIES_PATH = DATA_DIR / "vacancies.json"

api_client = HHVacanciesAPI()
connector = JsonConnector(VACANCIES_PATH)


def main() -> None:
    """
    Главная функция для запуска приложения.
    Запрашивает у пользователя текст для поиска вакансий, получает вакансии через API, сохраняет их в файл
    и запускает взаимодействие с пользователем через консоль.
    """
    print('Добро пожаловать!')
    search_text = input('Введите текст для поиска вакансий:')

    print('Получаем вакансии...')
    vacancies = api_client.get_vacancies(search_text)

    print('Сохраняем вакансии...')
    for vac in vacancies:
        connector.add_vacancy(vac)

    start_user_interaction(connector)


if __name__ == "__main__":
    main()
