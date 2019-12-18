import discord


async def handle_help_command(message):
    help_command = message.content.split()
    if help_command[1] == "help":
        if len(help_command) == 2:
            embed = discord.Embed(title="Command Help", description="Use !loyaltybot help [category] to see more info",
                                  color=0xff0000)
            embed.add_field(name="__**!loyaltybot help**__", value="This menu", inline=False)
            embed.add_field(name="__**Help Categories**__", value="Settings\nLoyalty", inline=False)
            embed.set_footer(text="Type !loyaltybot help [category]")
            await message.channel.send(embed=embed)
        elif len(help_command) == 3 and help_command[2].lower() == "settings":
            embed = discord.Embed(title="Settings Help", description="Use !loyaltybot help [category] to see more info",
                                  color=0xff0000)
            embed.add_field(name="__**!settings servertime set <channel ID>**__",
                            value="\nSets the server time channel ID for your server"
                                  "\n*Setup:* Create a voice channel, right click it and click `Copy ID` "
                                  "and then use it in the command above\n",
                            inline=False)
            embed.add_field(name="__**!settings servertime remove**__",
                            value="\nRemoves the server time channel. "
                                  "It should delete the channel afterwards to fully remove it",
                            inline=False)
            embed.set_footer(text="Type !loyaltybot help [category]")
            await message.channel.send(embed=embed)
        elif len(help_command) == 3 and help_command[2].lower() == "loyalty":
            embed = discord.Embed(title="Loyalty Help", description="Use !loyaltybot help [category] to see more info",
                                  color=0xff0000)
            embed.add_field(name="__**!settings loyaltyroles add <Role Name> <Days Required>**__",
                            value="\nAdds the specified role (CaSe SeNsItIve) to the server config as a loyalty role."
                                  "\n*Setup:* Create a role (no spaces in the name allowed. Will fix later), "
                                  "run the above command with a days required value (whole numbers)\n",
                            inline=False)
            embed.add_field(name="__**!settings loyaltyroles remove <Role Name>**__",
                            value="\nRemoves the specified role (CaSe SeNsItIve) "
                                  "from the server config as a loyalty role.",
                            inline=False)
            embed.set_footer(text="Type !loyaltybot help [category]")
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(f"Unknown help command. Did you type it correctly?\n"
                                       f"Usage: !loyaltybot help [category]")
