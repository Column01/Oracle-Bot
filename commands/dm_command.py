import asyncio
import modules.json_management as jm


async def handle_dm_command(message):
    command = message.content.split()
    if command[1] == "create":
        await create_dm_command(message, command)
    elif command[1] == "delete":
        await remove_dm_command(message, command)
    elif command[1] == "allow":
        await allow_dm_roles(message, command)
    elif command[1] == "remove":
        pass


async def create_dm_command(message, command):
    guild_id = str(message.guild.id)
    prefix = await jm.get_prefix(guild_id)
    usage = f"`{prefix}dm create @user`"
    if len(command) == 3:
        # Get the first mentioned user
        dm_to_add = message.mentions[0]
        # load the settings file from disk
        settings = await jm.get_server_settings()
        # create the DMs section if it doesn't exist
        if settings["guilds"][guild_id].get("dms") is None:
            settings["guilds"][guild_id]["dms"] = {}
        # Check if the DM exists, and if they don't, then create them
        if settings["guilds"][guild_id]["dms"].get(str(dm_to_add.id)) is None:
            settings["guilds"][guild_id]["dms"][dm_to_add.id] = []
            await jm.write_server_settings(settings)
            await message.channel.send(f"Added a new DM: `{dm_to_add.name}`. Welcome to the party!")
        else:
            await message.channel.send(f"That DM already exists. If you want to add roles for them to manage,"
                                       f" use the command:\n`{prefix}dm allow @user @role1 @role2...`")
    elif len(command) > 3:
        await asyncio.sleep(0.1)
        await message.channel.send(f"Too many arguments!\nUsage: {usage}")
    else:
        await asyncio.sleep(0.1)
        await message.channel.send(f"Something went wrong. Did you type the command correctly?\nUsage: {usage}")


async def remove_dm_command(message, command):
    guild_id = str(message.guild.id)
    prefix = await jm.get_prefix(guild_id)
    usage = f"`{prefix}dm delete @user`"
    if len(command) == 3:
        # Get the first mentioned user
        dm_to_remove = message.mentions[0]
        # load the settings file from disk
        settings = await jm.get_server_settings()
        # If they exist in the server settings, remove them
        if settings["guilds"][guild_id]["dms"].get(str(dm_to_remove.id)) is not None:
            settings["guilds"][guild_id]["dms"].pop(str(dm_to_remove.id))
            await jm.write_server_settings(settings)
            await message.channel.send(f"Removed the DM: `{dm_to_remove.name}` from the database successfully")
        # if they do not exist, tell the user that the user they tagged is not a DM
        else:
            await message.channel.send(f"Unable to remove DM: `{dm_to_remove.name}`. Are you sure they are a DM?")
    elif len(command) > 3:
        await asyncio.sleep(0.1)
        await message.channel.send(f"Too many arguments!\nUsage: {usage}")
    else:
        await asyncio.sleep(0.1)
        await message.channel.send(f"Something went wrong. Did you type the command correctly?\nUsage: {usage}")


async def allow_dm_roles(message, command):
    guild_id = str(message.guild.id)
    prefix = await jm.get_prefix(guild_id)
    usage = f"`{prefix}dm allow @user @role1 @roles2...`"
    if len(command) >= 4:
        target_dm = message.mentions[0]
        dm_user_id = str(target_dm.id)
        # Load the settings file
        settings = await jm.get_server_settings()
        if settings["guilds"][guild_id]["dms"].get(dm_user_id) is not None:
            # Get the DM's currently allowed roles
            allowed_dm_roles = settings["guilds"][guild_id]["dms"][dm_user_id]
            added_role_names = []
            # Loop over all roles mentioned
            for role in message.role_mentions:
                # If they are already allowed this role, pass over it.
                if await has_allowed_role(guild_id, dm_user_id, str(role.id)):
                    continue
                # If they do not have it already
                else:
                    # Add it to a list of roles we added and also add it to the DM's allowed roles.
                    added_role_names.append(role.name)
                    allowed_dm_roles.append(str(role.id))
                await asyncio.sleep(0.1)
            # Finally make the changes and write them to disk
            settings["guilds"][guild_id]["dms"][dm_user_id] = allowed_dm_roles
            if len(added_role_names) == 0:
                added_role_names = "None"
            else:
                added_role_names = ", ".join(added_role_names)
            await jm.write_server_settings(settings)
            await message.channel.send(f"Added the following roles to the tagged DM:"
                                       f"\n`{added_role_names}`")
        else:
            await asyncio.sleep(0.1)
            await message.channel.send(f"Unable to add roles to a DM that does not exist."
                                       f"\nCreate them as a DM using: `{prefix}dm create @user`")
    else:
        await asyncio.sleep(0.1)
        await message.channel.send(f"You must provide a DM and at least one role they are allowed to give to others."
                                   f"\nUsage: {usage}")


# Returns a boolean of whether they have this role in their allowed role settings
async def has_allowed_role(guild_id, dm_user_id, role_id):
    settings = await jm.get_server_settings()
    allowed_dm_roles = settings["guilds"][guild_id]["dms"][dm_user_id]
    for allowed_role in allowed_dm_roles:
        if allowed_role == role_id:
            return True
        await asyncio.sleep(0.1)
    return False
