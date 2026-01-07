# Развёртывание на PythonAnywhere (инструкция на русском)

Короткая инструкция, чтобы быстро развернуть проект на бесплатном аккаунте PythonAnywhere.

1) Создайте аккаунт
- Перейдите на https://www.pythonanywhere.com/ и зарегистрируйтесь (free план).

2) Перенесите код в аккаунт
- Рекомендуем: запушьте репозиторий на GitHub и на PythonAnywhere используйте команду `git clone https://github.com/<ваш_пользователь>/<repo>.git` в Bash-консоли (Files → Open Bash console).

3) Создайте виртуальное окружение и установите зависимости

```bash
python3.11 -m venv ~/venv-school-scheduler
source ~/venv-school-scheduler/bin/activate
pip install -U pip
pip install -r ~/your-repo-path/requirements.txt
```

4) Настройка Web-приложения
- Dashboard → Web → Add a new web app → Manual configuration → выберите ту же версию Python.
- Source code: укажите путь к папке с проектом (например `/home/yourusername/school-scheduler`).
- Virtualenv: укажите `/home/yourusername/venv-school-scheduler`.

5) WSGI
- Откройте WSGI-файл в Web → WSGI configuration file и замените содержимое на (пример):

```python
import os
import sys
project_home = '/home/yourusername/school-scheduler'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
os.environ.setdefault('FLASK_ENV', 'production')
from app import app as application
```

6) Переменные окружения
- В Web → Environment variables добавьте минимум:
  - `SECRET_KEY` — случайная строка (не используйте dev-значение в `config.py`).
  - опционально `EXCEL_FILE`, если загружаете Excel в другое место.

7) Загрузите Excel (если нужно)
- Files → Upload → поместите `data/SchoolScheduler.xlsx` в директорию проекта или укажите путь через `EXCEL_FILE`.

8) Права записи
- Убедитесь, что папки `uploads/` и `data/` существуют: в Bash-консоли выполните `mkdir -p uploads data`.

9) Перезагрузите приложение и проверяйте логи
- Нажмите `Reload` в Web табе и откройте URL.
- В случае ошибок смотрите `error.log` и `server.log` (Web tab → View logs).

10) Если хотите полностью автоматизировать развёртывание
- Я могу подготовить и запустить скрипт, который: клонирует репозиторий в ваш аккаунт PythonAnywhere, создаст/активирует виртуenv, установит зависимости, настроит WSGI и переменные окружения. Для этого мне потребуется ваш PythonAnywhere API token (создаётся в Account → API token). Токен можно отозвать после деплоя.

Если хотите автоматический запуск — пришлите API token и подтвердите, что разрешаете временные действия с вашим аккаунтом (я удалю/информирую вас после завершения и вы сможете отозвать токен).
