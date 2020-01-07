# Copyright © 2019, Colin Andress. All Rights reserved
# Name: oracle.py
# Description: A bot that manages groups for discord servers
# Author: Colin Andress

import re
import discord
import asyncio
import os
import logging
import modules.json_management as jm
import modules.loyal_users as loyalty
import modules.server_time as server_time
import commands.settings_command as settings_cmd
import commands.help_command as help_cmd
import commands.dm_command as dm_cmd


# Get discord bot token from disk and make a status
token_path = os.getcwd() + "/token.txt"
token = open(token_path, "r").read().strip("\n")
status = "over you. Oracle knows all"

# Initialize a logger (trying to track down a seemingly random SSL error.)
logger = logging.getLogger("discord")
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename="Oracle Log.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(levelname)s at %(asctime) from %(name)s %(message)s"))
logger.addHandler(handler)

# Init Discord client
client = discord.Client()


@client.event
# When the bot connects to discord
async def on_ready():
    # Create guild storage file
    await jm.create_server_settings_file()
    bot_name = client.user.name
    print(f"{bot_name} connected to discord!")
    # Setting discord presence
    await client.change_presence(activity=discord.Activity(name=status, type=discord.ActivityType.watching))
    print(f"Setting discord presence to: Watching {status}")
    print(f"{bot_name} is apart of the following guilds:")
    for guild in client.guilds:
        num = client.guilds.index(guild) + 1
        print(f"\t{num}. {guild.name} (id: {guild.id})")
        await asyncio.sleep(0.1)


@client.event
# When a member joins a guild
async def on_member_join(member):
    # Loop over all connected guilds
    for guild in client.guilds:
        # If the guild is the member's guild, send a welcome message to the system channel
        if guild == member.guild:
            if guild.system_channel is not None:
                await guild.system_channel.send(f"Welcome {member.name} to {guild.name}!")
        await asyncio.sleep(0.1)


@client.event
# When a member sends a message
async def on_message(message):
    author = message.author
    prefix = await jm.get_prefix(str(message.guild.id))
    # If the message is from a bot or contains an embed, ignore it.
    if author == client.user or len(message.embeds) > 0 or author.bot:
        return
    # split the message contents so we have a command array with arguments
    command = message.content.split()
    # Check if the message starts with the guild's prefix, if not, ignore it
    if re.match(f"{prefix}", command[0]):
        # DM command (ADMIN PERMS REQUIRED)
        if command[0] == f"{prefix}dm":
            # If they are not an admin, tell them to bugger off.
            if author_is_admin(author):
                await dm_cmd.handle_dm_command(message)
            else:
                await message.channel.send(f"I'm sorry, {author.name}, but you must be an admin to use the command.")
        # Settings command (ADMIN PERMS REQUIRED)
        elif command[0] == f"{prefix}settings":
            # If they are not an admin, tell them to bugger off.
            if author_is_admin(author):
                await settings_cmd.handle_settings_command(message)
            else:
                await message.channel.send(f"I'm sorry, {author.name}, but you must be an admin to use the command.")
        # Help command
        elif command[0] == f"{prefix}help":
            await help_cmd.handle_help_command(message)
        else:
            unknown_command = " ".join(command)
            await message.channel.send(f"Unknown command: `{unknown_command}`. Did you type it correctly?")


@client.event
# Handles when the bot is removed from a guild
async def on_guild_remove(guild):
    guild_id = str(guild.id)
    # Remove the guild from storage to make sure we don't store data we no longer need.
    settings = await jm.get_server_settings()
    settings["guilds"].pop(guild_id)
    await jm.write_server_settings(settings)
    print(f"The guild: {guild.name} removed the bot from the guild. We are sad to see them go, "
          f"but we know we are better off without them!")
    await asyncio.sleep(0.1)


@client.event
async def on_guild_join(guild):
    await create_guild_section(guild)
    print(f"Oracle was added to a new guild: {guild.name}. "
          f"I created a new entry in the server file for them :D")
    await asyncio.sleep(0.1)


async def create_guild_section(guild):
    guild_id = str(guild.id)
    settings = await jm.get_server_settings()
    if settings["guilds"].get(guild_id) is None:
        settings["guilds"][guild_id] = {}
        settings["guilds"][guild_id]["loyalty_roles"] = {}
        settings["guilds"][guild_id]["server_time_channel"] = 0
        settings["guilds"][guild_id]["dms"] = {}
        await jm.write_server_settings(settings)


def author_is_admin(author):
    return author.guild_permissions.administrator


# Register my loop tasks and run the bot
client.loop.create_task(loyalty.check_loyal_users(client))
client.loop.create_task(server_time.set_server_time(client))
client.run(token)
