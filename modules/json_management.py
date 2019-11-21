import json


def create_server_times_file():
    try:
        open("server_times.json", "r")
    except FileNotFoundError:
        st = {'guilds': {}}
        print(st)
        write_server_times(st)


def get_server_times():
    with open("server_times.json", "r") as r:
        st = json.load(r)
        r.close()
        return st


def write_server_times(st):
    with open("server_times.json", "w+") as w:
        json.dump(st, w, indent=4)
        w.close()


def get_guild_time_channel(guild_id):
    st = get_server_times()
    return int(st['guilds'][str(guild_id)]['channel_id'])
