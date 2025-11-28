import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("36280754"))
API_HASH = os.getenv("a81897f1a8b181ecef4b0a5b4aefafde")
BOT_TOKEN = os.getenv("7647872907:AAE4nO4k1THhOv7kGU2Eh32vKw-oKaAJ2qw")
SESSION = os.getenv("BQF1s6cAaNlw-BbbvdJlMv6J7vhAz6JEm8RSu1v14MDlFMRAHCh-5BRragzQCKztpT_j2PQKWOzgFAZLl_weU8HhABMKb03iH9npZHAJUbiYn1JA8mj6NZ9SZsq4uD8CLyh4kiXe1JALX3_Xb0xmkNHIhhwrThaCy9eFFcsKFUGTvJXRHZV16QZkVPI9VAlGY8qGfsY1QsqI821N7DxcfDuQ4IPH47jQfSe8wHb9udvJ5B9FMq9B3OFQYeujO4LZzG6EktoQZmiOJ-Xm8ia_dtUed_6REjd7qlrQZfKkcWDSzzP5v3-ligKSWlrOwWAriOifeIRG_KGOXwgRdZ-zEBECsdtMRQAAAAHUqEAcAA")

# Bot Client
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Assistant User Client
user = Client("assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

# Voice Chat Client
call = PyTgCalls(user)


# === DOWNLOAD SONG ===
def download_audio(query):
    try:
        opts = {
            "format": "bestaudio/best",
            "outtmpl": "song.mp3",
            "quiet": True
        }
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            return "song.mp3", info["entries"][0]["title"]
    except Exception as e:
        print("Error:", e)
        return None, None


# === COMMANDS ===
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("🔥 **Music Bot Online!**\nUse: `/play song name`")


@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("Gaana ka naam likh bhai…")

    query = " ".join(message.command[1:])
    msg = await message.reply(f"🔍 Searching **{query}** ...")

    file, title = download_audio(query)
    if not file:
        return await msg.edit("❌ Error downloading audio")

    chat_id = message.chat.id

    try:
        await call.join_group_call(
            chat_id,
            AudioPiped(file),
        )
        await msg.edit(f"🎶 Playing: **{title}**")
    except Exception as e:
        await msg.edit(f"❌ Error: `{e}`")


@app.on_message(filters.command("stop"))
async def stop(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("🛑 Music Stopped")


# === RUN ===
user.start()
call.start()
app.run()
