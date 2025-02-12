import sqlite3

commands = {}

def setup(client):
    commands['addalias'] = addalias_command
    commands['aliases'] = aliases_command
    commands['delalias'] = delalias_command
    commands['help'] = help_command
    commands['ping'] = ping_command

def init_db():
    conn = sqlite3.connect("werpyock_userbot.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS aliases (alias TEXT PRIMARY KEY, command TEXT NOT NULL)")
    conn.commit()
    return conn

async def addalias_command(args, event):
    if len(args) < 2:
        return "❗ Использование: <alias> <command>"
    alias = args[0].lower()
    command_text = " ".join(args[1:])
    conn = init_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO aliases (alias, command) VALUES (?, ?)", (alias, command_text))
        conn.commit()
        return f"✅ Алиас '{alias}' добавлен."
    except sqlite3.IntegrityError:
        return f"⚠️ Алиас '{alias}' уже существует."
    finally:
        conn.close()

async def aliases_command(args, event):
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT alias, command FROM aliases")
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "ℹ️ Нет алиасов."
    output = "📜 Список алиасов:\n"
    for alias, command_text in rows:
        output += f"- {alias} -> {command_text}\n"
    return output

async def delalias_command(args, event):
    if len(args) < 1:
        return "❗ Использование: <alias>"
    alias = args[0].lower()
    conn = init_db()
    c = conn.cursor()
    c.execute("DELETE FROM aliases WHERE alias = ?", (alias,))
    if c.rowcount == 0:
        output = f"⚠️ Алиас '{alias}' не найден."
    else:
        output = f"✅ Алиас '{alias}' удалён."
    conn.commit()
    conn.close()
    return output

async def help_command(args, event):
    output = "📜 Доступные команды:\n"
    for cmd in sorted(event.client.commands.keys()):
        output += f"- {cmd}\n"
    return output

async def ping_command(args, event):
    return "🏓 pong"
