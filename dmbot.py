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


# Get discord bot token from disk and init other misc info
token = open("token.txt", "r").read()
prefix = "!"
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
            # Get the current server settings file from disk
            server_settings = await jm.get_server_settings()
            guild = message.guild
            guild_id = str(message.guild.id)
            # if the guild is not in the server settings file, add it
            if server_settings["guilds"].get(guild_id) is None:
                server_settings["guilds"][guild_id] = {}
            # if it is the server time command
            if command[1] == "servertime":
                usage = "`!settings servertime setchannel <channel ID>`"
                if command[2] == "setchannel":
                    if len(command) == 4:
                        channel_id = command[3]
                        # set the channel id in the file
                        server_settings["guilds"][guild_id]["server_time_channel"] = channel_id
                        # write changes to disk
                        await jm.write_server_settings(server_settings)
                        await message.channel.send(f"Set server time channel to channel ID: {channel_id}")
                    elif len(command) < 4:
                        await message.channel.send("You must provide a channel ID for the server time channel."
                                                   "\nCreate a voice channel, right click it and click `Copy ID`")
                    else:
                        await message.channel.send(f"Too many arguments!\n{usage}")
            # Loyalty role commands
            elif command[1] == "loyaltyroles":
                # add loyalty role
                if command[2] == "add":
                    usage = "Usage: `!settings loyaltyroles add <Role Name> <number of days>`"
                    if len(command) == 5:
                        # get the role and the days required
                        role = discord.utils.get(guild.roles, name=command[3])
                        if role is None:
                            await message.channel.send(f"Cannot find role with name: {command[3]}. "
                                                       f"Did you type it correctly?\n{usage}")
                        days_req = command[4]
                        if days_req < '1':
                            await message.channel.send(f"You must provide a day requirement of 1 day or more.\n{usage}")
                        # make the loyalty roles section if it doesn't exist already
                        if server_settings["guilds"][guild_id].get("loyalty_Roles") is None:
                            server_settings["guilds"][guild_id]["loyalty_roles"] = {}
                        # add the role to the settings and write the settings to disk
                        server_settings["guilds"][guild_id]["loyalty_roles"][role.id] = days_req
                        await jm.write_server_settings(server_settings)
                        await message.channel.send(f"Added role: `{role.name}` to list of loyalty roles "
                                                   f"with a time requirement of `{days_req} days`.")
                    elif len(command) < 5:
                        await message.channel.send(f"You must provide the number of days required to get this role."
                                                   f"\n{usage}")
                    else:
                        await message.channel.send(f"Too many arguments!\n{usage}")
                # remove loyalty role
                elif command[2] == "remove":
                    usage = "Usage: `!settings loyaltyroles remove <Role Name>`"
                    if len(command) == 4:
                        # Fetch the role from discord
                        role = discord.utils.get(guild.roles, name=command[3])
                        if role is None:
                            await message.channel.send(f"Cannot find role with name: {command[3]}. "
                                                       f"Did you type it correctly?\n{usage}")
                        # Remove the role from the loyalty roles
                        server_settings["guilds"][guild_id]["loyalty_roles"].pop(str(role.id))
                        # write changes
                        await jm.write_server_settings(server_settings)
                        await message.channel.send(f"Removed role: `{command[3]}` from server settings.")
                    elif len(command) < 4:
                        await message.channel.send(f"You must provide the role you want removed from the server config"
                                                   f"\n{usage}")
                    else:
                        await message.channel.send(f"Too many arguments!\n{usage}`")
            # list server settings
            elif command[1] == "list":
                roles_info = []
                index = 0
                if len(server_settings["guilds"][guild_id]["loyalty_roles"]) == 0:
                    roles_info.append("None")
                else:
                    for role_id in server_settings["guilds"][guild_id]["loyalty_roles"]:
                        index += 1
                        role = discord.utils.get(guild.roles, id=int(role_id))
                        days = server_settings["guilds"][guild_id]["loyalty_roles"][role_id]
                        if days == '1':
                            roles_info.append(f"{index}. '{role.name}' with requirement of {days} day\n")
                        else:
                            roles_info.append(f"{index}. '{role.name}' with requirement of {days} days\n")
                roles_info = "".join(roles_info)
                server_time_id = await jm.get_guild_time_channel(str(guild.id))
                await message.channel.send(f"__**Current server settings:**__\n\n"
                                           f"**Server time channel ID:** `{server_time_id}`\n\n"
                                           f"**Loyalty Roles:**\n"
                                           f"```\n"
                                           f"{roles_info}"
                                           f"```")
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
