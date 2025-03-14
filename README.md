# Тестовое Farpost (SQLite, FastApi)
## Установка зависимостей
Желательно создать отдельный env (при разработке был использован venv). Далее использовать команду:
```bash
pip install -r requirements.txt
```
## Клон репозитория
```bash
git clone https://github.com/beautiful-white/python_dev_solovev_roman.git
```
ИЛИ
```bash
git clone git@github.com:beautiful-white/python_dev_solovev_roman.git
```
## Генерация баз данных
### _Этот этап можно пропустить, если нет желания чего-то трогать, примеры баз данных уже сгенерированы в репозитории._
Для генерации достаточно запустить файл **_creating_databases.ipynb_**, после чего скомпилировать каждый пункт (баз данных не должно быть в директории, иначе выдаст ошибку).

## Запуск API
```bash
uvicorn api:app --reload
```
После успешного запуска сервер будет доступен по адресу:
```
http://127.0.0.1:8000
```
Пример подключения:
```
http://127.0.0.1:8000/api/comments?user_login=940431dd563183b9
```
Так как данный логин есть в БД, результат будет таким:
![image](https://github.com/user-attachments/assets/c2799cf6-a12c-417d-b247-c2ec66fc632d)
