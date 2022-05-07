"""
Video + Music Stream Telegram Bot
Copyright (c) 2022-present levina=lab <https://github.com/levina-lab>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/licenses.html>
"""


import asyncio

from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_USERNAME,
    UPDATES_CHANNEL,
)

from program import __version__, LOGS
from pytgcalls import (__version__ as pytover)

from driver.filters import command
from driver.core import bot, me_bot, me_user
from driver.database.dbusers import add_served_user
from driver.database.dbchat import add_served_chat, is_served_chat
from driver.database.dblockchat import blacklisted_chats
from driver.database.dbpunish import is_gbanned_user
from driver.decorators import check_blacklist

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
@check_blacklist()
async def start_(c: Client, message: Message):
    user_id = message.from_user.id
    await add_served_user(user_id)
    await message.reply_photo(
        photo=f"{START_IMG}",
        caption=f"""ʜᴇʟʟᴏ 👋 ɪ ᴀᴍ ᴠᴇɴᴏᴍ sᴜᴘᴇʀ-ғᴀsᴛ ᴠᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ 🤖 ᴛᴏ ᴘʟᴀʏ ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ 🎸 ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘs ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.

┏━━━━━━━━━━━━━━━━━┓
┣★ ᴄʀᴇᴀᴛᴏʀ › : [ʀᴏᴍᴇᴏ xᴅ](https://t.me/Its_romeoo)
┣★ ᴜᴘᴅᴀᴛᴇs › : [sᴛʀᴀʏ ᴄᴏᴅᴇʀ](https://t.me/STRAY_CODER)
┣★ sᴜᴘᴘᴏʀᴛ › : [sᴛʀᴀʏ ᴄʜᴀᴛ](https://t.me/STRAY_CHAT_ROOM) 
┣★ ᴏғғɪᴄɪᴀʟ  › : [ɴᴇᴛᴡᴏʀᴋ](https://t.me/PHOENIX_EMPIRE) 
┣★ ʙʀᴏᴛʜᴇʀ › : [ᴄғᴄ ᴘʜᴏᴇɴɪx](https://t.me/PhoenixWarmed)
┗━━━━━━━━━━━━━━━━━┛

ᴜsᴇ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ !!"""
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("❓ᴄᴏᴍᴍᴀɴᴅs", callback_data="command_list")
                ],[
                    InlineKeyboardButton("📨 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton("📨 Updates", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],[
                    InlineKeyboardButton("✚ Add me to your Group", url=f"https://t.me/{me_bot.username}?startgroup=true")
                ],[
                    InlineKeyboardButton("🏳‍🌈 Basic Guide", callback_data="user_guide"),
                    InlineKeyboardButton("💡 About", callback_data="about_bot")
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@check_blacklist()
async def alive(c: Client, message: Message):
    chat_id = message.chat.id
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📨 Support", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "📨 Updates", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )
    text = f"**• Bot : `v{__version__}`\n• Pyrogram : `{pyrover}`\n• Python : `{__python_version__}`\n• PyTgCalls : `{pytover.__version__}`\n• Uptime : `{uptime}`**"
    await c.send_photo(
        chat_id,
        photo=f"https://telegra.ph/file/729082d25f6092cd51ef6.jpg",
        caption=text,
        reply_markup=buttons,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
@check_blacklist()
async def ping_pong(c: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("Server Connection Speed :-\n"  f"`{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@check_blacklist()
async def get_uptime(c: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"• Uptime: `{uptime}`\n"
        f"• Start Time: `{START_TIME_ISO}`"
    )


@Client.on_chat_join_request()
async def approve_join_chat(c: Client, m: ChatJoinRequest):
    if not m.from_user:
        return
    try:
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
    except FloodWait as e:
        await asyncio.sleep(e.x + 2)
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)


chat_watcher_group = 5

@Client.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message: Message):
    userid = message.from_user.id
    suspect = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.ban_member(userid)
        except ChatAdminRequired:
            LOGS.info(f"can't remove gbanned user from chat: {message.chat.id}")
            return
        await message.reply_text(
            f"👮🏼 (> {suspect} <)\n\n**Gbanned** user detected, that user has been gbanned by sudo user and was blocked from this Chat !\n\n🚫 **Reason:** potential spammer and abuser."
        )


@Client.on_message(command(["repo"]) & ~filters.edited)
async def help(client: Client, message: Message): 
    await message.reply_text(
        f"""`Click on the button to get the Source Code. If you have any inquiry regarding to this bot then kindly report in my Support Chat !!`""", 
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❰𝗦𝗼𝘂𝗿𝗰𝗲 𝗖𝗼𝗱𝗲❱", url=f"tg://need_update_for_some_feature")
                ]
            ]
        ),
    )


@Client.on_message(command(["start", "help"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/ae7b9fc91e49de4171faf.jpg",
        caption=f"""Thanks for adding me to your precious chat !! If you have any queries or facing any problem regarding me then report in our support group.""",
        reply_markup=InlineKeyboardMarkup(
                       [
                            [
                                InlineKeyboardButton("📨 U𝗉𝖽𝖺𝗍𝖾𝗌", url=f"https://t.me/{UPDATES_CHANNEL}"),
                                InlineKeyboardButton("S𝗎𝗉𝗉𝗈𝗋𝗍 📨", url=f"https://t.me/{GROUP_SUPPORT}")
                            ],
                        ]
                    )
                )
