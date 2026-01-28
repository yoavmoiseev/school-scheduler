# 🚀 Быстрая Справка - School Scheduler на Oracle Cloud

## 🌐 Доступ

- **Сайт:** https://sc.yamsoft.org
- **IP сервера:** 151.145.84.100
- **SSH:** `ssh -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100`

## 📝 Самые частые задачи

### 1. Обновить код на сервере

**Автоматически (рекомендуется):**
```powershell
cd C:\Users\User\Desktop\WEB-ScSc
.\update_server.ps1
```

**Вручную:**
```powershell
# Отправить на GitHub
git add .
git commit -m "Описание изменений"
git push

# Обновить сервер
ssh -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100 'cd ~/apps/WEB-ScSc && git pull && sudo systemctl restart flask-app'
```

### 2. Подключиться к серверу

```powershell
ssh -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100
```

### 3. Перезапустить приложение

```bash
# На сервере:
sudo systemctl restart flask-app

# С локального компьютера:
ssh -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100 'sudo systemctl restart flask-app'
```

### 4. Посмотреть логи

```bash
# Flask логи (последние 50 строк)
sudo journalctl -u flask-app -n 50 --no-pager

# Flask логи в реальном времени
sudo journalctl -u flask-app -f

# Nginx логи
sudo tail -f /var/log/nginx/error.log
```

### 5. Проверить статус

```bash
# Статус Flask
sudo systemctl status flask-app

# Статус Nginx
sudo systemctl status nginx

# Оба сразу
sudo systemctl status flask-app nginx
```

## 🔑 Важные пути

| Что | Где |
|-----|-----|
| SSH ключ | `C:\Users\User\.ssh\oracle_cloud_key` |
| Локальный проект | `C:\Users\User\Desktop\WEB-ScSc` |
| Проект на сервере | `/home/ubuntu/apps/WEB-ScSc` |
| Backup | `/home/ubuntu/apps/WEB-ScSc.backup` |
| Flask service | `/etc/systemd/system/flask-app.service` |
| Nginx config | `/etc/nginx/sites-available/flask-app` |
| SSL сертификаты | `/etc/letsencrypt/live/sc.yamsoft.org/` |

## 🔗 Полезные ссылки

- **Oracle Cloud Console:** https://cloud.oracle.com/
- **GitHub:** https://github.com/yoavmoiseev/school-scheduler
- **Cloudflare:** https://dash.cloudflare.com/
- **Полная документация:** [ORACLE_CLOUD_SETUP.md](deploy/ORACLE_CLOUD_SETUP.md)

## 🆘 Если что-то сломалось

### Сайт не открывается

```bash
# 1. Проверить Flask
ssh -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100 'sudo systemctl restart flask-app && sudo systemctl status flask-app'

# 2. Проверить Nginx
ssh -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100 'sudo nginx -t && sudo systemctl restart nginx'

# 3. Посмотреть логи
ssh -i ~\.ssh\oracle_cloud_key ubuntu@151.145.84.100 'sudo journalctl -u flask-app -n 30 --no-pager'
```

### После обновления кода не работает

```bash
# На сервере:
cd ~/apps/WEB-ScSc
git status  # Проверить состояние
git pull    # Обновить код
sudo systemctl restart flask-app  # Перезапустить
sudo systemctl status flask-app   # Проверить статус
```

### Восстановить данные из backup

```bash
# База данных
cp /home/ubuntu/apps/WEB-ScSc.backup/data/users.db /home/ubuntu/apps/WEB-ScSc/data/

# Файлы
cp -r /home/ubuntu/apps/WEB-ScSc.backup/uploads/* /home/ubuntu/apps/WEB-ScSc/uploads/

sudo systemctl restart flask-app
```

## 📊 Мониторинг

```bash
# CPU, RAM, процессы
htop

# Дисковое пространство
df -h

# Открытые порты
sudo ss -tlnp | grep -E ':80|:443|:5000'

# Firewall правила
sudo iptables -L INPUT -n --line-numbers

# SSL сертификат
sudo certbot certificates
```

## ⚙️ Настройка с нуля (если нужно переделать)

См. подробную инструкцию: [ORACLE_CLOUD_SETUP.md](deploy/ORACLE_CLOUD_SETUP.md)

---

**Последнее обновление:** 25 января 2026
