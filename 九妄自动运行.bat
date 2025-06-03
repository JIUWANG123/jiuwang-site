@echo off
title 自动备份与恢复九妄网页数据
color 0C
echo.
echo 正在备份 gallery.json 与 messages.json...
python backup.py
echo.
echo ================================
echo 请部署或推送 GitHub 后按任意键继续
pause >nul
echo 正在恢复上传记录与留言...
python restore.py
echo.
echo ✅ 完成：数据已备份并恢复
pause