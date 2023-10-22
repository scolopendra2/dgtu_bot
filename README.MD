# Бейджи статус пайплайна CI/CD
[![pipeline Status](https://github.com/scolopendra2/dgtu_bot/actions/workflows/main.yml/badge.svg)](https://github.com/scolopendra2/dgtu_bot/actions/workflows/main.yml)

# Python/JS version
[![Python Version](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/downloads/release/python-3100/) ![JavaScript version](https://img.shields.io/badge/javascript-%3E%3D%20ES6-brightgreen)

![Language stats](https://img.shields.io/badge/language_stats-javascript:0%25%20python:100%25%20html:0%25-brightgreen)


# ER диаграмма БД:
![ER](ER.png)

# Клонирование репозитория
git clone https://github.com/scolopendra2/dgtu_bot

# Установка и запуск виртуального окружения
python -m venv venv

venv/Scripts/activate

# Установка зависимостей
pip install -r requirements/prod.txt

# Подстановка секретных переменных в окружение
BOT_TOKEN - токен вашего бота
POSTGRES_DB - название базы данных
POSTGRES_USER - имя пользователя
POSTGRES_PASSWORD - пароль
POSTGRES_HOST - хост

# Запуск бота
python app.py