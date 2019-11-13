# Name: loyaltydatabase.py
# Description: Manages LoyaltyBot's database
# Author: Colin Andress
# Date Created: 11/12/2019

import sqlite3

# Create and Connect to the users database
conn = sqlite3.connect("loyalusers.db")
c = conn.cursor()


def create_tables():
    # Create all the user info
    c.execute("CREATE TABLE IF NOT EXISTS users(userid INT, username TEXT, joined TEXT, guildid int, permissions BLOB)")
    conn.commit()


def add_user(userid, name, joined, guildid):
    c.execute("INSERT INTO users (userid, username, joined, guildid) VALUES (?, ?, ?, ?)",
              (userid, name, joined, guildid))
    conn.commit()


def get_all_userids():
    c.execute("SELECT userid FROM users")
    conn.commit()
    if c.fetchone() is not None:
        return c.fetchone()[0]
    else:
        print(f"Database has no users in it")


def get_username(userid):
    c.execute("SELECT username,userid FROM users WHERE userid = ?", (userid, ))
    conn.commit()
    if c.fetchone() is not None:
        return c.fetchone()[0]
    else:
        print(f"UserID: {userid} is not in the database")


def get_joined(userid):
    c.execute("SELECT joined,userid FROM users WHERE userid = ?", (userid, ))
    conn.commit()
    if c.fetchone() is not None:
        return c.fetchone()[0]
    else:
        print(f"UserID: {userid} is not in the database")


def get_userid(username):
    c.execute("SELECT userid,username FROM users WHERE username = ?", (username, ))
    conn.commit()
    if c.fetchone() is not None:
        return c.fetchone()[0]
    else:
        print(f"Username: {username} is not in the database")


def get_guild_id(userid):
    c.execute("SELECT guildid,userid FROM users WHERE userid = ?", (userid, ))
    conn.commit()
    if c.fetchone() is not None:
        return c.fetchone()[0]
    else:
        print(f"UserID: {userid} is not in the database")


def get_user_permissions(userid):
    c.execute("SELECT permissions,userid FROM users WHERE userid = ?", (userid, ))
    conn.commit()
    if c.fetchone() is not None:
        return c.fetchone()[0]
    else:
        print(f"UserID: {userid} is not in the database")
