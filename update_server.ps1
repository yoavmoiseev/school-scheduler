# Скрипт для обновления кода на сервере
# Использование: .\update_server.ps1

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
