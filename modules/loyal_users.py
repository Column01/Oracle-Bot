# Copyright © 2019, Colin Andress. All Rights reserved
# Name: loyal_users.py
# Description: Script to check loyal user's playtimes and give them loyalty roles
# Author: Colin Andress

from datetime import datetime
import discord
import asyncio
import modules.json_management as jm


# Loop over all users and get their time as members
async def check_loyal_users(client):
    await client.wait_until_ready()
    await asyncio.sleep(1)
    while True:
        # Loop over every guild the bot is a part of
        for guild in client.guilds:
            guild_id = str(guild.id)
            settings = await jm.get_server_settings()
            if settings["guilds"].get(guild_id) is not None:
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
                    # Get the server settings file and then get the loyalty roles for the server
                    loyalty_roles = settings["guilds"][guild_id]["loyalty_roles"]
                    # Loop over all loyalty roles
                    for role_id in loyalty_roles:
                        role_days = int(loyalty_roles[role_id])
                        # If the user has been a member long enough for the role
                        if days >= role_days:
                            # Get the index of the next loyalty role in the storage
                            # (the old role) and then get the role ID
                            next_index = list(loyalty_roles.keys()).index(role_id) + 1
                            old_role_id = list(loyalty_roles.keys())[next_index]
                            # get the new role and the old role from discord
                            role = discord.utils.get(guild.roles, id=int(role_id))
                            old_role = discord.utils.get(guild.roles, id=int(old_role_id))
                            # if the new role exists on discord
                            if role is not None:
                                # and they don't already have it
                                if not await user_has_role(guild, member.id, int(role_id)):
                                    # Add the new role and remove the old one
                                    if old_role is not None:
                                        await member.remove_roles(old_role)
                                    await member.add_roles(role, reason="Playtime Requirements")
                            # break so we don't keep adding roles
                            break
            else:
                # guild is not in settings file.
                continue
        # Run every three seconds
        await asyncio.sleep(3)


# Returns True if the user has the role, and returns false if they don't have the role
async def user_has_role(guild, userid, roleid):
    user_roles = guild.get_member(userid).roles
    for role in user_roles:
        if role.id == roleid:
            return True
        await asyncio.sleep(0.1)
    return False
