from abc import ABC, abstractmethod
import requests
from tqdm import tqdm
from typing import List, Dict
from src.entities import Vacancy


class BaseVacanciesAPI(ABC):
    """
    Абстрактный базовый класс для API вакансий.
    """

    @abstractmethod
    def get_vacancies(self, search_text: str) -> List[Vacancy]:
        """
        Метод для получения списка вакансий.

        :param search_text: Текст для поиска вакансий.
        :return: Список вакансий.
        """
        pass


class HHVacanciesAPI(BaseVacanciesAPI):
    """
    Класс для взаимодействия с API HeadHunter для получения вакансий.
    """

    def get_vacancies(self, search_text: str) -> List[Vacancy]:
        """
        Получает список вакансий с сайта HeadHunter.

        :param search_text: Текст для поиска вакансий.
        :return: Список вакансий.
        """
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': search_text,
            'only_with_salary': True,
            'per_page': 100
        }

        raw_vacancies = self._get_list(url, params, max_pages=20)
        return [
            Vacancy(
                name=data['name'],
                url=data['alternate_url'],
                salary_currency=data['salary']['currency'],
                salary_from=data['salary']['from'],
                salary_to=data['salary']['to']
            )
            for data in raw_vacancies
        ]

    def _get_list(self, url: str, params: Dict[str, str], max_pages: int = 1) -> List[Dict]:
        """
        Получает список данных с указанного URL с заданными параметрами и количеством страниц.

        :param url: URL для запроса.
        :param params: Параметры запроса.
        :param max_pages: Максимальное количество страниц для получения данных.
        :return: Список данных.
        """
        items = []
        for current_page in tqdm(range(0, max_pages), desc='Progress'):
            params['page'] = current_page

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data['found'] == 0:
                break
            items.extend(data['items'])

        return items
