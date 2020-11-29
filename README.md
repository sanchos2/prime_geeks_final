# NOVA HR 1.0

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

### Описание

Цифровой ассистент сотрудника по подбору персонала:

[Демо версия проекта](http://hr.nautilus.com.ru/) 

### Установка

Устанавливаем python3

```sh
sudo apt install python3
sudo apt install python3-pip
```

Клонируем проект, устанавливаем зависимости

```sh
git clone https://github.com/sanchos2/prime_geeks_final.git
cd prime_geeks_final
pip3 install -r requirements.txt
```

Создаем виртуальное окружение

```sh
python3 -m venv venv
```
Для разработки переменные окружения можно не указывать - при этом будут использованы default значения
Для production среды добавляем переменные окружения в .env файл и размещаем его в корне проекта

```
DEBUG=True
SECRET_KEY=superkey
ALLOWED_HOSTS=127.0.0.1 localhost [::1]
DB_ENGINE=django.db.backends.postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=base
DB_USER=user
DB_PASSWORD=pa$$word

```
Для работы в production среде Debug установить в False 

### Запуск

Запуск проекта
Активируем виртуальное окружение и запускаем сервер для разработки

```sh
source venv/bin/activate
python3 manage.py runserver
```

Переходим по адресу http://127.0.0.1:8000
Панель администратора доступна по адресу http://127.0.0.1:8000/admin

-=Prime Geeks=-
