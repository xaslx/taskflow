## 
Веб-приложение для управления командой внутри компании.
Имеется аутентификация, авторизация, роли

## Функционал
Регистрация/Вход/Выход

Пользователь: Может обновлять свой профиль, Присоедениться к команде по коду, Удалить профиль, Оставлять комментарии в задаче

Админ: Может создать команду, Удалить пользователя, Добавить пользователей в команду, Просматривать команды или команду Изменять роли

Менеджер: Может Создавать встречи, задачи, Получить список всех задач и задачи, Удаление задачи, Обновление задачи, назначить задачу на пользователя при обновлении, Оставлять комментарии в задаче


## Структура проекта
```
.
├── .
├── ├── alembic.ini
├── ├── docker-compose.yaml
├── ├── Dockerfile
├── ├── .dockerignore
├── ├── .env
├── ├── .env.example
├── ├── .gitignore
├── ├── Makefile
├── ├── migrations
├── │   ├── env.py
├── │   ├── README
├── │   ├── script.py.mako
├── │   └── versions
├── │       ├── 2be207b43936_.py
├── │       └── f4f3fbbaf4d2_.py
├── ├── poetry.lock
├── ├── pyproject.toml
├── ├── .pytest_cache
├── │   ├── CACHEDIR.TAG
├── │   ├── .gitignore
├── │   ├── README.md
├── │   └── v
├── │       └── cache
├── │           ├── lastfailed
├── │           └── nodeids
├── ├── pytest.ini
├── ├── README.md
├── ├── src
├── │   ├── config.py
├── │   ├── database
├── │   │   ├── __init__.py
├── │   │   └── postgres.py
├── │   ├── exceptions
├── │   │   ├── base.py
├── │   │   ├── evaluation.py
├── │   │   ├── __init__.py
├── │   │   ├── jwt.py
├── │   │   ├── meeting.py
├── │   │   ├── task.py
├── │   │   ├── team.py
├── │   │   └── user.py
├── │   ├── ioc.py
├── │   ├── main.py
├── │   ├── models
├── │   │   ├── admin.py
├── │   │   ├── base.py
├── │   │   ├── evaluation.py
├── │   │   ├── __init__.py
├── │   │   ├── meeting.py
├── │   │   ├── task.py
├── │   │   ├── team.py
├── │   │   └── user.py
├── │   ├── repositories
├── │   │   ├── evaluation.py
├── │   │   ├── __init__.py
├── │   │   ├── meeting.py
├── │   │   ├── task.py
├── │   │   ├── team.py
├── │   │   └── user.py
├── │   ├── routers
├── │   │   ├── auth.py
├── │   │   ├── evaluations.py
├── │   │   ├── __init__.py
├── │   │   ├── main_page.py
├── │   │   ├── meeting.py
├── │   │   ├── tasks.py
├── │   │   ├── teams.py
├── │   │   └── users.py
├── │   ├── schemas
├── │   │   ├── evaluation.py
├── │   │   ├── __init__.py
├── │   │   ├── meeting.py
├── │   │   ├── pagination.py
├── │   │   ├── response.py
├── │   │   ├── task.py
├── │   │   ├── team.py
├── │   │   ├── token.py
├── │   │   └── user.py
├── │   ├── services
├── │   │   ├── auth.py
├── │   │   ├── hash.py
├── │   │   ├── __init__.py
├── │   │   └── jwt.py
├── │   ├── static
├── │   │   └── templates
├── │   │       └── index.html
├── │   └── use_cases
├── │       ├── admin
├── │       │   ├── create_team.py
├── │       │   ├── delete_user.py
├── │       │   ├── get_all_teams.py
├── │       │   ├── get_team_info.py
├── │       │   ├── __init__.py
├── │       │   └── team_manager.py
├── │       ├── __init__.py
├── │       ├── manager
├── │       │   ├── create_evaluation.py
├── │       │   ├── create_meeting.py
├── │       │   ├── create_task.py
├── │       │   ├── delete_meeting.py
├── │       │   ├── delete_task_by_id.py
├── │       │   ├── get_all_tasks.py
├── │       │   ├── get_by_task_by_id.py
├── │       │   ├── __init__.py
├── │       │   └── update_task.py
├── │       └── user
├── │           ├── add_task_comment.py
├── │           ├── delete.py
├── │           ├── get_all_evaluations.py
├── │           ├── get_user_meetings.py
├── │           ├── __init__.py
├── │           ├── join_team.py
├── │           ├── login.py
├── │           ├── refresh_token.py
├── │           ├── register.py
├── │           └── update_user.py
└── └── tests/
    ├── ├── conftest.py
    └── └── user_tests/
        └── └── test_use_cases.py
```

## API
## Аутентификация

| Метод | Маршрут | Описание |
|-------|---------|----------|
| POST  | `/api/auth/register` | Регистрация пользователя |
| POST  | `/api/auth/login`    | Вход пользователя |
| POST  | `/api/auth/logout`   | Выход пользователя |
| POST  | `/api/auth/refresh-token` | Обновление access токена |

---

## Пользователи

| Метод | Маршрут | Описание | Доступ |
|-------|---------|----------|--------|
| DELETE | `/api/users` | Удаление своего профиля | Пользователь |
| PUT    | `/api/users` | Обновление своего профиля | Пользователь |
| DELETE | `/api/users/admin/{user_id}` | Удаление пользователя | Администратор |

---

## Команды

| Метод | Маршрут | Описание | Доступ |
|-------|---------|----------|--------|
| POST   | `/api/teams` | Создание команды | Администратор |
| GET    | `/api/teams` | Получение списка команд | Администратор |
| POST   | `/api/teams/join` | Присоединиться к команде по коду | Пользователь |
| GET    | `/api/teams/{team_id}/members` | Получение информации о команде и ее участниках | Администратор |
| POST   | `/api/teams/{team_id}/members` | Добавление пользователя в команду | Администратор |
| POST   | `/api/teams/{team_id}/members/{user_id}` | Удаление пользователя из команды | Администратор |
| PATCH  | `/api/teams/{team_id}/members/{user_id}` | Изменение роли пользователя | Администратор |

---

## Задачи

| Метод | Маршрут | Описание | Доступ |
|-------|---------|----------|--------|
| GET    | `/api/tasks` | Получение списка задач команды, где состоит менеджер | Менеджер |
| POST   | `/api/tasks` | Создание задачи | Менеджер |
| GET    | `/api/tasks/{task_id}` | Получение задачи по ID | Менеджер |
| DELETE | `/api/tasks/{task_id}` | Удаление задачи | Менеджер |
| PATCH  | `/api/tasks/{task_id}` | Изменение задачи | Менеджер |
| POST   | `/api/tasks/{task_id}/comments` | Добавление комментария к задаче | Пользователь |

---

## Оценки

| Метод | Маршрут | Описание | Доступ |
|-------|---------|----------|--------|
| GET   | `/api/evaluations` | Получение всех своих оценок | Пользователь |
| POST  | `/api/evaluations` | Выставление оценки за выполненную задачу | Менеджер |

---

## Встречи

| Метод | Маршрут | Описание | Доступ |
|-------|---------|----------|--------|
| GET    | `/api/meetings` | Получение всех своих встреч | Пользователь |
| POST   | `/api/meetings` | Создание встречи | Менеджер |
| DELETE | `/api/meetings/{meeting_id}` | Удаление встречи | Менеджер |


Есть админка sqladmin по адресу **127.0.0.1:8000/admin**

Имеется минимальный фронтенд по адресу **'/'**.

Регистрация, Вход, Выход, Обновление профиля, Удаление профиля, Присоеденение к команде по коду.

Для админа - Создание команды, Удаление поьзователя по ID, Просмотр команд. (Можно поставить себе роль admin в админке, чтобы этот блок появился)


## Использованные инструменты
- FastAPI
- alembic
- jinja2
- dishka
- pytest
- sqladmin
- sqlalchemy
- postgresql
- black
- jwt


## Запуск
- make build
- make up
- make down
- make logs
