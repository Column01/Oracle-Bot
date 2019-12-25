# Copyright © 2019, Colin Andress. All Rights reserved
# Name: dmbot.py
# Description: A bot that manages DM's and their players for discord servers
# Author: Colin Andress

import discord
import asyncio
import modules.json_management as jm
import modules.loyal_users as lu
import modules.server_time as st
import commands.settings_command as scmd
import commands.help_command as helpcmd
import commands.dm_command as dmcmd


# Get discord bot token from disk and init other misc info
token = open("token.txt", "r").read().strip("\n")
status = "who's loyal, and who's not!"

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
            await guild.system_channel.send(f"Welcome {member.name} to {guild.name}!")
        await asyncio.sleep(0.1)


@client.event
# When a member sends a message
async def on_message(message):
    prefix = await jm.get_prefix(str(message.guild.id))
    # If the message is from the bot or contains and embed, ignore it.
    if message.author == client.user or len(message.embeds) > 0:
        return
    # If the message author is an administrator
    if message.author.guild_permissions.administrator:
        # split the message contents so we have a command array with arguments
        command = message.content.split()
        # handle the commands
        if command[0] == f"{prefix}dm":
            await dmcmd.handle_dm_command(message)
        elif command[0] == f"{prefix}settings":
            await scmd.handle_settings_command(message)
        elif command[0] == f"{prefix}loyaltybot":
            if command[1] == "help":
                await helpcmd.handle_help_command(message)
        else:
            unknown_command = " ".join(command)
            if unknown_command[:1] == prefix:
                await message.channel.send(f"Unknown command: `{unknown_command}`. Did you type it correctly?")
    else:
        await message.channel.send("You must be an admin to use commands for Loyalty Bot!")


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
    guild_id = str(guild.id)
    settings = await jm.get_server_settings()
    settings["guilds"][guild_id] = {}
    await jm.write_server_settings(settings)
    print(f"Oracle was added to a new guild: {guild.name}. "
          f"I created a new entry in the server file for them :D")
    await asyncio.sleep(0.1)


# Register my loop tasks and run the bot
client.loop.create_task(lu.check_loyal_users(client))
client.loop.create_task(st.set_server_time(client))
client.run(token)
