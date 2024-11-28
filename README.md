## Database Syncer

Скрипт для синхронизации баз данных между собой.

Для удобства проверки работы кода всё завернуто в docker-compose и разворачивается одной командой.

Есть БД source_db - образец, данные которой копируются в БД tagret_db.

Данные, которые лежат в target_db остаются не тронутыми и добавляется всё, что есть в source_db

### Запуск

```shell
docker-compose up --build
```

Необходимо будет дождаться создания двух БД и таблиц внутри них.

Затем запустится контейнер python_sync и сообщит о своем завершении.

Для удобства добавлен adminer, чтобы визуально посмотреть на структуры БД, не залезая в контейнеры.

#### Просмотр структуры БД в adminer

Перейти в adminer:

```shell
http://localhost:8080/
```

Доступ в БД target_db:

* System: MySQL
* Server: mysql-target
* Username: target_user
* Password: password
* Database: target_db

Доступ в БД source_db:

* System: MySQL
* Server: mysql-source
* Username: source_user
* Password: password
* Database: source_db
