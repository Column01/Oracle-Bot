# Name: dmdatabase.py
# Description: Manages DMBot's database
# Author: Colin Andress
# Date Created: 11/12/2019

import sqlite3

# Create and Connect to the users database
conn = sqlite3.connect("DMS.db")
c = conn.cursor()


# Create the tables in the database.
def create_tables():
    c.execute("CREATE TABLE IF NOT EXISTS dms(userid INT, allowedroles TEXT)")
    conn.commit()


# Adds the user as a dm in the DB if they don't already exist
# Returns true if they were added to the DB
# Returns false if they already exist in the DB
def add_dm(userid):
    if not existing_dm(userid):
        c.execute("INSERT INTO dms (userid, allowedroles) VALUES (?, ?)", (userid, ""))
        conn.commit()
        return True
    else:
        return False


# Adds the roles to the list of roles the DM is allowed to add to others. 
# Returns the roles added if it succeeds (empty added roles means they already had all the roles)
# Returns False if it fails to find them in the DB
def add_allowed_roles(userid, roles):
    # Get a list of the DM's allowed roles
    allowed_roles = get_allowed_roles(userid)
    added_roles = []
    # If that list is not empty loop over it
    if allowed_roles is not None:
        for role in roles:
            # if the role is already allowed for that DM, continue
            if has_allowed_role(userid, role):
                continue
            # if the DM is not already allowed that role, then add it to the 
            # list of roles they are allowed and the roles that were added to the DM
            else:
                allowed_roles.append(role)
                added_roles.append(role)
        roles_str = ",".join(allowed_roles)
        # remove comma at start of roles and then update the DM's allowed roles in the DB
        if roles_str[0] == ",":
            roles_str = roles_str[1:]
        c.execute("UPDATE dms SET allowedroles = ? WHERE userid = ?", (roles_str, userid))
        conn.commit()
        return added_roles
    else:
        return False


# Returns the DM's roles they are allowed to add to others
# Returns none if the DM does not exist in the DB
def get_allowed_roles(userid):
    c.execute("SELECT allowedroles,userid FROM dms WHERE userid = ?", (userid,))
    fetch = c.fetchone()
    if fetch is not None:
        return fetch[0].split(",")
    return None


# Returns true if the DM has the role in their list of allowed roles they can add to others
# Returns false if they DM is not already allowed to add that role
def has_allowed_role(userid, role):
    allowed_roles = get_allowed_roles(userid)
    for role1 in allowed_roles:
        if role1 == role:
            return True
    return False


# Returns true if the DM exists in the database
# Returns false if they do not already exist in the database
def existing_dm(userid):
    c.execute("SELECT userid FROM dms WHERE userid = ?", (userid,))
    fetch = c.fetchone()
    if fetch is not None:
        return True
    return False
