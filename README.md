# Vacancy Finder

## О проекте

Vacancy Finder - это приложение для поиска вакансий с использованием API HeadHunter и сохранения результатов в JSON
файл. Приложение предоставляет интерфейс для взаимодействия с пользователем через консоль, позволяя искать, фильтровать,
сортировать и удалять вакансии.

## Структура проекта

- `src/api.py` - Модуль для работы с API HeadHunter.
- `src/entities.py` - Модуль, содержащий описание класса `Vacancy`.
- `src/connector.py` - Модуль для работы с JSON файлом, содержащим вакансии.
- `src/user_interaction.py` - Модуль для взаимодействия с пользователем через консоль.
- `src/config.py` - Модуль для конфигурации путей в проекте.
- `main.py` - Главный файл для запуска приложения.

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone 
2. Установите Poetry, если он ещё не установлен

3. Установите необходимые зависимости:
   poetry install
4. Активируйте виртуальное окружение Poetry
   poetry shell

## Использование

1. Запустите приложение:
   python main.py

2. Следуйте инструкциям в консоли:
   Введите текст для поиска вакансий.
   Выберите действие из списка доступных команд.

## Примеры команд

Получить топ вакансий.
Удалить вакансию.
Фильтровать вакансии по ключевым словам.
Сортировать вакансии.
Просмотр деталей вакансии.
Выйти из приложения.

## Конфигурация

Путь к файлу с вакансиями и другие параметры могут быть настроены в модуле src/config.py.

## Требования

Python 3.7 и выше

## Лицензия

# Этот проект лицензирован под лицензией "MIT". #