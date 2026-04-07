import discord
from src.config.settings import settings
from src.utils.logger import get_logger
from src.handlers.command_handler import handle_command

logger = get_logger(__name__)

def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True  # 이거 중요 (메시지 읽기)

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")

    @client.event
    async def on_message(message):
        if message.author.bot:
            return

        await handle_command(message)

    client.run(settings.discord_bot_token)