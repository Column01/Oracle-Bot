# Name: dmbot.py
# Description: A bot that manages DM's and their players for discord servers (designed for one server ATM)
# Author: Colin Andress
# Date Created: 11/12/2019

import discord
import asyncio
import pytz
from datetime import datetime
import modules.dmdatabase as db
import modules.json_management as jm
import commands.settings_command as scmd
import commands.help_command as help


# Get discord bot token from disk and init other misc info
token = open("token.txt", "r").read()
status = "who's loyal, and who's not!"

client = discord.Client()


@client.event
# When the bot connects to discord
async def on_ready():
    # Create the database and the tables in it.
    await db.create_tables()
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
    command = message.content.split()
    # If the message author is an administrator
    if message.author.guild_permissions.administrator:
        # split the message contents so we have a command array with arguments
        # if the first item is the "dm" command
        if command[0] == f"{prefix}dm":
            # and if the second item is "create"
            if command[1] == "create":
                # loop over the message mentions and add each mention to the database
                for dm in message.mentions:
                    try_add_dm = await db.add_dm(dm.id)
                    added_roles = []
                    # loop over the roles that were mentioned in the message and add them to each DM
                    for role in message.role_mentions:
                        await dm.add_roles(role)
                        added_roles.append(role.name)
                    added_roles = ", ".join(added_roles)
                    # if adding the DM worked, reply with a message
                    if try_add_dm:
                        await message.channel.send(f"Added the DM: `{dm.name}` to the database "
                                                   f"and assigned them the role(s): `{added_roles}`")
                    # if adding the dm failed, message the channel with a list of the roles the DM is allowed to add
                    else:
                        allowed_roles = await db.get_allowed_roles(dm.id)
                        role_names = []
                        for roleid in allowed_roles:
                            role_names.append(message.guild.get_role(int(roleid)).name)
                        if allowed_roles is not None:
                            role_names = ", ".join(role_names)
                            await message.channel.send(f"`{dm.name}` is already a DM "
                                                       f"and is allowed to give the following roles:\n `{role_names}`")
            # if the second item is "allow"
            if command[1] == "allow":
                # loop over message mentions
                for dm in message.mentions:
                    role_ids = []
                    role_names = []
                    # loop over each role that was mentioned and add it to two different arrays
                    # (one with the IDS and one with the names)
                    for role in message.role_mentions:
                        role_ids.append(str(role.id))
                        role_names.append(role.name)
                    # try to add the allowed roles to the DM that was mentioned in the message
                    try_add_roles = await db.add_allowed_roles(dm.id, role_ids)
                    role_names = ", ".join(role_names)
                    # if adding failed, message the channel asking if they made the DM
                    if try_add_roles is False:
                        await message.channel.send(f"Failed to add roles to the DM: `{dm.name}`. "
                                                   f"\nDid you make them a DM using '!dm create'?")
                    # if it returned anything else
                    else:
                        # and the length of the returned data is not zero, the roles were added.
                        if len(try_add_roles) != 0:
                            try_add_roles = ", ".join(try_add_roles)
                            await message.channel.send(f"Added the roles: `{try_add_roles}` to the DM: `{dm.name}`")
                        # if there is nothing in try_add_roles, that means it the DM is allowed to add these roles.
                        else:
                            await message.channel.send(f"`{dm.name}` already has roles: `{role_names}`")
        # Server time Command
        elif command[0] == f"{prefix}settings":
            await scmd.handle_settings_command(message)
        elif command[0] == f"{prefix}loyaltybot":
            if command[1] == "help":
                await help.handle_help_command(message)
        else:
            if message.startswith(prefix):
                await message.channel.send(f"Unknown command: {command}. Did you type it correctly?")
    else:
        await message.channel.send("You must be an admin to use commands for Loyalty Bot!")


# Returns True if the user has the role, and returns false if they don't have the role
async def user_has_role(guild, userid, roleid):
    user_roles = guild.get_member(userid).roles
    for role in user_roles:
        if role.id == roleid:
            return True
        await asyncio.sleep(0.1)
    return False


# checks the current time against the time passed to it and if they are the same, will return True
async def is_current_time(t):
    await asyncio.sleep(0.1)
    # Get time and compare it to the given time.
    ti = datetime.now(pytz.timezone("US/Eastern"))
    ft = datetime.strftime(ti, "%m/%d/%y %H:%M EST")
    return t == ft


# Loop over all users and get their time as members
async def check_users():
    await client.wait_until_ready()
    await asyncio.sleep(1)
    while True:
        # Loop over every guild the bot is a part of
        for guild in client.guilds:
            # Loop over every member in that guild
            for member in guild.members:
                # ignore bots
                if member.bot:
                    continue
                # get their joined time and convert it to datetime format
                joined = datetime.fromisoformat(str(member.joined_at))
                # get the current datetime format
                current = datetime.now()
                # subtract them to get the days they've been a member
                days = abs(current-joined).days
                if days >= 1:
                    # check for a default role
                    default_role = discord.utils.get(guild.roles, name="Default")
                    # if it doesn't exist, make the role
                    if default_role is None:
                        default_role = await guild.create_role(name="Default", reason="Blank Bot Role")
                        print(f"Creating default role for {guild.name}")
                    # if they don't have the default role, give it to them
                    if not await user_has_role(guild, member.id, default_role.id):
                        print(f"{member.name} in {guild.name} does not have default role. Adding to user")
                        await member.add_roles(default_role, reason="Playtime Requirements")
        # Run every three seconds
        await asyncio.sleep(3)


# Creates a category and channel for the server time in EST
async def set_server_time():
    await client.wait_until_ready()
    await asyncio.sleep(1)
    while True:
        # Get current EST time and format it
        t = datetime.now(pytz.timezone("US/Eastern"))
        formatted_time = datetime.strftime(t, "%m/%d/%y %H:%M EST")
        # For all guilds that the bot is connected to
        for guild in client.guilds:
            # Set some overwrites to prevent joining of the Voice channel (all roles are blacklisted)
            overwrites = {}
            for role in guild.roles:
                overwrites[role] = discord.PermissionOverwrite(connect=False)
            # Try and get the server time channel for the guild (set by the user)
            server_time_id = await jm.get_guild_time_channel(guild.id)
            server_time_channel = discord.utils.get(guild.voice_channels, id=server_time_id)
            # if the server time channel doesn't exist, or the channel name is already the current time, then continue
            if server_time_channel is None or await is_current_time(server_time_channel.name):
                continue
            else:
                # edit the name to the new time and set the overwrites again
                await server_time_channel.edit(name=formatted_time, overwrites=overwrites)
        # Runs every second
        await asyncio.sleep(1)


# Register my loop tasks and run the bot
client.loop.create_task(check_users())
client.loop.create_task(set_server_time())
client.run(token)
