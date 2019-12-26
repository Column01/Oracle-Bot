# DM Bot

A discord bot to manage Dungeon masters on your discord server


## Commands

**NOTE:** Replace `!` with the prefix you set in your server settings. If you forget your prefix, DM me on discord and I can reset it manually: `Column#2194`

### Help Command

- `!help [category]`

### Server Settings

- List server settings:
	- `!settings list`

- Set bot prefix:
	- `!settings prefix <prefix>`

- Set the server time channel:
	- `!settings servertime set <voice_channel_ID>`

- Remove the server time channel:
	- `!settings servertime remove`

- Add a loyalty role:
	- `!settings loyaltyroles add <role name> <days required>`

- Remove a loyalty role:
	- `!settings loyaltyroles remove <role name>`

### DM Management

- Create a DM:
	- `!dm create @user`

- Delete a DM:
	- `!dm delete @user`

- Allow roles for a DM to add to others:
	- `!dm allow @user @role1 @role2...`