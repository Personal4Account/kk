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
        photo=f"https://telegra.ph//file/d018eb81849c32d3cf8e4.jpg",
        caption=f"""**𝖨 𝖺𝗆 𝖲𝗎𝗉𝖾𝗋𝖥𝖺𝗌𝗍 𝗉𝗅𝖺𝗒𝖾𝗋 𝗍𝗈 𝗉𝗅𝖺𝗒 𝗆𝗎𝗌𝗂𝖼 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉𝗌 𝗏𝗈𝗂𝖼𝖾 𝖼𝗁𝖺𝗍. 

𝖯𝗈𝗐𝖾𝗋𝖾𝖽 𝖻𝗒 𝖲𝗉𝗈𝗍𝗂𝖿𝗒™**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕𝖢𝗅𝗂𝖼𝗄 𝖧𝖾𝗋𝖾 𝖳𝗈 𝖠𝖽𝖽 𝖬𝖾➕", url=f"https://t.me/{me_bot.username}?startgroup=true")
                ],
                 [
                    InlineKeyboardButton("❓𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌", callback_data="command_list")
                ],[
                    InlineKeyboardButton("📢 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url=f"https://t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton("𝖴𝗉𝖽𝖺𝗍𝖾𝗌 📡", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],[
                    InlineKeyboardButton("𝖮𝗐𝗇𝖾𝗋'𝗑𝖣 🚩", url="https://t.me/Its_romeoo")
                ],
            ]
        ),
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
                InlineKeyboardButton("❰𝗦𝘂𝗽𝗽𝗼𝗿𝘁❱", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "❰𝗨𝗽𝗱𝗮𝘁𝗲𝘀❱", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )
    text = f"**𝗛𝗲𝘆𝘆 {message.from_user.mention()}, I'm {me_bot.first_name}**\n\n🧑🏼‍💻 My Master: [{ALIVE_NAME}](https://t.me/{OWNER_USERNAME})\n👾 Bot Version: `v{__version__}`\n🔥 Pyrogram Version: `{pyrover}`\n🐍 Python Version: `{__python_version__}`\n✨ PyTgCalls Version: `{pytover.__version__}`\n🆙 Uptime Status: `{uptime}`\n\n **𝗧𝗵𝗶𝘀 𝗕𝗼𝘁 𝗜𝘀 𝗗𝗲𝘀𝗶𝗴𝗻𝗲𝗱 𝗕𝘆 𝗨𝘀𝗶𝗻𝗴 𝗣𝘆𝘁𝗵𝗼𝗻 𝗕𝘆 #𝙊𝙥_𝙍𝙤𝙢𝙚𝙤**"
    await c.send_photo(
        chat_id,
        photo=f"{ALIVE_IMG}",
        caption=text,
        reply_markup=buttons,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
@check_blacklist()
async def ping_pong(c: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("× 𝐈 𝖺𝗆 𝐀𝗅𝗂𝗏𝖾 !! 𝗟𝖾𝗍𝗌 𝗙𝗎𝖼𝗄 𝗧𝗁𝖾 𝘃𝗰.")


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


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    chat_id = m.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    for member in m.new_chat_members:
        try:
            if member.id == me_bot.id:
                if chat_id in await blacklisted_chats():
                    await m.reply_text(
                        "❗️ This chat has blacklisted by sudo user and You're not allowed to use me in this chat."
                    )
                    return await bot.leave_chat(chat_id)
            if member.id == me_bot.id:
                return await m.reply(
                    "𝖳𝗁𝗇𝗑 𝖿𝗈𝗋 𝖺𝖽𝖽𝗂𝗇𝗀 𝗆𝖾 𝗁𝖾𝗋𝖾 , 𝖭𝗈𝗐 𝗆𝖺𝗄𝖾 𝗆𝖾 𝖺𝖽𝗆𝗂𝗇 𝗈𝖿 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝗈𝗍𝗁𝖾𝗋𝗐𝗂𝗌𝖾 𝗂 𝗐𝗂𝗅𝗅 𝗇𝗈𝗍 𝖺𝖻𝗅𝖾 𝗍𝗈 𝗐𝗈𝗋𝗄 𝗉𝗋𝗈𝗉𝖾𝗋𝗅𝗒.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("𝖴𝗉𝖽𝖺𝗍𝖾𝗌 📡", url=f"https://t.me/{UPDATES_CHANNEL}"),
                                InlineKeyboardButton("📢 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url=f"https://t.me/{GROUP_SUPPORT}")
                            ],
                        ]
                    )
                )
            return
        except Exception:
            return


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
