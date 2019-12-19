import asyncio
import discord
import modules.json_management as jm


async def handle_settings_command(message):
    settings_command = message.content.split()
    # Get the current server settings file from disk
    server_settings = await jm.get_server_settings()
    guild = message.guild
    guild_id = str(message.guild.id)
    # if the guild is not in the server settings file, add it
    if server_settings["guilds"].get(guild_id) is None:
        server_settings["guilds"][guild_id] = {}
    # if it is the server time command
    if settings_command[1] == "servertime":
        if settings_command[2] == "set":
            await server_time_set(message, server_settings, guild_id, settings_command)
        elif settings_command[2] == "remove":
            await server_time_remove(message, server_settings, guild_id, guild, settings_command)
    # Loyalty role commands
    elif settings_command[1] == "loyaltyroles":
        # add loyalty role
        if settings_command[2] == "add":
            await loyalty_roles_add(message, server_settings, guild_id, settings_command, guild)
        # remove loyalty role
        elif settings_command[2] == "remove":
            await loyalty_roles_remove(message, server_settings, guild_id, settings_command, guild)
    # list server settings
    elif settings_command[1] == "list":
        await list_settings(message, server_settings, guild)
    elif settings_command[1] == "prefix":
        new_prefix = settings_command[2]
        await set_prefix(message, server_settings, guild_id, settings_command, new_prefix)


async def list_settings(message, settings, guild):
    guild_id = str(guild.id)
    roles_info = []
    index = 0
    await sort_loyalty_roles(settings, guild_id)
    if len(settings["guilds"][guild_id]["loyalty_roles"]) == 0:
        roles_info.append("None")
    else:
        for role_id in settings["guilds"][guild_id]["loyalty_roles"]:
            index += 1
            role = discord.utils.get(guild.roles, id=int(role_id))
            days = settings["guilds"][guild_id]["loyalty_roles"][role_id]
            if days == '1':
                roles_info.append(f"{index}. '{role.name}' with requirement of {days} day\n")
            else:
                roles_info.append(f"{index}. '{role.name}' with requirement of {days} days\n")
            await asyncio.sleep(0.1)
    roles_info = "".join(roles_info)
    server_time_id = await jm.get_guild_time_channel(str(guild.id))
    await message.channel.send(f"__**Current server settings:**__\n\n"
                               f"**Server time channel ID:** `{server_time_id}`\n\n"
                               f"**Loyalty Roles:**\n"
                               f"```\n"
                               f"{roles_info}"
                               f"```")


async def loyalty_roles_add(message, settings, guild_id, command, guild):
    prefix = await jm.get_prefix(guild_id)
    usage = f"Usage: `{prefix}settings loyaltyroles add <Role Name> <number of days>`"
    if len(command) == 5:
        # get the role and the days required
        role = discord.utils.get(guild.roles, name=command[3])
        if role is None:
            await message.channel.send(f"Cannot find role with name: {command[3]}. "
                                       f"Did you type it correctly?\nUsage: {usage}")
        days_req = command[4]
        if days_req < '1':
            await message.channel.send(f"You must provide a day requirement of 1 day or more.\n{usage}")
        # make the loyalty roles section if it doesn't exist already
        if settings["guilds"][guild_id].get("loyalty_roles") is None:
            settings["guilds"][guild_id]["loyalty_roles"] = {}
            # add the role to the settings and write the settings to disk
        # if the role is not already in the server settings, add it
        if settings["guilds"][guild_id]["loyalty_roles"].get(str(role.id)) is None:
            settings["guilds"][guild_id]["loyalty_roles"][role.id] = days_req
            await jm.write_server_settings(settings)
            await sort_loyalty_roles(settings, guild_id)
            await message.channel.send(f"Added role: `{role.name}` to list of loyalty roles "
                                       f"with a time requirement of `{days_req} days`.")
        else:
            await message.channel.send(f"The role `{role.name}` is already a loyalty roles. Type "
                                       f"`!settings list` to see existing loyalty roles")
    elif len(command) < 5:
        await asyncio.sleep(0.1)
        await message.channel.send(f"You must provide the number of days required to get this role."
                                   f"\nUsage: {usage}")
    else:
        await asyncio.sleep(0.1)
        await message.channel.send(f"Too many arguments!\nUsage: {usage}")


async def sort_loyalty_roles(settings, guild_id):
    # Sorts the loyalty roles in order from highest day's required to lowest
    sorted_dict = {}
    loyal_roles = settings["guilds"][guild_id]["loyalty_roles"]
    for key, value in sorted(loyal_roles.items(), key=lambda item: int(item[1]), reverse=True):
        sorted_dict[key] = value
    settings["guilds"][guild_id]["loyalty_roles"] = sorted_dict
    await jm.write_server_settings(settings)


async def loyalty_roles_remove(message, settings, guild_id, command, guild):
    prefix = await jm.get_prefix(guild_id)
    usage = f"Usage: `{prefix}settings loyaltyroles remove <Role Name>`"
    if len(command) == 4:
        # Fetch the role from discord
        role = discord.utils.get(guild.roles, name=command[3])
        if role is None:
            await message.channel.send(f"Cannot find role with name: {command[3]}. "
                                       f"Did you type it correctly?\n{usage}")
        # Remove the role from the loyalty roles
        settings["guilds"][guild_id]["loyalty_roles"].pop(str(role.id))
        # write changes
        await jm.write_server_settings(settings)
        await sort_loyalty_roles(settings, guild_id)
        await message.channel.send(f"Removed role: `{command[3]}` from server settings.")
    elif len(command) < 4:
        await asyncio.sleep(0.1)
        await message.channel.send(f"You must provide the role you want removed from the server config"
                                   f"\n{usage}")
    else:
        await asyncio.sleep(0.1)
        await message.channel.send(f"Too many arguments!\nUsage: {usage}`")


async def server_time_set(message, settings, guild_id, command):
    prefix = await jm.get_prefix(guild_id)
    usage = f"`{prefix}settings servertime set <channel ID>`"
    if len(command) == 4:
        channel_id = command[3]
        # set the channel id in the file
        settings["guilds"][guild_id]["server_time_channel"] = channel_id
        # write changes to disk
        await jm.write_server_settings(settings)
        await message.channel.send(f"Set server time channel to channel ID: `{channel_id}`")
    elif len(command) < 4:
        await message.channel.send("You must provide a channel ID for the server time channel."
                                   "\nCreate a voice channel, right click it and click `Copy ID`")
    else:
        await message.channel.send(f"Too many arguments!\nUsage: {usage}")


async def server_time_remove(message, settings, guild_id, guild, command):
    prefix = await jm.get_prefix(guild_id)
    usage = f"`{prefix}settings servertime remove`"
    channel_id = settings["guilds"][guild_id]["server_time_channel"]
    if len(command) == 3:
        # Try to get the channel from the id and delete it
        channel = discord.utils.get(guild.voice_channels, id=int(channel_id))
        if channel is not None:
            await channel.delete(reason="Removing server time channel")
        # Remove it from storage and write the changes
        settings["guilds"][guild_id].pop("server_time_channel")
        await jm.write_server_settings(settings)
        await message.channel.send("Removed server time channel from server settings and deleted the channel")
    elif len(command) > 3:
        await message.channel.send(f"Too many arguments!\nUsage: {usage}")


async def set_prefix(message, settings, guild_id, command, new_prefix):
    prefix = await jm.get_prefix(guild_id)
    usage = f"`{prefix}settings prefix <prefix>`"
    if len(command) == 3:
        settings["guilds"][guild_id]["prefix"] = new_prefix
        await jm.write_server_settings(settings)
        await message.channel.send(f"Changed the bot prefix to: `{new_prefix}`")
    if len(command) > 3:
        await message.channel.send(f"Too many arguments!\nUsage: {usage}")
