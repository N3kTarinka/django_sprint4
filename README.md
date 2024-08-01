[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=2A85F7&width=435&lines=%23+Blogicum)](https://git.io/typing-svg)

# Как локально развернуть и посмотреть проект?
1. Склонировать репозиторий.

2. Создать виртуальное окружение:
```python
python -m venv venv
```
3. Активировать виртуальное окружение
```python
source venv/Scripts/activate
```
4. Установить зависимости из файла requirements.txt:
```python
pip install -r requirements.txt
```
5. Применить миграции:
```python
python manage.py migrate
```
6. Загрузить фикстуры в БД
```python
python manage.py loaddata ../db.json
```
7. Создание суперпользователя:
```python
python manage.py createsuperuser
```
8. Запускаем проект и смотрим :)
```python
python manage.py runserver
```

# Автор проекта: Никита Ж.