# Отчёт о развёртывании на PythonAnywhere

Дата: 2026-01-07

Этот файл содержит все важные сведения о том, что было сделано при автоматическом развёртывании проекта на PythonAnywhere. Сохраните этот файл вместе с репозиторием (не содержит секретов), чтобы не потерять настройки.

## Репозиторий
- GitHub: https://github.com/yoavmoiseev/school-scheduler

## Что было сделано (кратко)
- Добавлены скрипты автоматического деплоя и инструкции: `deploy/pa_deploy.sh`, `deploy/deploy_pythonanywhere.md`, `deploy/README_RU_AUTODEPLOY.md`, `deploy/DEPLOY_PYTHONANYWAY_RU.md`, `scripts/web_app_setup.sh`.
- В репозитории создан WSGI‑helper: `deploy/pythonanywhere_wsgi.py` (тоже скопирован в директорию `WEB-ScSc` в ходе скрипта).
- На сервере PythonAnywhere выполнён скрипт `pa_deploy.sh`, который:
  - создал виртуальное окружение `/home/yamSOFT/venv-school-scheduler` и установил зависимости из `requirements.txt`;
  - создал папки `uploads` и `data` в директории проекта;
  - сгенерировал безопасный `SECRET_KEY` и записал его в `.env` в корне проекта (см. ниже);
  - записал WSGI‑helper `pythonanywhere_wsgi.py` в корень проекта `WEB-ScSc`.

## Пути и значения (на сервере)
- Корень проекта: `/home/yamSOFT/school-scheduler/WEB-ScSc`
- Виртуальное окружение: `/home/yamSOFT/venv-school-scheduler`
- WSGI (что используется сервером): `/var/www/yamsoft_pythonanywhere_com_wsgi.py` — заменён на импорт из `app.py` с добавлением `project_home`.
- WSGI helper в проекте: `/home/yamSOFT/school-scheduler/WEB-ScSc/pythonanywhere_wsgi.py`
- Файл с окружением (содержащий `SECRET_KEY`): `/home/yamSOFT/school-scheduler/WEB-ScSc/.env` (ФАЙЛ СОДЕРЖИТ СЕКРЕТ — НЕ ПУБЛИКУЙТЕ)
- Логи (на PythonAnywhere): `/var/log/yamsoft.pythonanywhere.com.error.log` и `/var/log/yamsoft.pythonanywhere.com.server.log`

## Содержимое WSGI, использованное на сервере
```python
import os
import sys

# Путь к корню вашего проекта (где лежит app.py)
project_home = '/home/yamSOFT/school-scheduler/WEB-ScSc'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Загрузить .env если есть (простая парсерная логика KEY=VALUE)
env_path = os.path.join(project_home, '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and v and k not in os.environ:
                os.environ[k] = v

os.environ.setdefault('FLASK_ENV', 'production')

# Импортируем Flask-приложение из `app.py`
from app import app as application
```

## Как проверить приложение вручную (команды на PythonAnywhere Bash)
1) Просмотр логов (последние строки):
```bash
tail -n 200 /var/log/yamsoft.pythonanywhere.com.error.log
tail -n 200 /var/log/yamsoft.pythonanywhere.com.server.log
```
2) Показать WSGI helper в проекте:
```bash
cat ~/school-scheduler/WEB-ScSc/pythonanywhere_wsgi.py
```
3) Проверить наличие `.env` (не публикуйте содержимое):
```bash
ls -la ~/school-scheduler/WEB-ScSc/.env
```
4) Быстрая локальная проверка импорта приложения (в виртуальном окружении):
```bash
source ~/venv-school-scheduler/bin/activate
python - <<'PY'
import sys, importlib
sys.path.insert(0, '/home/yamSOFT/school-scheduler/WEB-ScSc')
try:
    importlib.import_module('app')
    print('import ok')
except Exception as e:
    print('import failed:', e)
PY
```

## Статические файлы (рекомендация для Web tab)
- URL `/static` -> `/home/yamSOFT/school-scheduler/WEB-ScSc/static`
- URL `/uploads` -> `/home/yamSOFT/school-scheduler/WEB-ScSc/uploads`

## Где поместить Excel (если необходимо)
- По умолчанию приложение ищет `data/SchoolScheduler.xlsx` в корне проекта. Загрузите файл в:
  `/home/yamSOFT/school-scheduler/WEB-ScSc/data/SchoolScheduler.xlsx`
- Или укажите путь в переменной окружения `EXCEL_FILE` через Web → Environment variables.

## Как сменить/отрезать `SECRET_KEY`
1) Сгенерировать новый секрет локально или в PythonAnywhere:
```bash
python - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
```
2) Отредактировать файл `/home/yamSOFT/school-scheduler/WEB-ScSc/.env` и заменить значение `SECRET_KEY=...` на новое.
3) На странице Web нажать `Reload`.

## Как отозвать доступ (если предоставляли API token)
- PythonAnywhere: Account → API token → Revoke token.
- Если давали доступ по паролю — смените пароль в Account → Change password.

## Команды для отката / удаления развёртывания
- Удалить `.env` (если хотите убрать секреты с сервера):
```bash
rm ~/school-scheduler/WEB-ScSc/.env
```
- Откат к предыдущему коммиту в репозитории (если нужно):
```bash
cd ~/school-scheduler
git fetch origin
git reset --hard origin/main~1
```

## Файлы, добавленные/изменённые в рамках работы
- `deploy/pa_deploy.sh` — скрипт автодеплоя
- `deploy/pythonanywhere_wsgi.py` — WSGI helper (копия в проекте)
- `deploy/README_RU_AUTODEPLOY.md`, `deploy/deploy_pythonanywhere.md`, `deploy/DEPLOY_PYTHONANYWAY_RU.md` — инструкции
- `scripts/web_app_setup.sh` — локальная helper-скрипт
- Обновлён `/var/www/yamsoft_pythonanywhere_com_wsgi.py` (через WSGI editor на PythonAnywhere)

## Что сохранить где
- Сохраните этот файл `deploy/DEPLOY_REPORT.md` в репозитории (он не содержит секретов).
- Секрет (`SECRET_KEY`) хранится только в `/home/yamSOFT/school-scheduler/WEB-ScSc/.env` на сервере.
- Резервную копию Excel сохраняйте локально и/или в `uploads/backups/`.

## Следующие шаги (рекомендации)
1) Проверьте сайт в браузере: https://yamsoft.pythonanywhere.com
2) Если всё работает, решите где хранить Excel и загрузите его при необходимости.
3) При желании: настроить HTTPS перенаправление (Force HTTPS) и права доступа к тестовому сайту (Password protection) в Web tab.
4) Отозвать API token, если выдавали его временно.

Если нужно — могу добавить сюда экспортированные логи и список точных команд, которые были выполнены (с временными метками). Скажите, хотите ли вы сохранить логи в репо (обычно не рекомендуется — логов не публикуют).

## Конец отчёта
