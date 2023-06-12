## Описание
### Тестовое задание от компании Центр Финансовых Технологий (ЦФТ):
Был реализован сервис, позволяющий создавать юзера и предоставлять доступ к ресурсам по JWT-токену, сохраненному в cookies.

Для реализации проекта были использованы следующие технологии: FastAPI, FastAPI Users(db-alchemy), SQLAlchemy, Docker, PostgreSQL (полный список в pyproject.toml).

## Инструкция по запуску
Для начала нужно клонировать данный репозиторий

```
git clone https://github.com/FancyDogge/testovoe_bewise2.git
```

Далее для запуска перейдите в директорию с docker-compose.yml и введите сдледующую команду для 

```
docker-compose up --build
```

Начнется сборка образов и установка зависимостей, после чего приложение и бд должны запуститься.
Миграции запустятся автоматически.

Все готово!
Теперь приложение запущено и можно опробовать API по адресу localhost:8000/docs
