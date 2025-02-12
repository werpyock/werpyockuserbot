#!/bin/sh
echo "Устанавливаем необходимые пакеты..."
pkg update -y
pkg upgrade -y
pkg install -y git python openssl
git clone https://github.com/werpyock/werpyockuserbot.git
cd werpyockuserbot
echo "Устанавливаем зависимости Python для запуска..."
pip install --upgrade pip
pip install telethon
echo "Запускаю Werpyock Userbot.."
python start.py
