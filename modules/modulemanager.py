commands = {}

def setup(client):
    commands['loadmod'] = loadmod_command
    commands['unloadmod'] = unloadmod_command
    commands['reloadmod'] = reloadmod_command

async def loadmod_command(args, event):
    if len(args) != 1:
        return "❗ Использование: !loadmod <module_name>"
    module_name = args[0].lower()
    result = event.client.load_module(module_name)
    return result

async def unloadmod_command(args, event):
    if len(args) != 1:
        return "❗ Использование: !unloadmod <module_name>"
    module_name = args[0].lower()
    result = event.client.unload_module(module_name)
    return result

async def reloadmod_command(args, event):
    if len(args) != 1:
        return "❗ Использование: !reloadmod <module_name>"
    module_name = args[0].lower()
    result = event.client.reload_module(module_name)
    return result
