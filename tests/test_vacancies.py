import pytest
from src.entities import Vacancy
from src.connector import JsonConnector
from src.user_interaction import filter_vacancies_by_keyword, filter_vacancies_by_salary
from pathlib import Path
import json


# Тесты для класса Vacancy

@pytest.mark.parametrize('field_name', ['salary_from', 'salary_to'])
def test_vacancy_salary_failed_be_negative(field_name):
    with pytest.raises(ValueError, match='Salary cannot be negative'):
        Vacancy('name', 'url', **{field_name: -1})


def test_vacancy_compare_by_salary_from():
    vac1 = Vacancy('name', 'url', salary_from=10)
    vac2 = Vacancy('name', 'url', salary_from=20)
    vac3 = Vacancy('name', 'url', salary_from=20)
    assert vac1 < vac2
    assert vac2 == vac3
    assert vac3 > vac1


def test_vacancy_compare_by_salary_to():
    vac1 = Vacancy('name', 'url', salary_to=10)
    vac2 = Vacancy('name', 'url', salary_to=20)
    vac3 = Vacancy('name', 'url', salary_to=20)
    assert vac1 < vac2
    assert vac2 == vac3
    assert vac3 > vac1


def test_vacancy_compare_by_different_salary():
    vac1 = Vacancy('name', 'url', salary_to=10)
    vac2 = Vacancy('name', 'url', salary_from=20)
    assert vac1 < vac2


def test_equal_vacancies():
    vac2 = Vacancy('name_1', 'url', salary_from=20)
    vac3 = Vacancy('name_2', 'url', salary_from=20)
    assert vac2 == vac3


# Тесты для фильтрации и сортировки

def test_filter_vacancies_by_keyword():
    vacancies = [
        Vacancy('Python Developer', 'url1'),
        Vacancy('Java Developer', 'url2'),
        Vacancy('Python Engineer', 'url3')
    ]
    result = filter_vacancies_by_keyword(vacancies, 'Python')
    assert len(result) == 2
    assert result[0].name == 'Python Developer'
    assert result[1].name == 'Python Engineer'


@pytest.fixture
def json_connector(tmp_path):
    file_path = tmp_path / "vacancies.json"
    return JsonConnector(file_path)


def test_add_vacancy(json_connector):
    vacancy = Vacancy('Python Developer', 'url1', salary_from=1000, salary_to=2000)
    json_connector.add_vacancy(vacancy)
    vacancies = json_connector.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0] == vacancy


def test_remove_vacancy(json_connector):
    vacancy = Vacancy('Python Developer', 'url1', salary_from=1000, salary_to=2000)
    json_connector.add_vacancy(vacancy)
    json_connector.remove_vacancy(vacancy)
    vacancies = json_connector.get_vacancies()
    assert len(vacancies) == 0
