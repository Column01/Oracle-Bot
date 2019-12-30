# DM Bot

A discord bot to manage Dungeon masters on your discord server

## Commands

**NOTE:** Replace `o!` with the prefix you set in your server settings. If you forget your prefix, DM me on discord and I can reset it manually: `Column#2194` or kick and re-invite the bot (THIS WIPES SERVER SETTINGS!)

### Help Command

- `o!help [category]`

### Server Settings

- List server settings:
	- `o!settings list`

- Set bot prefix:
	- `o!settings prefix <prefix>`

- Set the server time channel:
	- `o!settings servertime set <voice_channel_ID>`

- Remove the server time channel:
	- `o!settings servertime remove`

- Add a loyalty role:
	- `o!settings loyaltyroles add @role <days required>`

- Remove a loyalty role:
	- `o!settings loyaltyroles remove @role`

### DM Management

- Create a DM:
	- `o!dm create @user`

- Delete a DM:
	- `o!dm delete @user`

- Allow roles for a DM to add to others:
	- `o!dm allow @user @role1 @role2...`