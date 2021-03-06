# Copyright © 2019, Colin Andress. All Rights reserved
# Name: server_time.py
# Description: Updates the server time channel for each guild
# Author: Colin Andress

import asyncio
import discord
import logging
from aiohttp.client_exceptions import ClientConnectorError
from datetime import datetime
import pytz
import modules.json_management as jm

# Initializing a logger for connection errors.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="Oracle.log", encoding="utf-8", mode="w")
formatter = logging.Formatter("(%(asctime)s) [%(levelname)s] %(name)s %(message)s", "%d/%m/%y %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)


# Creates a category and channel for the server time in EST
async def set_server_time(client):
    await client.wait_until_ready()
    await asyncio.sleep(1)
    logger.info('Server Time module started. Server time channels should now be altered to the current time.')
    while True:
        try:
            # Get current EST time and format it
            t = datetime.now(pytz.timezone("US/Eastern"))
            formatted_time = datetime.strftime(t, "%m/%d/%y %H:%M EST")
            # For all guilds that the bot is connected to
            for guild in client.guilds:
                # Try and get the server time channel for the guild (set by the user)
                server_time_id = await jm.get_guild_time_channel(guild.id)
                server_time_channel = discord.utils.get(guild.voice_channels, id=server_time_id)
                # if the server time channel doesn't exist, or the channel name is already the current time,
                # then continue
                if server_time_channel is None or await _is_current_time(server_time_channel.name):
                    continue
                else:
                    # Edit the name to the new time and set the permissions to deny connecting users.
                    await server_time_channel.edit(name=formatted_time)
                    await server_time_channel.set_permissions(guild.default_role, connect=False)
            # Runs every second
            await asyncio.sleep(1)
        except ClientConnectorError as e:
            print(f"Error when setting servertime. Read exception below: \n{e}")
            logger.info(f"There was an exception when setting the server time. Read more below: \nException: {e}")


# checks the current time against the time passed to it and if they are the same, will return True
async def _is_current_time(t):
    await asyncio.sleep(0.1)
    # Get time and compare it to the given time.
    ti = datetime.now(pytz.timezone("US/Eastern"))
    ft = datetime.strftime(ti, "%m/%d/%y %H:%M EST")
    return t == ft
