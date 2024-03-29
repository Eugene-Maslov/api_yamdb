# api_yamdb
### Описание проекта:
Проект представляет собой API для социальной сети оценок фильмов, книг и музыкальных произведений.

### Технологии:
Python 3.9  
Django 3.2

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Eugene-Maslov/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

```
cd api_yamdb
```

Выполнить миграции:

```
python manage.py migrate
```

Открыть командную строку и перейти в директорию api_yamdb:

```
cd api_yamdb
```

Импортировать данные из файлов *.csv в базу данных проекта:

```
sqlite3.exe db.sqlite3 < data_import
```

Вернуться в bash и запустить проект:

```
python manage.py runserver
```

### Документация по эндпоинтам, запросам и ответам:

http://127.0.0.1:8000/redoc/

### Авторы:
_Никитенко Николай_: первый разработчик  
_Маслов Евгений_: второй разработчик, тимлид  
_Андрющенко Стас_: третий разработчик