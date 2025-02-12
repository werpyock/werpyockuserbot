#!/bin/sh
echo "Устанавливаем необходимые пакеты..."
pkg update -y
pkg upgrade -y
pkg install -y git python openssl
echo "Устанавливаем зависимости Python для запуска..."
pip install --upgrade pip
pip install telethon
echo "Запускаю установку Werpyock Userbot.."
python start.py
