import disnake
from disnake.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=disnake.Intents.default())

    async def on_ready(self):
        print(f'Бот успешно запущен!')

bot = Bot()

try:
    bot.load_extension('commands.message')
except Exception as e:
    print(e)

if __name__ == "__main__":
    bot.run("ТОКЕН НЕ ЗАБУДЬ ВСТАВИТЬ :)")