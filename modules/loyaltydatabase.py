# Name: loyaltydatabase.py
# Description: Manages LoyaltyBot's database
# Author: Colin Andress
# Date Created: 11/12/2019

import sqlite3

# Create and Connect to the users database
conn = sqlite3.connect("DMS.db")
c = conn.cursor()


def create_tables():
    # Create all the user info
    c.execute("CREATE TABLE IF NOT EXISTS dms(userid INT, allowedroles TEXT)")
    conn.commit()


def add_dm(userid):
    if not existing_dm(userid):
        c.execute("INSERT INTO dms (userid, allowedroles) VALUES (?, ?)", (userid, ""))
        conn.commit()
        return True
    else:
        return False


def add_allowed_roles(userid, roles):
    allowed_roles = get_allowed_roles(userid)
    added_roles = []
    if allowed_roles is not None:
        for role in roles:
            if has_allowed_role(userid, role):
                pass
            else:
                allowed_roles.append(role)
                added_roles.append(role)
        roles_str = ",".join(allowed_roles)
        if roles_str[0] == ",":
            roles_str = roles_str[1:]
        c.execute("UPDATE dms SET allowedroles = ? WHERE userid = ?", (roles_str, userid))
        conn.commit()
        return added_roles
    else:
        return False


def get_allowed_roles(userid):
    c.execute("SELECT allowedroles,userid FROM dms WHERE userid = ?", (userid,))
    fetch = c.fetchone()
    if fetch is not None:
        return fetch[0].split(",")
    return None


def has_allowed_role(userid, role):
    allowed_roles = get_allowed_roles(userid)
    for role1 in allowed_roles:
        if role1 == role:
            return True
    return False


def existing_dm(userid):
    c.execute("SELECT userid FROM dms WHERE userid = ?", (userid,))
    fetch = c.fetchone()
    if fetch is not None:
        return True
    return False
