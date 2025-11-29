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
/api/auth/register - Регистрация пользователей
/api/auth/login - Вход
/api/authlogout - Выход
/api/auth/refresh-token - Обновить access токен

/api/users - Удаление своего профиля
/api/users - Обновление своего профиля
/api/users/admin/{user_id} - Удалить пользователя (Доступно только админу)

/api/teams - Создание команды (Доступно только админу)
/api/teams - Получить список команд (Доступно только админу)
/api/teams/join - Присоедениться к команде, по коду
/api/teams/{team_id}/members - Получение информации о конкретной команде и ее участников (Доступно только админу)
/api/teams/{team_id}/members - Добавление пользователя в команду (Доступно только админу)
/api/teams/{team_id}/members/{user_id} - Удаление пользователя из команды (Доступно только админу)
/api/teams/{team_id}/members/{user_id} - Изменение роли у пользователя (Доступно только админу)

/api/tasks - Получение списка задач в команде, где состоит менеджер (Доступно только менеджеру)
/api/tasks - Создание задачи руководителем (Доступно только менеджеру)
/api/tasks/{task_id} - Получение задачи по ID (Доступно только менеджеру)
/api/tasks/{task_id} - Удаление задачи по ID (Доступно только менеджеру)
/api/tasks/{task_id} - Изменение задачи (Доступно только менеджеру)
/api/tasks/{task_id}/comments - Добавление комментария к задаче

/api/evaluations - Получение всех своих оценок 
/api/evaluations - Выставление оценки за выполненную задачу (Доступно только менеджеру)

/api/meetings - Получение всех своих встреч
/api/meetings - Создание встречи (Доступно только менеджеру)
/api/meetings/{meeting_id} - Удаление встречи (Доступно только менеджеру)

/ - Минимальный фронтенд
