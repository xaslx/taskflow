## 
Веб-приложение для управления командой внутри компании.
Имеется аутентификация, авторизация, роли

## Функционал
Регистрация/Вход/Выход

Пользователь: Может обновлять свой профиль, Присоедениться к команде по коду, Удалить профиль, Оставлять комментарии в задаче

Админ: Может создать команду, Удалить пользователя, Добавить пользователей в команду, Просматривать команды или команду Изменять роли

Менеджер: Может Создавать встречи, задачи, Получить список всех задач и задачи, Удаление задачи, Обновление задачи, назначить задачу на пользователя при обновлении, Оставлять комментарии в задаче


## Структура проекта

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