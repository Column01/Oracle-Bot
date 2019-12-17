import discord


async def handle_help_command(message):
    help_command = message.content.split()
    if len(help_command) == 2 and help_command[1] == "help":
        embed = discord.Embed(title="Command Help", description="Use !loyaltybot help [category] to see more info",
                              color=0xff0000)
        embed.add_field(name="!loyaltybot help", value="This menu", inline=False)
        embed.add_field(name="Help Categories", value="Settings\nLoyalty", inline=False)
        embed.set_footer(text="Type !loyaltybot help [category]")
        await message.channel.send(embed=embed)
    elif len(help_command) == 3 and help_command[2].lower() == "settings":
        embed = discord.Embed(title="Settings Help", description="Use !loyaltybot help [category] to see more info",
                              color=0xff0000)
        embed.add_field(name="**!settings servertime set <channel ID>**",
                        value="\nSets the server time channel ID for your server"
                              "\n**Setup:** Create a voice channel, right click it and click `Copy ID`",
                        inline=False)
        embed.add_field(name="**!settings servertime remove**",
                        value="\nRemove the server time channel. Delete the channel afterwards to fully remove it.",
                        inline=False)
        embed.set_footer(text="Type !loyaltybot help [category]")
        await message.channel.send(embed=embed)
