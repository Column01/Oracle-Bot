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
    c.execute("CREATE TABLE IF NOT EXISTS users(userid INT, username TEXT, joined TEXT, guildid int, permissions TEXT)")
    conn.commit()


def add_user(userid, name, joined, guildid, permissions):
    c.execute("INSERT INTO users (userid, username, joined, guildid, permissions) VALUES (?, ?, ?, ?, ?)",
              (userid, name, joined, guildid, permissions))
    conn.commit()


def add_user_permission(userid, permission):
    userperms = get_user_permissions(userid)
    if user_has_permission(userid, permission) or userperms is None:
        return False
    else:
        userperms.append(permission)
        userperms = ",".join(userperms)
        c.execute("UPDATE users SET permissions = ? WHERE userid = ?", (userperms, userid))
        conn.commit()
        return True


def user_has_permission(userid, permission):
    userperms = get_user_permissions(userid)
    for userperm in userperms:
        if userperm == permission:
            return True
    return False


def get_all_userids():
    c.execute("SELECT userid FROM users")
    return c.fetchall()


def get_username(userid):
    c.execute("SELECT username,userid FROM users WHERE userid = ?", (userid, ))
    fetch = c.fetchone()
    if fetch is not None:
        return fetch[0]
    return None


def get_joined(userid):
    c.execute("SELECT joined,userid FROM users WHERE userid = ?", (userid, ))
    fetch = c.fetchone()
    if fetch is not None:
        return fetch[0]
    return None


def get_userid(username):
    c.execute("SELECT userid,username FROM users WHERE username = ?", (username, ))
    fetch = c.fetchone()
    if fetch is not None:
        return fetch[0]
    return None


def get_guild_id(userid):
    c.execute("SELECT guildid,userid FROM users WHERE userid = ?", (userid, ))
    fetch = c.fetchone()
    if fetch is not None:
        return fetch[0]
    return None


def get_user_permissions(userid):
    c.execute("SELECT permissions,userid FROM users WHERE userid = ?", (userid, ))
    fetch = c.fetchone()
    if fetch is not None:
        return fetch[0].split(",")
    return None

