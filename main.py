from pyrogram import Client, filters
from pytgcalls import PyTgCalls

app = Client(
    "music",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("Bot is running!")

app.run()
