import json
from abc import ABC, abstractmethod
from dataclasses import asdict
from pathlib import Path
from typing import List
from src.entities import Vacancy


class Connector(ABC):
    """
    Абстрактный базовый класс для соединителей.
    Определяет интерфейс для работы с вакансиями.
    """

    @abstractmethod
    def get_vacancies(self) -> List[Vacancy]:
        """
        Получить список вакансий.

        Returns:
            List[Vacancy]: Список вакансий.
        """
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавить вакансию.

        Args:
            vacancy (Vacancy): Вакансия для добавления.
        """
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удалить вакансию.

        Args:
            vacancy (Vacancy): Вакансия для удаления.
        """
        pass

    @staticmethod
    def _parse_vacancy_to_dict(vacancy: Vacancy) -> dict:
        """
        Преобразовать объект Vacancy в словарь.

        Args:
            vacancy (Vacancy): Объект Vacancy.

        Returns:
            dict: Словарь с данными вакансии.
        """
        return asdict(vacancy)

    @staticmethod
    def _parse_dict_to_vacancy(raw_data: dict) -> Vacancy:
        """
        Преобразовать словарь в объект Vacancy.

        Args:
            raw_data (dict): Словарь с данными вакансии.

        Returns:
            Vacancy: Объект Vacancy.
        """
        return Vacancy(**raw_data)


class JsonConnector(Connector):
    """
    Класс для работы с вакансиями, сохраняемыми в JSON файл.
    """

    def __init__(self, file_path: Path, encoding: str = 'utf-8') -> None:
        """
        Инициализация JsonConnector.

        Args:
            file_path (Path): Путь к файлу JSON.
            encoding (str): Кодировка файла. По умолчанию 'utf-8'.
        """
        self.file_path = file_path
        self.encoding = encoding

    def get_vacancies(self) -> List[Vacancy]:
        """
        Получить список вакансий из JSON файла.

        Returns:
            List[Vacancy]: Список вакансий.
        """
        if not self.file_path.exists():
            return []

        vacancies = []
        with self.file_path.open(encoding=self.encoding) as f:
            for item in json.load(f):
                vacancy = self._parse_dict_to_vacancy(item)
                vacancies.append(vacancy)
        return vacancies

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавить вакансию в JSON файл.

        Args:
            vacancy (Vacancy): Вакансия для добавления.
        """
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            self._save_vacancies(vacancies)

    def remove_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удалить вакансию из JSON файла.

        Args:
            vacancy (Vacancy): Вакансия для удаления.
        """
        vacancies = self.get_vacancies()
        if vacancy in vacancies:
            vacancies.remove(vacancy)
            self._save_vacancies(vacancies)

    def _save_vacancies(self, vacancies: List[Vacancy]) -> None:
        """
        Сохранить список вакансий в JSON файл.

        Args:
            vacancies (List[Vacancy]): Список вакансий для сохранения.
        """
        raw_data = [self._parse_vacancy_to_dict(vac) for vac in vacancies]
        with self.file_path.open(mode='w', encoding=self.encoding) as file:
            json.dump(raw_data, file, indent=2, ensure_ascii=False)
