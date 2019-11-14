# Name: loyaltybot.py
# Description: A bot that manages roles for users based on their time in the server
# Author: Colin Andress
# Date Created: 11/12/2019

import discord
import asyncio
from datetime import datetime

# Discord bot token and other misc information
token = open("token.txt", "r").read()
defaultperms = "join,hello"
prefix = "!"
status = "who's loyal, and who's not!"
client = discord.Client()


@client.event
# When the bot connects to discord
async def on_ready():
    botname = client.user.name
    print(f"{botname} connected to discord!")
    # Setting discord presence
    await client.change_presence(activity=discord.Activity(name=status, type=discord.ActivityType.watching))
    print(f"Setting discord presence to: Watching {status}")
    print(f"{botname} is apart of the following guilds:")
    for guild in client.guilds:
        num = client.guilds.index(guild) + 1
        print(f"\t{num}. {guild.name} (id: {guild.id})")


@client.event
# When a member joins a guild
async def on_member_join(member):
    # Loop over all connected guilds
    for guild in client.guilds:
        # If the guild is the member's guild, send a welcome message to the system channel
        if guild == member.guild:
            await guild.system_channel.send(f"Welcome {member.name} to {guild.name}!")


@client.event
# When a member sends a message
async def on_message(message):
    # and the message is "{prefix}hello", send a welcome message
    name = message.author.name
    userid = message.author.id
    if message.content == prefix + "role":
        pass


def user_has_role(guild, userid, roleid):
    user_roles = guild.get_member(userid).roles
    for role in user_roles:
        if role.id == roleid:
            return True
    return False


# Loop over all users and get their time as members
async def check_users():
    await client.wait_until_ready()
    await asyncio.sleep(1)
    while True:
        # Loop over every guild the bot is a part of
        for guild in client.guilds:
            # Loop over every member in that guild
            for member in guild.members:
                # get their joined time and convert it to datetime format
                joined = datetime.fromisoformat(str(member.joined_at))
                # get the current datetime format
                current = datetime.now()
                # subtract them to get the days they've been a member
                days = abs(current-joined).days
                if days < 1:
                    # check for a default role
                    default_role = discord.utils.get(guild.roles, name="Default")
                    # if it doesn't exist, make the role
                    if default_role is None:
                        discord_role = await guild.create_role(name="Default", reason="Blank Bot Role")
                    # if they don't have the defualt role, give it to them
                    if not user_has_role(guild, member.id, default_role.id):
                        await member.add_roles(default_role, reason="Playtime Requirements")
        # Run every three seconds
        await asyncio.sleep(3)

# Register my loop task and run the bot
client.loop.create_task(check_users())
client.run(token)
