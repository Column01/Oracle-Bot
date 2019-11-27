async def handle_help_command(message):
    command = message.content.split()
    if len(command) == 2:
        await message.channel.send(f"__**Help Categories:**__"
                                   f"```Settings"
                                   f"```")
