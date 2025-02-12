import configparser
import os

CONFIG_FILE = 'config.ini'

def create_config():
    config = configparser.ConfigParser()
    config.add_section('Telegram')
    config.set('Telegram', 'API_ID', input('Введите ваш API ID: '))
    config.set('Telegram', 'API_HASH', input('Введите ваш API Hash: '))
    config.set('Telegram', 'prefix', input('Введите желаемый префикс команд (например, !): '))

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    print(f'Конфигурационный файл {CONFIG_FILE} успешно создан.')

if __name__ == '__main__':
    if os.path.exists(CONFIG_FILE):
        overwrite = input(f'Файл {CONFIG_FILE} уже существует. Перезаписать? (y/n): ').lower()
        if overwrite != 'y':
            print('Настройка отменена.')
            exit()
    create_config()
    os.system("python main.py")
