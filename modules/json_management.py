# Copyright © 2019, Colin Andress. All Rights reserved
# Name: json_management.py
# Description: Manages the JSON storage for the servers
# Author: Colin Andress

import json
import asyncio


guild_storage = "guild_storage.json"


# Create the server settings file if it doesn't exist
async def create_server_settings_file():
    try:
        open(guild_storage, "r")
    except FileNotFoundError:
        st = {'guilds': {}}
        await write_server_settings(st)
    await asyncio.sleep(0.1)


# Load the server settings file
async def get_server_settings():
    await asyncio.sleep(0.1)
    with open(guild_storage, "r") as r:
        st = json.load(r)
        r.close()
        return st


# Write the changes to the server storage file.
async def write_server_settings(st):
    await asyncio.sleep(0.1)
    with open(guild_storage, "w+") as w:
        json.dump(st, w, indent=4)
        w.close()
    await asyncio.sleep(0.1)


# Returns the channel ID for the guild time channel. Returns None if there is not one set
async def get_guild_time_channel(guild_id):
    await asyncio.sleep(0.1)
    st = await get_server_settings()
    if await is_in_guilds_file(guild_id):
        if st['guilds'][str(guild_id)].get("server_time_channel") is not None:
            channel_id = int(st['guilds'][str(guild_id)]['server_time_channel'])
            if channel_id == 0:
                return None
            else:
                return int(st['guilds'][str(guild_id)]['server_time_channel'])
    return None


# Get the prefix for the guild in the config. If there is no prefix set, return an exclamation point
async def get_prefix(guild_id):
    await asyncio.sleep(0.1)
    st = await get_server_settings()
    if await is_in_guilds_file(guild_id):
        if st['guilds'][str(guild_id)].get("prefix") is not None:
            return st['guilds'][str(guild_id)]['prefix']
    return "o!"


async def is_in_guilds_file(guild_id):
    settings = await get_server_settings()
    if settings['guilds'].get(str(guild_id)) is None:
        return False
    else:
        return True
