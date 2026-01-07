# Автодеплой на PythonAnywhere — инструкция (русский)

Этот документ описывает, как выполнить автодеплой скриптом в вашем аккаунте PythonAnywhere. Скрипт находится в `deploy/pa_deploy.sh` и рассчитан на запуск в Bash-консоли PythonAnywhere.

Шаги:

1) Войдите в свой аккаунт PythonAnywhere и откройте Bash-консоль (Dashboard → Consoles → Start a Bash console).

2) Клонируйте репозиторий (если ещё не клонировали):

```bash
git clone https://github.com/yoavmoiseev/school-scheduler.git
cd school-scheduler
```

3) Запустите автодеплой скрипт из папки репозитория:

```bash
bash deploy/pa_deploy.sh
```

Скрипт выполнит:
- создание виртуального окружения `~/venv-school-scheduler` (если ещё нет),
- установку зависимостей из `requirements.txt`,
- создание папок `uploads` и `data`,
- создание файла `.env` с безопасным `SECRET_KEY` (если `.env` ещё нет),
- запись файла `pythonanywhere_wsgi.py` в корень проекта (его содержимое нужно вставить в WSGI-конфиг через Web tab).

4) В Web → Web tab:
- Установите "Source code" на путь к репозиторию (`/home/yourusername/school-scheduler`),
- Установите Virtualenv на `/home/yourusername/venv-school-scheduler`,
- Откройте WSGI configuration file и замените содержимое на содержимое `pythonanywhere_wsgi.py` (файл, созданный скриптом),
- Нажмите Reload.

5) После перезагрузки проверьте `error.log` и `server.log` в Web tab при необходимости.

Безопасность:
- Скрипт записывает `SECRET_KEY` в `.env` в корне проекта. Этот файл не должен попадать в публичный репозиторий; если ваш репозиторий публичен — удалите `.env` из репозитория и храните его только на сервере.
- Если захотите, вы можете позже отозвать токен (в Account → API token) или изменить `SECRET_KEY` через создание нового значения и замены в `.env`.

Если хотите — я могу сгенерировать отчёт после запуска: URL, содержимое `.env` (секреты не вывожу публично), какие команды выполнены, и что нужно сохранить.
