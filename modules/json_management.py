import json


def create_server_settings_file():
    try:
        open("guild_settings.json", "r")
    except FileNotFoundError:
        st = {'guilds': {}}
        print(st)
        write_server_settings(st)


def get_server_settings():
    with open("guild_settings.json", "r") as r:
        st = json.load(r)
        r.close()
        return st


def write_server_settings(st):
    with open("guild_settings.json", "w+") as w:
        json.dump(st, w, indent=4)
        w.close()


def get_guild_time_channel(guild_id):
    st = get_server_settings()
    if st['guilds'][str(guild_id)].get("server_time_channel") is not None:
        return int(st['guilds'][str(guild_id)]['server_time_channel'])
    return None
