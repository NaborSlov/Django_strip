## API для платежной системы Strip

### Перед началом работы:

#### Настройка переменных окружения:

Для работы проекта необходимо создать **.env** в корневой папке.
В нем нужно указать необходимые значения переменных:

* API_KEY_STRIP = **токен strip**

#### Установка зависимостей:

В корневой папке находиться файл с зависимостями requirements.txt

```shell
pip install -r requirements.txt
```

* Запуск проекта

```shell
python ./manage.py runserver
```

#### Docker

* Запуск докера

```shell
docker compose up --build -d
```