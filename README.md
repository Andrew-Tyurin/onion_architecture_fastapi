# Onion Architecture | Луковая архитектура
## Образец паттерн/шаблон использования архитектуры на FastApi

### В проекте python 3.13

### REST-API реализовано: create(POST), read(GET), delete(DELETE); В проекте простые ручки, есть фильтрация по Book, агрегация по Author. А так-же, авторизация на стороне нашего приложения используя аутентификацию oauth-google.

### запуск проекта:
- Скачиваем проект, заходим в корневую директорию проекта.
- Создать свой файл со своей базой .env в котором DATABASE_URL=sqlite+aiosqlite:///fastapi.db или для postgres  
  DATABASE_URL=postgresql+asyncpg://fastapi:1234@localhost:5432/fastapi_db именно асинхронная, обычный  
  sqlite, postgres не подойдёт, нужен драйвер для sqlite: aiosqlite, postgres: asyncpg. и Указать имя СУБД:
  - NAME_DBMS=sqlite
  - NAME_DBMS=postgresql
- Так-же в .env файл обязательно должны быть данные для google oauth: CLIENT_ID, CLIENT_SECRET для этого нужно  
  создать клиента <https://console.cloud.google.com/auth/clients>, а для генерации jwt нужен SECRET_KEY  
  сгенерировать SECRET_KEY:  
  ```bash
  openssl rand -base64 48 | tr '+/' '-_' | tr -d '='
  ```
  ADMIN_PASSWORD - по которому добавляется возможность удалять пользователей. Итого .env выглядеть должен примерно так: 
  ```env
  # Образец .env:
  NAME_DBMS=sqlite
  DATABASE_URL=sqlite+aiosqlite:///fastapi.db
  SECRET_KEY=1234qwer...
  ADMIN_PASSWORD=1234
  GOOGLE_CLIENT_ID=настроенный OAuth клиент в console.cloud.google.com
  GOOGLE_CLIENT_SECRET=настроенный OAuth клиент в console.cloud.google.com
  ```

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
  создастся тестовая база которая проверит каждый endpoint связанный domain моделями: Book, Author.  
  Тестовая база по умолчанию использует sqlite, но можно так-же использовать postgres указав В .test.env  
  аналогично .env, а именно NAME_DBMS и DATABASE_URL.
  ```bash
  pytest -vs
  ```
- Создать таблицы в бд и заполнить moc данными(можно не заполнять данными, но создать таблицы обязательно  
  запуск из корня проекта:
  ```bash
  python create_tables.py
  ```
- Запустить проект(из корневой директории проекта):  
  ```bash
  python main.py
  ```
- В браузере: http://localhost:8000/docs и тыкам на endpoints ))
