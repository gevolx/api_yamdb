### API Yamdb
REST API ��� ������� Yamdb. ��������� ��������� CRUD API �������.

### ���������. ��� ��������� ������:

����������� ����������� � ������� � ���� � ��������� ������:

```
git clone https://github.com/gevolx/api_yamdb.git
```

```
cd api_yamdb
```

C������ � ������������ ����������� ���������:

```
python3 -m venv env
```

```
source env/bin/activate
```

���������� ����������� �� ����� requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

��������� ��������:

```
python3 manage.py migrate
```

��������� ������:

```
python3 manage.py runserver
```

### ������� �������� � API:

��� ����������� ������������ � ��������� ������ ���������� ������� ������ � json �����  
```
{
    "email": "string",
    "username": "string"
}
```  
�� ��������:
```
http://127.0.0.1:8000/api/v1/auth/signup/
```
����� ����� � ����� sent_emails ����� ������� ������ � ����� �������������, ������� ����� ��������� � ������� 
```
{
    "username": "string",
    "confirmation_code": "string"
}
```
�� ��������:
```
http://127.0.0.1:8000/api/v1/auth/token/
```

��������� ������ ���� ������������
```
GET http://127.0.0.1:8000/api/v1/titles/
```
���������� ������ ������ � ������������.
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

������ �������� �������� � API ����� �������� �� ��������� /redoc
```
http://127.0.0.1:8000/redoc
```

### ������������ ����������
```
Python 3.10, Django 2.2 (django rest framework + simplejwt)
```

### ������
[gevolx](https://github.com/gevolx)
[NiroTime](https://github.com/NiroTime)
[alexkopss](https://github.com/alexkopss)