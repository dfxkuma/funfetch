import discord
from discord.ext import commands
from funfetch import Server


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.server = Server()

    async def on_ready(self):
        print("Bot is ready.")


my_bot = MyBot(command_prefix="!", intents=discord.Intents.all())


@my_bot.server.use()
async def get_member_count(guild_id):
    guild = my_bot.get_guild(guild_id)

    return guild.member_count


if __name__ == "__main__":
    my_bot.run("TOKEN")
