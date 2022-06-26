### API Yamdb
REST API для проекта Yamdb на Django. Позволяет выполнять CRUD API запросы.

### Установка. Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/gevolx/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов к API:

Для регистрации пользователя и получения токена необходимо сделать запрос с json телом  
```
{
    "email": "string",
    "username": "string"
}
```  
на эндпоинт:
```
http://127.0.0.1:8000/api/v1/auth/signup/
```
После этого в папке sent_emails будет создано письмо с кодом подтверждения, который нужно отправить в формате 
```
{
    "username": "string",
    "confirmation_code": "string"
}
```
на эндпоинт:
```
http://127.0.0.1:8000/api/v1/auth/token/
```

Получение списка всех произведений
```
GET http://127.0.0.1:8000/api/v1/titles/
```
Добавление нового отзыва к произведению.
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Полный перечень запросов к API можно получить по эндпоинту /redoc
```
http://127.0.0.1:8000/redoc
```