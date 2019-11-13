# Name: loyaltybot.py
# Description: A bot that manages roles for users based on their time in the server
# Author: Colin Andress
# Date Created: 11/12/2019

import discord
import asyncio
from datetime import datetime

import modules.loyaltydatabase as db
db.create_tables()

# Discord bot token and other misc information
token = open("token.txt", "r").read()
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
    # Add them to the users database
    db.add_user(member.id, member.name, member.joined_at, member.guild)
    # Loop over all connected guilds
    for guild in client.guilds:
        # If the guild is the member's guild, send a welcome message to the system channel
        if guild == member.guild:
            await guild.system_channel.send(f"Welcome {member.name} to {guild.name}!")
            print(f"Sent a message to guild: {guild.name}")


@client.event
# When a member sends a message
async def on_message(message):
    # and the message is "{prefix}hello", send a welcome message
    name = message.author.name
    userid = message.author.id
    if message.content == prefix + "hello":
        await message.channel.send(f"Hello {name}!")
        print(f"Sent a message to guild: {message.guild.name}")
    elif message.content == prefix + "joined":
        joined = datetime.fromisoformat(str(message.author.joined_at))
        date = joined.strftime("%B %d, %Y")
        await message.channel.send(f"{name} joined on {date}")
    elif message.content == prefix + "join":
        db.add_user(userid, name, str(message.author.joined_at), message.guild.id)
        await message.channel.send(f"Added user with the following info: {userid, name, str(message.author.joined_at), message.guild.id}")
    elif message.content == prefix + "userinfo":
        await message.channel.send(f"DB Info:\n{db.get_username(userid)}\n{db.get_guild_id(userid)}\n{db.get_joined(userid)}\n{db.get_userid(db.get_username(userid))}")
    elif message.content == prefix + "roles":
        for role in message.guild.roles:
            roleid = role.id
            name = role.name
            permissions = role.permissions
            await message.channel.send(f"{name, roleid, permissions}")


def user_has_role(userid, rolename):
    for userrole in client.get_guild(db.get_guild_id(userid)).get_member(userid).roles:
        if userrole.name == rolename:
            return True
    return False


# Loop over all users and get their time as members
async def check_users():
    await client.wait_until_ready()
    await asyncio.sleep(1)
    while True:
        # get all userids and loop over them
        userids = db.get_all_userids()
        for userid in userids:
            # Get some user data and the guild
            userid = userid[0]
            username = db.get_username(userid)
            joined = datetime.fromisoformat(db.get_joined(userid))
            today = datetime.now()
            member_time = abs((today - joined).days)
            guild = client.get_guild(db.get_guild_id(userid))
            # If they are a member for one day
            if member_time == 1:
                # get the discord role "Default"
                discord_role = discord.utils.get(guild.roles, name="Default")
                # if it doesn't exist, make it
                if discord_role is None:
                    discord_role = await guild.create_role(name="Default", reason="Blank Bot Roles")
                # Check if the user doesn't already have the role
                if not user_has_role(userid, "Default"):
                    # and finally give the user the default role if they don't have it
                    await guild.get_member(userid).add_roles(discord_role)
                    print(f'Gave user: {username} the role "{discord_role.name}" in guild: "{guild.name}" '
                          f'for being a loyal member for {member_time} days!')
        # Run every three seconds
        await asyncio.sleep(3)

# Run the bot
client.loop.create_task(check_users())
client.run(token)
