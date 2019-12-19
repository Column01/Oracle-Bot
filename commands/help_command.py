import discord
import modules.json_management as jm


async def handle_help_command(message):
    help_command = message.content.split()
    prefix = await jm.get_prefix(str(message.guild.id))
    description = f"Use {prefix}loyaltybot help [category] to see more info"
    footer = f"Type {prefix}loyaltybot help [category]"
    if help_command[1] == "help":
        if len(help_command) == 2:
            embed = discord.Embed(title="Command Help", description=description,
                                  color=0xff0000)
            embed.add_field(name=f"__**{prefix}loyaltybot help**__", value="This menu", inline=False)
            embed.add_field(name="__**Help Categories**__", value="- Settings\n- Loyalty\n- DMs", inline=False)
            embed.set_footer(text=footer)
            await message.channel.send(embed=embed)
        elif len(help_command) == 3 and help_command[2].lower() == "settings":
            embed = discord.Embed(title="Settings Help", description=description,
                                  color=0xff0000)
            embed.add_field(name=f"__**{prefix}settings servertime set <channel ID>**__",
                            value="\nSets the server time channel ID for your server"
                                  "\n*Setup:* Create a voice channel, right click it and click `Copy ID` "
                                  "and then use it in the command above\n",
                            inline=False)
            embed.add_field(name=f"__**{prefix}settings servertime remove**__",
                            value="\nRemoves the server time channel. "
                                  "It should delete the channel afterwards to fully remove it",
                            inline=False)
            embed.set_footer(text=footer)
            await message.channel.send(embed=embed)
        elif len(help_command) == 3 and help_command[2].lower() == "loyalty":
            embed = discord.Embed(title="Loyalty Help", description=description,
                                  color=0xff0000)
            embed.add_field(name=f"__**{prefix}settings loyaltyroles add <Role Name> <Days Required>**__",
                            value="\nAdds the specified role (CaSe SeNsItIve) to the server config as a loyalty role."
                                  "\n*Setup:* Create a role (no spaces in the name allowed. Will fix later), "
                                  "run the above command with a days required value (whole numbers)\n",
                            inline=False)
            embed.add_field(name=f"__**{prefix}settings loyaltyroles remove <Role Name>**__",
                            value="\nRemoves the specified role (CaSe SeNsItIve) "
                                  "from the server config as a loyalty role.",
                            inline=False)
            embed.set_footer(text=footer)
            await message.channel.send(embed=embed)
        elif len(help_command) == 3 and help_command[2].lower() == "dms":
            embed = discord.Embed(title="DMs Help", description=description,
                                  color=0xff0000)
            embed.add_field(name=f"__**{prefix}dm create @user**__",
                            value="\nTurns the tagged user into a DM in the server settings.",
                            inline=False)
            embed.add_field(name=f"__**{prefix}dm allow @user @role1 @role2...**__",
                            value="\nAdds the tagged roles to a list of roles the tagged user can add to others. "
                                  f"You must make the user a DM first with `{prefix}dm create @user`",
                            inline=False)
            embed.add_field(name=f"__**{prefix}dm delete @user**__",
                            value="\nRemoves the tagged user from the server settings as a DM",
                            inline=False)
            embed.set_footer(text=footer)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(f"Unknown help command. Did you type it correctly?\n"
                                       f"Usage: {prefix}loyaltybot help [category]")
