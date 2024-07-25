import pytest
from src.entities import Vacancy

def test_vacancy_initialization():
    vacancy = Vacancy(name="Developer", url="http://example.com")
    assert vacancy.name == "Developer"
    assert vacancy.url == "http://example.com"
    assert vacancy.salary_currency == "RUR"
    assert vacancy.salary_from is None
    assert vacancy.salary_to is None

def test_vacancy_salary_validation():
    with pytest.raises(ValueError, match="Salary cannot be negative"):
        Vacancy(name="Developer", url="http://example.com", salary_from=-100)

def test_vacancy_comparison():
    vac1 = Vacancy(name="Dev", url="http://example.com", salary_from=1000)
    vac2 = Vacancy(name="Dev", url="http://example.com", salary_from=2000)
    assert vac1 < vac2
    assert vac2 > vac1
    assert vac1 != vac2

def test_vacancy_equality():
    vac1 = Vacancy(name="Dev", url="http://example.com", salary_from=1000, salary_to=2000)
    vac2 = Vacancy(name="Dev", url="http://example.com", salary_from=1000, salary_to=2000)
    assert vac1 == vac2
