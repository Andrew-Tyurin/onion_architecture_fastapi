# Onion Architecture | Луковая архитектура
## Образец паттерн/шаблон использования архитектуры на FastApi

### В проекте python 3.13

### REST-API реализовано: create(POST), read(GET), delete(DELETE); В проекте простые ручки, 3 бизнес модели User Book Author, но есть фильтрация по Book, агрегация по Author. А так-же, авторизация на стороне нашего приложения используя аутентификацию oauth-google.

### запуск проекта:
- Создать свой файл со своей базой .env в котором DATABASE_URL="sqlite+aiosqlite:///sqlite.db"  
  именно асинхронная обычный sqlite, postgres не подойдёт, нужен драйвер для sqlite:  
  aiosqlite, postgres: asyncpg.
- Так-же в .env файл обязательно должны быть данные для google oauth: CLIENT_ID, CLIENT_SECRET   
  для этого нужно создать клиента <https://console.cloud.google.com/auth/clients>, а для генерации  
  jwt нужен SECRET_KEY, итого примерно выглядеть должно так .env:
  - DATABASE_URL=sqlite+...
  - SECRET_KEY=1234qwer...
  - GOOGLE_CLIENT_ID=настроенный OAuth клиент в console.cloud.google.com
  - GOOGLE_CLIENT_SECRET=настроенный OAuth клиент в console.cloud.google.com
- Скачиваем проект удобным вам способом. Заходим в корневую папку проекта:
- ```bash
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
