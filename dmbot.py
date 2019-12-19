# Name: dmbot.py
# Description: A bot that manages DM's and their players for discord servers (designed for one server ATM)
# Author: Colin Andress
# Date Created: 11/12/2019

import discord
import asyncio
import modules.json_management as jm
import modules.loyal_users as lu
import modules.server_time as st
import commands.settings_command as scmd
import commands.help_command as helpcmd
import commands.dm_command as dmcmd


# Get discord bot token from disk and init other misc info
token = open("token.txt", "r").read()
status = "who's loyal, and who's not!"

client = discord.Client()


@client.event
# When the bot connects to discord
async def on_ready():
    # Create the database and the tables in it.
    # Create server times file
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
        if command[0] == f"{prefix}dm":
            await dmcmd.handle_dm_command(message)
        # Server time Command
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


# Register my loop tasks and run the bot
client.loop.create_task(lu.check_loyal_users(client))
client.loop.create_task(st.set_server_time(client))
client.run(token)
