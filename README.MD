# Novator

Django-приложение для учета клиентов, групп, абонементов, расписания и посещаемости.

## Что умеет проект

- вести список клиентов, групп, тренеров и залов;
- создавать и редактировать абонементы;
- отмечать посещения через кнопку `Посетил` и отменять отметку;
- искать клиента по номеру карты на главной странице;
- смотреть карточку клиента с абонементами и историей посещений;
- управлять расписанием занятий;
- формировать документы по клиентам и группам через `docxtpl`;
- показывать отчеты по чеку и сумме абонементов у тренера;
- собирать статистику активности пользователей.

## Технологии

- Python 3.11
- Django 4.2
- SQLite
- Bootstrap 5
- `django-crispy-forms`
- `crispy-bootstrap5`
- `docxtpl`
- `djangorestframework`

## Структура проекта

- `nov/manage.py` - точка входа Django
- `nov/nov/settings.py` - настройки проекта
- `nov/nov/urls.py` - корневые маршруты
- `nov/myapp/` - основное приложение
- `nov/myapp/views.py` - логика страниц и действий
- `nov/myapp/models.py` - модели данных
- `nov/myapp/forms.py` - формы
- `nov/myapp/templates/` - шаблоны страниц
- `nov/myapp/static/` - CSS, JS и изображения
- `nov/db.sqlite3` - база данных SQLite

## Требования

- Python 3.11 или выше
- `pip`
- виртуальное окружение

## Быстрый старт

### 1. Создать и активировать виртуальное окружение

Из корня проекта:

```bash
python -m venv .venv
```

Активировать:

```bash
source .venv/bin/activate
```

На Windows см. отдельный раздел ниже.

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Применить миграции

Перейдите в папку `nov`, где лежит `manage.py`:

```bash
cd nov
python manage.py migrate
```

### 4. Создать суперпользователя

Если нужен вход в админку:

```bash
python manage.py createsuperuser
```

### 5. Запустить сервер

```bash
python manage.py runserver 127.0.0.1:8000
```

После этого приложение будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

## Как запускать на Windows

Ниже описан вариант через PowerShell. Он самый удобный для этого проекта.

### Вариант 1. PowerShell

1. Откройте PowerShell в корне проекта.
2. Создайте виртуальное окружение:

```powershell
py -3.11 -m venv .venv
```

3. Если PowerShell блокирует запуск скриптов, один раз выполните:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

4. Активируйте окружение:

```powershell
.\.venv\Scripts\Activate.ps1
```

5. Установите зависимости:

```powershell
pip install -r requirements.txt
```

6. Перейдите в папку проекта Django:

```powershell
cd nov
```

7. Примените миграции:

```powershell
python manage.py migrate
```

8. При необходимости создайте администратора:

```powershell
python manage.py createsuperuser
```

9. Запустите сервер:

```powershell
python manage.py runserver 127.0.0.1:8000
```

10. Откройте в браузере:

```text
http://127.0.0.1:8000/
```

### Вариант 2. CMD

Если удобнее обычный `cmd.exe`:

```bat
py -3.11 -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
cd nov
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

## Перенос на Windows

Если переносишь проект на Windows, делай так:

1. Скопируй всю папку проекта на новый компьютер.
2. Убедись, что в корне проекта есть `requirements.txt`, `nov/` и `backups/`.
3. Создай виртуальное окружение заново:

```powershell
py -3.11 -m venv .venv
```

4. Активируй окружение и поставь зависимости:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

5. Если у тебя уже есть более новая база, просто замени файл:

```text
nov/db.sqlite3
```

6. Если схема базы совпадает с кодом, обычно достаточно:

```powershell
cd nov
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

7. Если база была создана на другой версии проекта и есть ошибки, сначала сделай резервную копию текущего `nov/db.sqlite3`, потом восстанови нужный файл и снова запусти `migrate`.

8. `scripts/com.novator.backup.plist` и `scripts/install_backup_agent.sh` на Windows не используются. Для ежедневного бэкапа там нужен Планировщик задач Windows или ручной запуск `scripts/daily_backup.sh` в подходящей среде.

9. Если нужен ручной возврат из бэкапа, используй `backups/db/latest.sqlite3` и замени им `nov/db.sqlite3`.

## Полезные команды

### Проверка настроек Django

```bash
python manage.py check
```

### Создание миграций после изменения моделей

```bash
python manage.py makemigrations
python manage.py migrate
```

### Запуск административной панели

Админка доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

## Особенности работы

- Главная страница и большинство разделов требуют авторизации.
- Кнопки `Посетил` и `Отменить` обновляют абонемент и создают запись посещаемости.
- При создании клиента генерируется `.docx`-документ в `nov/myapp/templates/client_details_template/`.
- В проекте используется SQLite, поэтому дополнительных сервисов для базы данных не нужно.

## Резервные копии

В репозитории есть скрипты для ежедневного бэкапа SQLite-базы.

- основной скрипт: `scripts/daily_backup.sh`
- macOS LaunchAgent: `scripts/com.novator.backup.plist`
- установщик агента: `scripts/install_backup_agent.sh`
- папка с копиями: `backups/db/`
- актуальная копия: `backups/db/latest.sqlite3`

Если проект переносится на другую машину, проверьте пути в этих скриптах.

Чтобы установить ежедневный бэкап на macOS, запустите:

```bash
./scripts/install_backup_agent.sh
```

## Ручное восстановление базы

Если нужно вернуть базу из резервной копии вручную:

1. Остановите Django-приложение, если оно запущено.
2. Сделайте защитную копию текущей базы:

```bash
cp nov/db.sqlite3 nov/db.sqlite3.before_restore
```

3. Замените текущую базу актуальной копией:

```bash
cp backups/db/latest.sqlite3 nov/db.sqlite3
```

4. Запустите приложение снова и проверьте вход в систему.

Если нужна именно историческая копия, используйте любой сохранённый файл из `backups/db/`, но в текущей схеме бэкап перезаписывается, поэтому основной файл восстановления - `latest.sqlite3`.

## Известные замечания

- В `settings.py` указан путь `nov/static` в `STATICFILES_DIRS`. Если этой папки нет, Django показывает предупреждение `staticfiles.W004`.
- Для локальной разработки это не мешает запуску, но предупреждение можно убрать, если создать папку или поправить настройку.

## Автор

Иван Толпеев
