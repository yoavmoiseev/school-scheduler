# 🚀 Инструкция: Деплой на Oracle Cloud Always Free

## 📋 Содержание
1. [Регистрация Oracle Cloud](#регистрация)
2. [Создание VM Instance](#создание-vm)
3. [Настройка сервера](#настройка-сервера)
4. [Деплой приложения](#деплой-приложения)
5. [Настройка Custom Domain](#настройка-домена)
6. [Защита от Idle Reclaim](#защита-от-удаления)
7. [Обновление кода через Git](#обновление-git)
8. [Текущая настройка проекта](#текущая-настройка)

---

## 1️⃣ Регистрация Oracle Cloud {#регистрация}

### Шаг 1: Создание аккаунта

1. Перейдите на: https://www.oracle.com/cloud/free/
2. Нажмите **"Start for free"**
3. Заполните форму регистрации:
   - **Email** (лучше Gmail)
   - **Country/Territory** (выберите вашу страну)
   - Имя и фамилия
   
4. Подтвердите email

### Шаг 2: Верификация аккаунта

1. **Выберите Home Region** (регион, где будут ресурсы):
   - Рекомендую: **Germany Central (Frankfurt)** - ближе к Европе/Израилю
   - Или: **UK South (London)**
   - ⚠️ **ВАЖНО:** Home Region нельзя изменить потом!

2. **Введите данные кредитной карты:**
   - Карта нужна только для верификации
   - Списание будет только $1 (вернут сразу)
   - ✅ Без карты Always Free не будет работать
   - ❌ Автоматического списания НЕ будет

3. Пройдите SMS верификацию

### Шаг 3: Подтверждение аккаунта

- Активация занимает **5-30 минут**
- Придет email: "Your Oracle Cloud Account is Ready"
- Войдите в консоль: https://cloud.oracle.com/

---

## 2️⃣ Создание VM Instance {#создание-vm}

### Подготовка: Создание SSH ключа

**Windows (PowerShell):**
```powershell
# Создать папку для ключей
mkdir ~\.ssh -Force

# Создать SSH ключ
ssh-keygen -t rsa -b 4096 -f ~\.ssh\oracle_cloud_key

# НЕ вводите passphrase (просто Enter)
```

Будет создано 2 файла:
- `oracle_cloud_key` (приватный ключ - хранить в секрете!)
- `oracle_cloud_key.pub` (публичный ключ - для Oracle)

**Скопируйте публичный ключ:**
```powershell
Get-Content ~\.ssh\oracle_cloud_key.pub
```

### Создание VM в Oracle Cloud Console

1. **Войдите в консоль:** https://cloud.oracle.com/
2. **Откройте меню** ≡ (слева сверху)
3. **Compute** → **Instances**
4. Нажмите **"Create Instance"**

### Настройки Instance:

#### **1. Name and placement:**
- **Name:** `flask-app-1` (или любое имя)
- **Compartment:** оставить по умолчанию (root)

#### **2. Image and shape:**

**Image:**
- Нажмите **"Change Image"**
- Выберите: **Ubuntu 22.04 Minimal**
- Нажмите **"Select Image"**

**Shape:**
- Нажмите **"Change Shape"**
- Выберите **"Ampere"** (ARM процессоры)
- Выберите **"VM.Standard.A1.Flex"**
- Настройте:
  - **OCPU count:** `2` (для одного сайта) или `1` (для нескольких)
  - **Memory (GB):** `12` (для 2 OCPU) или `6` (для 1 OCPU)
- Нажмите **"Select Shape"**

💡 **Для 2-3 сайтов:**
- Создайте 2-3 VM по 1 OCPU + 6GB каждая
- ИЛИ одну VM 4 OCPU + 24GB для всех сайтов

#### **3. Networking:**
- **VCN:** оставить по умолчанию (будет создана автоматически)
- **Subnet:** Public Subnet
- ✅ **"Assign a public IPv4 address"** - включить!

#### **4. Add SSH keys:**
- Выберите **"Paste public keys"**
- Вставьте содержимое файла `oracle_cloud_key.pub`

#### **5. Boot volume:**
- **Size:** `50 GB` (минимум)
- Или увеличьте до 100-200 GB (используется из 200GB лимита)

#### **6. Create:**
- Нажмите **"Create"**

### ⏳ Ожидание создания:

- Создание займет **2-5 минут**
- Статус изменится: `Provisioning` → `Running`
- **Сохраните Public IP адрес!** (будет показан в деталях Instance)

---

## 3️⃣ Настройка сервера {#настройка-сервера}

### Шаг 1: Открытие портов в Oracle Cloud

**В консоли Oracle Cloud:**

1. **Compute** → **Instances** → выберите вашу VM
2. **Instance Details** → **Primary VNIC** → нажмите на имя subnet
3. **Security Lists** → нажмите на **Default Security List**
4. Нажмите **"Add Ingress Rules"**

**Добавьте правила:**

**Правило 1 - HTTP:**
- **Source Type:** CIDR
- **Source CIDR:** `0.0.0.0/0`
- **IP Protocol:** TCP
- **Destination Port Range:** `80`
- **Description:** `HTTP`

**Правило 2 - HTTPS:**
- **Source Type:** CIDR
- **Source CIDR:** `0.0.0.0/0`
- **IP Protocol:** TCP
- **Destination Port Range:** `443`
- **Description:** `HTTPS`

**Правило 3 - Flask (опционально, для тестов):**
- **Source Type:** CIDR
- **Source CIDR:** `0.0.0.0/0`
- **IP Protocol:** TCP
- **Destination Port Range:** `5000`
- **Description:** `Flask Dev`

### Шаг 2: Подключение к VM через SSH

**Windows (PowerShell):**
```powershell
ssh -i ~\.ssh\oracle_cloud_key ubuntu@YOUR_PUBLIC_IP
```

Замените `YOUR_PUBLIC_IP` на ваш IP адрес из консоли Oracle.

При первом подключении ответьте `yes`.

### Шаг 3: Настройка firewall на Ubuntu

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Открытие портов в Ubuntu firewall
# ВАЖНО: Вставляем правила ПЕРЕД правилом REJECT (обычно на позиции 5)
sudo iptables -I INPUT 5 -m state --state NEW -p tcp --dport 5000 -j ACCEPT
sudo iptables -I INPUT 5 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 5 -m state --state NEW -p tcp --dport 80 -j ACCEPT

# Проверить правила (порты 80, 443, 5000 должны быть ПЕРЕД REJECT)
sudo iptables -L INPUT -n --line-numbers

# Сохранение правил
sudo netfilter-persistent save

# Если netfilter-persistent не установлен:
sudo apt install iptables-persistent -y
sudo netfilter-persistent save
```

### Шаг 4: Установка необходимого ПО

```bash
# Установка Python и зависимостей
sudo apt install -y python3 python3-pip python3-venv git

# Установка Nginx (для reverse proxy)
sudo apt install -y nginx

# Установка Certbot (для SSL сертификатов)
sudo apt install -y certbot python3-certbot-nginx

# Установка Docker (опционально)
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ubuntu

# Перелогиниться для применения docker группы
exit
# Подключиться снова
ssh -i ~\.ssh\oracle_cloud_key ubuntu@YOUR_PUBLIC_IP
```

---

## 4️⃣ Деплой приложения {#деплой-приложения}

### Вариант A: Деплой с Git

#### Шаг 1: Клонирование проекта

```bash
# Создать папку для проектов
mkdir -p ~/apps
cd ~/apps

# Клонировать ваш репозиторий (если есть на GitHub)
git clone YOUR_REPO_URL
cd WEB-ScSc

# ИЛИ создать папку и загрузить файлы вручную
mkdir -p ~/apps/WEB-ScSc
```

#### Шаг 2: Загрузка файлов (если нет Git)

**На вашем локальном компьютере (PowerShell):**

```powershell
# Перейти в папку проекта
cd C:\Users\User\Desktop\WEB-ScSc\WEB-ScSc

# Создать архив (7zip или WinRAR)
# ИЛИ использовать SCP:

scp -i ~\.ssh\oracle_cloud_key -r ./* ubuntu@YOUR_PUBLIC_IP:~/apps/WEB-ScSc/
```

#### Шаг 3: Настройка Python окружения

```bash
cd ~/apps/WEB-ScSc

# Создать virtual environment
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Создать необходимые папки
mkdir -p data uploads/backups uploads/favorites uploads/tmp

# Установить права
chmod 755 data uploads
```

#### Шаг 4: Тестовый запуск

```bash
# Запуск приложения
python app.py
```

Откройте в браузере: `http://YOUR_PUBLIC_IP:5000`

Если работает - **Ctrl+C** для остановки.

### Шаг 5: Создание systemd service

```bash
# Создать service файл
sudo nano /etc/systemd/system/flask-app.service
```

**Содержимое файла:**

```ini
[Unit]
Description=Flask School Schedule App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/apps/WEB-ScSc
Environment="PATH=/home/ubuntu/apps/WEB-ScSc/venv/bin"
ExecStart=/home/ubuntu/apps/WEB-ScSc/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 2 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Сохранить: **Ctrl+O**, **Enter**, **Ctrl+X**

```bash
# Активировать service
sudo systemctl daemon-reload
sudo systemctl enable flask-app
sudo systemctl start flask-app

# Проверить статус
sudo systemctl status flask-app

# Посмотреть логи
sudo journalctl -u flask-app -f
```

### Шаг 6: Настройка Nginx

```bash
# Создать конфигурацию Nginx
sudo nano /etc/nginx/sites-available/flask-app
```

**Содержимое файла:**

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN.com www.YOUR_DOMAIN.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Увеличить таймаут для загрузки файлов
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    # Лимит размера загружаемых файлов
    client_max_body_size 20M;
}
```

Замените `YOUR_DOMAIN.com` на ваш домен.

```bash
# Активировать конфигурацию
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/

# Удалить дефолтную конфигурацию
sudo rm /etc/nginx/sites-enabled/default

# Проверить конфигурацию
sudo nginx -t

# Перезапустить Nginx
sudo systemctl restart nginx
```

---

## 5️⃣ Настройка Custom Domain {#настройка-домена}

### Шаг 1: Настройка DNS записей

В панели управления вашего доменного регистратора (где купили домен):

**Добавьте A записи:**

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_PUBLIC_IP | 3600 |
| A | www | YOUR_PUBLIC_IP | 3600 |

Замените `YOUR_PUBLIC_IP` на IP адрес вашей VM.

**Проверка DNS (через 5-30 минут):**

```bash
# На вашем компьютере или на сервере:
nslookup YOUR_DOMAIN.com
```

### Шаг 2: Установка SSL сертификата

**На сервере:**

```bash
# Получить SSL сертификат от Let's Encrypt
sudo certbot --nginx -d YOUR_DOMAIN.com -d www.YOUR_DOMAIN.com

# Ответить на вопросы:
# Email: введите ваш email
# Terms of Service: Yes
# Redirect HTTP to HTTPS: Yes (рекомендуется)
```

**Автообновление сертификата:**

```bash
# Проверить автообновление
sudo certbot renew --dry-run

# Если работает - сертификат будет обновляться автоматически каждые 90 дней
```

### Шаг 3: Проверка

Откройте в браузере: `https://YOUR_DOMAIN.com`

✅ Должен работать с SSL сертификатом!

---

## 6️⃣ Защита от Idle Reclaim {#защита-от-удаления}

Oracle удаляет VM, если за 7 дней:
- CPU < 20%
- Network < 20%
- Memory < 20% (только A1)

### Решение 1: Cron job (легкий)

```bash
# Создать скрипт
nano ~/keep-alive.sh
```

**Содержимое:**

```bash
#!/bin/bash
# Keep Oracle VM alive by generating CPU activity

# 20% CPU load for 10 seconds
stress-ng --cpu 1 --cpu-load 20 --timeout 10s &> /dev/null

# Small network activity
curl -s https://www.google.com &> /dev/null
```

```bash
# Дать права на выполнение
chmod +x ~/keep-alive.sh

# Установить stress-ng
sudo apt install -y stress-ng

# Добавить в crontab
crontab -e
```

**Добавьте строку:**

```
# Keep Oracle VM alive - run every hour
0 * * * * /home/ubuntu/keep-alive.sh
```

Сохранить и выйти.

### Решение 2: Мониторинг systemd service

```bash
sudo nano /etc/systemd/system/keepalive.service
```

**Содержимое:**

```ini
[Unit]
Description=Keep Oracle VM Alive
After=network.target

[Service]
Type=simple
User=ubuntu
ExecStart=/bin/bash -c 'while true; do stress-ng --cpu 1 --cpu-load 15 --timeout 30s; sleep 1800; done'
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable keepalive
sudo systemctl start keepalive
```

---

## 🎯 Для нескольких сайтов

### Вариант 1: Несколько VM (по одной на сайт)

Повторите шаги 2-5 для каждой VM:
- VM 1: domain1.com → IP1
- VM 2: domain2.com → IP2
- VM 3: domain3.com → IP3

### Вариант 2: Один сервер, несколько доменов

**Запустите приложения на разных портах:**

```bash
# App 1 на порту 5000
# App 2 на порту 5001
# App 3 на порту 5002
```

**Nginx конфигурация для нескольких доменов:**

```nginx
# Сайт 1
server {
    listen 80;
    server_name domain1.com www.domain1.com;
    location / {
        proxy_pass http://127.0.0.1:5000;
        # ... остальные настройки
    }
}

# Сайт 2
server {
    listen 80;
    server_name domain2.com www.domain2.com;
    location / {
        proxy_pass http://127.0.0.1:5001;
        # ... остальные настройки
    }
}
```

---

## 📊 Мониторинг ресурсов

```bash
# CPU и RAM
htop

# Дисковое пространство
df -h

# Логи приложения
sudo journalctl -u flask-app -f

# Логи Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Статус всех сервисов
sudo systemctl status flask-app nginx keepalive
```

---

## 🔄 Обновление приложения

```bash
cd ~/apps/WEB-ScSc

# Остановить приложение
sudo systemctl stop flask-app

# Обновить код (если Git)
git pull

# ИЛИ загрузить новые файлы через SCP

# Активировать venv
source venv/bin/activate

# Обновить зависимости (если нужно)
pip install -r requirements.txt

# Запустить приложение
sudo systemctl start flask-app

# Проверить статус
sudo systemctl status flask-app
```

---

## 🆘 Решение проблем

### Не могу создать VM (Out of Capacity)

**Причина:** В выбранном регионе нет свободных Always Free ресурсов.

**Решение:**
1. Попробуйте другую Availability Domain (AD-1, AD-2, AD-3)
2. Попробуйте позже (утро/ночь по времени региона)
3. Обновите страницу и создавайте снова каждые 10 минут

### Не могу подключиться по SSH

```bash
# Проверьте права на ключ
chmod 600 ~/.ssh/oracle_cloud_key

# Попробуйте с verbose
ssh -v -i ~/.ssh/oracle_cloud_key ubuntu@YOUR_IP

# Проверьте Security List в Oracle Console
```

### Сайт не открывается

```bash
# Проверьте статус приложения
sudo systemctl status flask-app

# Проверьте порты
sudo netstat -tulpn | grep 5000

# Проверьте Nginx
sudo nginx -t
sudo systemctl status nginx

# Проверьте firewall правила в Oracle Console
```

### SSL сертификат не устанавливается

```bash
# Убедитесь что DNS настроен правильно
nslookup YOUR_DOMAIN.com

# Проверьте что Nginx работает на порту 80
curl -I http://YOUR_DOMAIN.com

# Попробуйте снова
sudo certbot --nginx -d YOUR_DOMAIN.com -d www.YOUR_DOMAIN.com
```

---

## 📚 Полезные ссылки

- Oracle Cloud Console: https://cloud.oracle.com/
- Oracle Cloud Docs: https://docs.oracle.com/en-us/iaas/
- Let's Encrypt: https://letsencrypt.org/
- Nginx Docs: https://nginx.org/en/docs/

---

## ✅ Чек-лист деплоя

- [ ] Зарегистрирован аккаунт Oracle Cloud
- [ ] Создана VM Instance (ARM A1)
- [ ] Открыты порты 80, 443 в Security List
- [ ] Подключился по SSH
- [ ] Установлено ПО (Python, Nginx, Certbot)
- [ ] Загружен проект на сервер
- [ ] Создан systemd service для Flask
- [ ] Настроен Nginx reverse proxy
- [ ] Настроены DNS A-записи
- [ ] Установлен SSL сертификат
- [ ] Настроена защита от Idle Reclaim
- [ ] Сайт работает на HTTPS!

---

**🎉 Готово! Ваше приложение теперь работает на Oracle Cloud бесплатно!**

---

## 7️⃣ Обновление кода через Git {#обновление-git}

### Текущая настройка

**Репозиторий GitHub:** https://github.com/yoavmoiseev/school-scheduler

**Путь на сервере:** `/home/ubuntu/apps/WEB-ScSc`

### Способ 1: Автоматический скрипт (рекомендуется)

**На локальном компьютере:**

```powershell
cd C:\Users\User\Desktop\WEB-ScSc
.\update_server.ps1
```

**Скрипт делает:**
1. `git add .` + `git commit` + `git push` на GitHub
2. На сервере: `git pull` + перезапуск Flask
3. Показывает статус приложения

**Если скрипта нет, создайте:**

```powershell
# Создать файл update_server.ps1
New-Item -Path "C:\Users\User\Desktop\WEB-ScSc\update_server.ps1" -ItemType File -Force
```

**Содержимое update_server.ps1:**

```powershell
# Скрипт для обновления кода на сервере
Write-Host "🚀 Обновление сервера sc.yamsoft.org..." -ForegroundColor Cyan

# Git push локально
Write-Host "`n📤 Отправка изменений на GitHub..." -ForegroundColor Yellow
git add .
$message = Read-Host "Введите сообщение коммита (или Enter для 'Update')"
if ([string]::IsNullOrWhiteSpace($message)) {
    $message = "Update"
}
git commit -m $message
git push origin main

# Обновление на сервере
Write-Host "`n📥 Обновление кода на сервере..." -ForegroundColor Yellow
& 'C:\Windows\System32\OpenSSH\ssh.exe' -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100 'cd ~/apps/WEB-ScSc; git pull; sudo systemctl restart flask-app'

# Проверка статуса
Write-Host "`n✅ Проверка статуса..." -ForegroundColor Yellow
& 'C:\Windows\System32\OpenSSH\ssh.exe' -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100 'sudo systemctl status flask-app --no-pager | head -10'

Write-Host "`n🎉 Готово! Сайт обновлён: https://sc.yamsoft.org" -ForegroundColor Green
```

### Способ 2: Ручное обновление

**Вариант A: С вашего компьютера (одной командой)**

```powershell
# 1. Отправить изменения на GitHub
git add .
git commit -m "Описание изменений"
git push origin main

# 2. Обновить на сервере и перезапустить
ssh -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100 'cd ~/apps/WEB-ScSc && git pull && sudo systemctl restart flask-app'
```

**Вариант B: Прямо на сервере**

```powershell
# Подключиться к серверу
ssh -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100

# На сервере выполнить:
cd ~/apps/WEB-ScSc
git pull
sudo systemctl restart flask-app

# Проверить статус
sudo systemctl status flask-app
```

### Проверка обновления

```bash
# Посмотреть текущий коммит на сервере
ssh -i ~/.ssh/oracle_cloud_key ubuntu@151.145.84.100 'cd ~/apps/WEB-ScSc && git log -1 --oneline'

# Посмотреть логи приложения
ssh -i ~/.ssh/oracle_cloud_key ubuntu@151.145.84.100 'sudo journalctl -u flask-app -n 50 --no-pager'
```

---

## 8️⃣ Текущая настройка проекта {#текущая-настройка}

### 🌐 Основная информация

| Параметр | Значение |
|----------|----------|
| **Домен** | https://sc.yamsoft.org |
| **IP адрес** | 151.145.84.100 |
| **SSH ключ** | `C:\Users\User\.ssh\oracle_cloud_key` |
| **Репозиторий** | https://github.com/yoavmoiseev/school-scheduler |
| **Регион Oracle** | Israel Jerusalem (IL-JERUSALEM-1) |
| **VM Instance** | flask-app-2 (VM.Standard.E2.1.Micro) |

### 📂 Структура на сервере

```
/home/ubuntu/
├── apps/
│   ├── WEB-ScSc/              # Основное приложение (Git репозиторий)
│   │   ├── app.py             # Flask приложение
│   │   ├── venv/              # Python virtual environment
│   │   ├── data/              # База данных SQLite
│   │   ├── uploads/           # Загруженные файлы
│   │   └── ...                # Остальные файлы проекта
│   └── WEB-ScSc.backup/       # Backup старой версии (можно удалить)
└── keep-alive.sh              # Скрипт защиты от Idle Reclaim
```

### 🔧 Сервисы и конфигурация

**Systemd service:**
- Путь: `/etc/systemd/system/flask-app.service`
- Команды:
  - Запуск: `sudo systemctl start flask-app`
  - Остановка: `sudo systemctl stop flask-app`
  - Перезапуск: `sudo systemctl restart flask-app`
  - Статус: `sudo systemctl status flask-app`
  - Логи: `sudo journalctl -u flask-app -f`

**Nginx конфигурация:**
- Путь: `/etc/nginx/sites-available/flask-app`
- Слушает: порт 80 (HTTP) и 443 (HTTPS)
- Проксирует на: `http://127.0.0.1:5000`
- Команды:
  - Проверка: `sudo nginx -t`
  - Перезагрузка: `sudo systemctl reload nginx`
  - Логи доступа: `sudo tail -f /var/log/nginx/access.log`
  - Логи ошибок: `sudo tail -f /var/log/nginx/error.log`

**SSL сертификат:**
- Выдан: Let's Encrypt
- Домен: sc.yamsoft.org
- Путь сертификата: `/etc/letsencrypt/live/sc.yamsoft.org/`
- Автообновление: каждые 90 дней (настроено автоматически)
- Проверка: `sudo certbot certificates`

**Keep-alive защита:**
- Скрипт: `/home/ubuntu/keep-alive.sh`
- Cron: каждый час (0 * * * *)
- Проверка: `crontab -l`

### 📱 Cloudflare DNS

**Текущие записи для yamsoft.org:**

| Type | Name | Value | Proxy |
|------|------|-------|---------|
| A | sc | 151.145.84.100 | DNS only (🟠) |
| CNAME | www | yoavmoiseev.github.io | DNS only |
| A | @ | 185.199.108-111.153 (GitHub Pages) | DNS only |

⚠️ **Важно:** Proxy status должен быть **DNS only** (оранжевая иконка), иначе Let's Encrypt не сможет выдать сертификат.

### 🔐 SSH подключение

**С Windows PowerShell:**

```powershell
# Подключение к серверу
ssh -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100

# Или полный путь
ssh -i C:\Users\User\.ssh\oracle_cloud_key ubuntu@151.145.84.100
```

**Первое подключение:**
- При первом подключении появится вопрос о fingerprint
- Ответьте `yes` для добавления в known_hosts

### 📦 Установленное ПО

| Пакет | Версия | Назначение |
|-------|--------|------------|
| Python | 3.10.12 | Запуск Flask приложения |
| Nginx | 1.18.0 | Reverse proxy и SSL |
| Git | 2.34.1 | Обновление кода |
| Certbot | 1.21.0 | SSL сертификаты Let's Encrypt |
| stress-ng | 0.13.12 | Keep-alive защита |
| cron | 3.0pl1 | Планировщик задач |

### 🔄 Частые команды

**Перезапуск всех сервисов:**

```bash
sudo systemctl restart flask-app nginx
```

**Проверка статуса всего:**

```bash
sudo systemctl status flask-app nginx
```

**Просмотр логов в реальном времени:**

```bash
# Flask логи
sudo journalctl -u flask-app -f

# Nginx логи
sudo tail -f /var/log/nginx/access.log /var/log/nginx/error.log
```

**Обновление кода:**

```bash
cd ~/apps/WEB-ScSc
git fetch origin
# Жёстко синхронизировать рабочую копию с origin/main
git reset --hard origin/main
sudo chown -R ubuntu:ubuntu /home/ubuntu/apps/WEB-ScSc
sudo systemctl restart flask-app
```

**Проверка открытых портов:**

```bash
sudo ss -tlnp | grep -E ':80|:443|:5000'
```

**Проверка firewall:**

```bash
sudo iptables -L INPUT -n --line-numbers
```

### 🆘 Восстановление после проблем

**Если сайт не работает:**

```bash
# 1. Проверить статус сервисов
sudo systemctl status flask-app nginx

# 2. Перезапустить Flask
sudo systemctl restart flask-app

# 3. Проверить логи
sudo journalctl -u flask-app -n 50 --no-pager

# 4. Проверить Nginx
sudo nginx -t
sudo systemctl restart nginx

# 5. Проверить что Flask слушает на 5000
sudo ss -tlnp | grep 5000
```

**Если потерян SSH доступ:**

1. Зайдите в Oracle Cloud Console: https://cloud.oracle.com/
2. Compute → Instances → flask-app-2
3. Используйте Console Connection для доступа через браузер

**Если нужно восстановить данные:**

```bash
# Backup находится в:
/home/ubuntu/apps/WEB-ScSc.backup/

# Восстановить базу данных:
cp /home/ubuntu/apps/WEB-ScSc.backup/data/users.db /home/ubuntu/apps/WEB-ScSc/data/

# Восстановить файлы:
cp -r /home/ubuntu/apps/WEB-ScSc.backup/uploads/* /home/ubuntu/apps/WEB-ScSc/uploads/
```

---

## ✅ Критическая секция: гарантированный и предсказуемый деплой

Ниже — проверенные правила, которые нужно соблюдать, чтобы обновления из GitHub
всегда автоматически отражались на сервере и чтобы не было "двойных" копий кода.

1) Структура репозитория и рабочая директория сервиса
- Отслеживаемая версия приложения находится в подпапке `WEB-ScSc/` репозитория.
- Сервис systemd должен запускать приложение из этой подпапки, а не из верхнего уровня.
    Рекомендуемый `flask-app.service` (пример):

```ini
[Unit]
Description=Flask School Schedule App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/apps/WEB-ScSc/WEB-ScSc
Environment=PATH=/home/ubuntu/apps/WEB-ScSc/venv/bin
ExecStart=/home/ubuntu/apps/WEB-ScSc/venv/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2) Корректный рабочий процесс (developer -> server)
- Локально: правки → тест → `git add .` → `git commit -m "..."` → `git push origin main`
- На сервере (автоматически или вручную):

```bash
cd /home/ubuntu/apps/WEB-ScSc
git fetch origin
git reset --hard origin/main
sudo chown -R ubuntu:ubuntu /home/ubuntu/apps/WEB-ScSc
sudo systemctl restart flask-app
```

3) Никогда не держать две рабочие копии одновременно
- Не создавайте вручную дубли файлов на верхнем уровне (top-level). Если до этого были
    неотслеживаемые файлы (они отображаются как `??` в `git status`), их нужно удалить
    или перенести в `WEB-ScSc/` и закоммитить. Иначе `git pull` не перезапишет их.

4) Виртуальное окружение
- При обновлении можно восстановить `venv` из бэкапа или пересоздать:

```bash
python3 -m venv /home/ubuntu/apps/WEB-ScSc/venv
/home/ubuntu/apps/WEB-ScSc/venv/bin/pip install -r /home/ubuntu/apps/WEB-ScSc/WEB-ScSc/requirements.txt
```

5) Быстрая диагностика (если сайт не изменился после `git reset`)
- Проверить, откуда запущен процесс:

```bash
sudo systemctl show -p ExecStart -p WorkingDirectory flask-app
ps aux | grep python | grep flask-app
```

- Проверить git status и untracked файлы:

```bash
cd /home/ubuntu/apps/WEB-ScSc
git status --porcelain
git ls-files --others --exclude-standard
```

6) Рекомендация: используйте `git reset --hard origin/main` (вместо `git pull`),
     чтобы гарантированно привести рабочую копию в соответствие с `origin/main`.

7) Про `offline` ветку
- Ветка `offline` содержит автономную сборку, её **не нужно** использовать для продакшена.

Если следовать этим инструкциям, обновления с GitHub будут попадать на сервер корректно
и сервис будет запускать именно ту копию, которую вы правите и пушите.

### 📞 Контакты и ссылки

- **Oracle Cloud Console:** https://cloud.oracle.com/
- **GitHub репозиторий:** https://github.com/yoavmoiseev/school-scheduler
- **Cloudflare Dashboard:** https://dash.cloudflare.com/
- **Сайт:** https://sc.yamsoft.org
- **Email для SSL уведомлений:** yoav@yamsoft.org

---

**🎉 Готово! Ваше приложение теперь работает на Oracle Cloud бесплатно!**
