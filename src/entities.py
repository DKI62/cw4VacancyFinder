from dataclasses import dataclass


@dataclass
class Vacancy:
    """
    Класс для представления вакансии.

    Атрибуты:
        name (str): Название вакансии.
        url (str): Ссылка на вакансию.
        salary_currency (str): Валюта зарплаты. По умолчанию 'RUR'.
        salary_from (int | None): Нижняя граница зарплаты. По умолчанию None.
        salary_to (int | None): Верхняя граница зарплаты. По умолчанию None.
    """
    name: str
    url: str
    salary_currency: str = 'RUR'
    salary_from: int | None = None
    salary_to: int | None = None

    def __post_init__(self):
        """
        Вызывается после инициализации объекта.
        Проверяет корректность значений зарплаты.
        """
        self._validate_salary(self.salary_from)
        self._validate_salary(self.salary_to)

    @staticmethod
    def _validate_salary(salary: int | None) -> None:
        """
        Проверяет, что значение зарплаты не является отрицательным.

        Args:
            salary (int | None): Значение зарплаты.

        Raises:
            ValueError: Если значение зарплаты отрицательное.
        """
        if salary is not None and salary < 0:
            raise ValueError("Salary cannot be negative")

    def __lt__(self, other: 'Vacancy') -> bool:
        """
        Сравнивает вакансии по зарплате.

        Args:
            other (Vacancy): Другая вакансия для сравнения.

        Returns:
            bool: True, если текущая вакансия имеет меньшую зарплату, чем другая вакансия, иначе False.
        """
        if self.salary_from and other.salary_from:
            return self.salary_from < other.salary_from

        if self.salary_to and other.salary_to:
            return self.salary_to < other.salary_to

        self_salary = self.salary_from or self.salary_to
        other_salary = other.salary_from or other.salary_to
        return self_salary < other_salary

    def __eq__(self, other: 'Vacancy') -> bool:
        """
        Проверяет равенство двух вакансий по зарплате.

        Args:
            other (Vacancy): Другая вакансия для сравнения.

        Returns:
            bool: True, если зарплаты равны, иначе False.
        """
        eq_from = self.salary_from == other.salary_from
        eq_to = self.salary_to == other.salary_to
        return eq_from == eq_to
