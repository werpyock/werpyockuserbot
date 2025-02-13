import configparser
import os
import sys
import subprocess

CONFIG_FILE = 'config.ini'
MAIN_SCRIPT = 'main.py'

def get_input(prompt):
    """Безопасный ввод с обработкой EOFError."""
    try:
        return input(prompt)
    except EOFError:
        print("\nОшибка: Не удалось получить ввод. Запустите скрипт в интерактивном режиме.")
        sys.exit(1)

def create_config():
    config = configparser.ConfigParser()
    config.add_section('Telegram')
    config.set('Telegram', 'API_ID', get_input('Введите ваш API ID: '))
    config.set('Telegram', 'API_HASH', get_input('Введите ваш API Hash: '))
    config.set('Telegram', 'prefix', get_input('Введите желаемый префикс команд (например, !): ')))

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

    print(f'Конфигурационный файл {CONFIG_FILE} успешно создан.')

def run_main():
    """Запускает main.py, если он существует."""
    if os.path.exists(MAIN_SCRIPT):
        print(f'Запуск {MAIN_SCRIPT}...')
        subprocess.run(["python", MAIN_SCRIPT], check=True)
    else:
        print(f'Ошибка: {MAIN_SCRIPT} не найден. Убедитесь, что файл существует.')

if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        create_config()
    
    run_main()
