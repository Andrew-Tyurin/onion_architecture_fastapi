# Onion Architecture | Луковая архитектура
## Образец паттерн/шаблон использования архитектуры на FastApi

### В проекте python 3.13

### REST-API реализовано: create(POST), read(GET), delete(DELETE); В проекте простые ручки, 3 бизнес модели User Book Author, но есть фильтрация по Book, агрегация по Author итд.

### запуск проекта:
- Создать свой файл со своей базой .env в котором DATABASE_URL="sqlite+aiosqlite:///sqlite.db"   
  так-же в .env файл обязательно должны быть данные для google oauth CLIENT_ID, CLIENT_SECRET   
  для этого нужно создать клиента <https://console.cloud.google.com/auth/clients>  
  база 'асинхронная' обычный sqlite, postgres не подойдёт, нужен драйвер для  
  sqlite: aiosqlite, postgres: asyncpg
- Скачиваем проект удобным вам способом: архивом, git clone ...; Заходим в корневую папку проекта:
  ```bash
  python3 -m venv .venv
  ```
- ```bash
  source .venv/bin/activate
  ```
- ```bash
  pip install -r requirements.txt
  ```
- Перед созданием таблиц с которыми взаимодействуют endpoints, можно запустить из корня проекта pytest  
  создастся тестовая база, и проверит каждый endpoint связанный domain моделями: Book, Author
  ```bash
  pytest -vs
  ```
- Создать таблицы в бд и заполнить moc данными(можно не заполнять данными, но создать таблицы обязательно)  
  запуск из корня проекта:
  ```bash
  python create_tables.py
  ```
- Запустить проект(из корневой директории проекта):  
  ```bash
  python main.py
  ```
- В браузере: http://localhost:8000/docs и тыкам на endpoints ))
