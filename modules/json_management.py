import json
import asyncio


async def create_server_settings_file():
    try:
        open("guild_settings.json", "r")
    except FileNotFoundError:
        st = {'guilds': {}}
        await write_server_settings(st)
    await asyncio.sleep(0.1)


async def get_server_settings():
    await asyncio.sleep(0.1)
    with open("guild_settings.json", "r") as r:
        st = json.load(r)
        r.close()
        return st


async def write_server_settings(st):
    await asyncio.sleep(0.1)
    with open("guild_settings.json", "w+") as w:
        json.dump(st, w, indent=4)
        w.close()
    await asyncio.sleep(0.1)


async def get_guild_time_channel(guild_id):
    await asyncio.sleep(0.1)
    st = await get_server_settings()
    if st['guilds'][str(guild_id)].get("server_time_channel") is not None:
        return int(st['guilds'][str(guild_id)]['server_time_channel'])
    return None


async def get_prefix(guild_id):
    await asyncio.sleep(0.1)
    st = await get_server_settings()
    if st['guilds'][str(guild_id)].get("prefix") is not None:
        return st['guilds'][str(guild_id)]['prefix']
    else:
        return "!"
