import os
import importlib
import configparser
import logging
import sqlite3
from telethon import TelegramClient, events

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
CONFIG_FILE = 'config.ini'
MODULES_DIR = 'modules'
PROTECTED_MODULES = {'modulemanager', 'utility'}

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
API_ID = int(config.get('Telegram', 'API_ID'))
API_HASH = config.get('Telegram', 'API_HASH')
COMMAND_PREFIX = config.get('Telegram', 'prefix', fallback='!')

client = TelegramClient('werpyock_userbot', API_ID, API_HASH)
client.commands = {}
client.command_prefix = COMMAND_PREFIX
loaded_modules = {}

def init_db():
    conn = sqlite3.connect("werpyock_userbot.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS aliases (alias TEXT PRIMARY KEY, command TEXT NOT NULL)")
    conn.commit()
    return conn

def get_alias(alias):
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT command FROM aliases WHERE alias = ?", (alias,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def load_module(module_name):
    module_name = module_name.lower()
    if module_name in loaded_modules:
        logging.info("Module %s already loaded.", module_name)
        return f"⚠️ Module '{module_name}' already loaded."
    try:
        module = importlib.import_module(f'{MODULES_DIR}.{module_name}')
        if hasattr(module, 'setup'):
            module.setup(client)
            for cmd, func in module.commands.items():
                client.commands[cmd.lower()] = func
        loaded_modules[module_name] = module
        logging.info("Module %s loaded.", module_name)
        return f"✅ Module '{module_name}' loaded successfully."
    except Exception as e:
        if module_name not in PROTECTED_MODULES:
            logging.error("Error loading module %s: %s", module_name, e)
        return f"❌ Error loading module '{module_name}': {e}"

def unload_module(module_name):
    module_name = module_name.lower()
    if module_name not in loaded_modules:
        logging.info("Module %s not loaded.", module_name)
        return f"⚠️ Module '{module_name}' is not loaded."
    if module_name in PROTECTED_MODULES:
        logging.info("Protected module %s unload attempt ignored.", module_name)
        return f"✅ Module '{module_name}' is protected and cannot be unloaded."
    try:
        if hasattr(loaded_modules[module_name], 'teardown'):
            loaded_modules[module_name].teardown(client)
        for cmd in list(client.commands):
            if client.commands[cmd].__module__.lower() == module_name:
                del client.commands[cmd]
        del loaded_modules[module_name]
        logging.info("Module %s unloaded.", module_name)
        return f"✅ Module '{module_name}' unloaded successfully."
    except Exception as e:
        if module_name not in PROTECTED_MODULES:
            logging.error("Error unloading module %s: %s", module_name, e)
        return f"❌ Error unloading module '{module_name}': {e}"

def reload_module(module_name):
    module_name = module_name.lower()
    if module_name in PROTECTED_MODULES:
        logging.info("Protected module %s reload attempt ignored.", module_name)
        return f"✅ Module '{module_name}' is protected and cannot be reloaded."
    unload_result = unload_module(module_name)
    if "unloaded successfully" not in unload_result:
        return unload_result
    return load_module(module_name)

@client.on(events.NewMessage)
async def command_handler(event):
    logging.info("Received message: %s", event.raw_text)
    command_text = event.raw_text.strip()
    if not command_text:
        return
    parts = command_text.split()
    cmd_name = parts[0].lower()
    args = parts[1:]
    alias_cmd = get_alias(cmd_name)
    if alias_cmd:
        alias_parts = alias_cmd.split()
        cmd_name = alias_parts[0].lower()
        args = alias_parts[1:] + args
        logging.info("Alias used: %s -> %s", parts[0], alias_cmd)
    if cmd_name in client.commands:
        try:
            result = await client.commands[cmd_name](args, event)
            if event.raw_text != result:
                await event.edit(result)
            logging.info("Executed command: %s, result: %s", cmd_name, result)
        except Exception as e:
            if cmd_name not in PROTECTED_MODULES:
                logging.error("Error executing command %s: %s", cmd_name, e)
    else:
        await event.edit("❓ Unknown command. Type !help for a list of commands.")

if __name__ == '__main__':
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)
    for filename in os.listdir(MODULES_DIR):
        if filename.endswith('.py') and filename != '__init__.py':
            load_module(filename[:-3])
    logging.info("Werpyock Userbot started.")
    client.start()
    client.run_until_disconnected()