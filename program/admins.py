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


import traceback

from cache.admins import admins
from config import BOT_USERNAME, IMG_5

from driver.core import calls, me_user
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.queues import QUEUE, clear_queue
from driver.filters import command, other_filters
from driver.decorators import authorized_users_only, check_blacklist
from driver.utils import skip_current_song, skip_item, remove_if_exists
from driver.database.dbqueue import (
    is_music_playing,
    remove_active_chat,
    music_off,
    music_on,
)

from pyrogram import Client, filters
from program.utils.inline import stream_markup, close_mark
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message(command(["refresh", f"refresh@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
@check_blacklist()
async def update_admin(client, message: Message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "Bot refreshed Successfully❗\nAdmin list has been updated❗️"
    )


@Client.on_message(
    command(["stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vstop"])
    & other_filters
)
@authorized_users_only
@check_blacklist()
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await calls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await m.reply_text("sᴛᴏᴘ ❌ ᴘʟᴀʏɪɴɢ :)")
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"× 404 !! Error ×")
    else:
        await m.reply_text("Nothing is playing in the vc❗️")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                return await m.reply_text("The music is already paused❗")
            await calls.pause_stream(chat_id)
            await music_off(chat_id)
            await m.reply_text(
                "ᴘᴀᴜsᴇᴅ ▶️ ᴍᴜsɪᴄ :("
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"× 404 !! Error ×")
    else:
        await m.reply_text("Nothing is streaming in the vc❗️")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                return await m.reply_text("The music is already resumed❗")
            await calls.resume_stream(chat_id)
            await music_on(chat_id)
            await m.reply_text(
                "ʀᴇsᴜᴍᴇᴅ ⏸ ᴍᴜsɪᴄ :)"
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"× 404 !! Error ×")
    else:
        await m.reply_text("Nothing is streaming in the vc❗️")


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
@check_blacklist()
async def skip(c: Client, m: Message):
    user_id = m.from_user.id
    chat_id = m.chat.id
    queue = await skip_current_song(chat_id)
    if queue == 0:
        await m.reply_text("sᴋɪᴘᴘᴇᴅ ⏩ ᴍᴜsɪᴄ :(")
    elif queue == 1:
        await m.reply_text("There is no more music in queue to skip❗")
    elif queue == 2:
        await m.reply_text("Clearing the queues❗")
    else:
        buttons = stream_markup(user_id)
        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
        thumbnail = f"{IMG_5}"
        title = f"{queue[0]}"
        userid = m.from_user.id
        gcname = m.chat.title
        ctitle = await CHAT_TITLE(gcname)
        image = await thumb(thumbnail, title, userid, ctitle)
        await c.send_photo(
            chat_id,
            photo=image,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=f"[Song Information ⚠️]({queue[1]})\n\n**Group ID:** `{chat_id}`\n**Bot User :** {requester}",
        )
        remove_if_exists(image)


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                return await m.reply_text("The assistant is already muted❗")
            await calls.mute_stream(chat_id)
            await music_off(chat_id)
            await m.reply_text(
                "ᴍᴜᴛᴇᴅ ▶️ ᴜsᴇʀʙᴏᴛ :("
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"× 404 !! Error ×")
    else:
        await m.reply_text("Nothing is streaming in the vc❗️")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                return await m.reply_text("The assistant is already unmuted❗")
            await calls.unmute_stream(chat_id)
            await music_on(chat_id)
            await m.reply_text(
                "ᴜɴᴍᴜᴛᴇᴅ ⏸ ᴜsᴇʀʙᴏᴛ :)"
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"× 404 !! Error ×")
    else:
        await m.reply_text("Nothing is streaming in the vc❗️")


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
@check_blacklist()
async def change_volume(c: Client, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("usage: `/volume` (`0-200`)")
    a = await c.get_chat_member(m.chat.id, me_user.id)
    if not a.can_manage_voice_chats:
        return await m.reply_text(
            "The userbot must be admin in this chat to be able change the volume stream!"
        )
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await calls.change_volume_call(chat_id, volume=int(range))
            await m.reply_text(
                f"**volume set to** `{range}`%❗"
            )
        except Exception as e:
            traceback.print_exc()
            await m.reply_text(f"× 404 !! Error ×")
    else:
        await m.reply_text("Nothing is streaming in the vc❗️")


@Client.on_callback_query(filters.regex("set_pause"))
@check_blacklist()
async def cbpause(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⚠️ Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await query.answer("The music is already paused❗", show_alert=True)
                return
            await calls.pause_stream(chat_id)
            await music_off(chat_id)
            await query.answer("Music Paused❗️", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"× 404 !! Error ×", reply_markup=close_mark)
    else:
        await query.answer("Nothing is streaming in the vc❗️", show_alert=True)


@Client.on_callback_query(filters.regex("set_resume"))
@check_blacklist()
async def cbresume(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⚠️ Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await query.answer("The music is already resumed❗", show_alert=True)
                return
            await calls.resume_stream(chat_id)
            await music_on(chat_id)
            await query.answer("Music Resumed❗️", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"× 404 !! Error ×", reply_markup=close_mark)
    else:
        await query.answer("Nothing is streaming in the vc❗️", show_alert=True)


@Client.on_callback_query(filters.regex("set_stop"))
@check_blacklist()
async def cbstop(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⚠️ Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await calls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("Song has been Stopped❗️", reply_markup=close_mark)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"× 404 !! Error ×", reply_markup=close_mark)
    else:
        await query.answer("Nothing is streaming in the vc❗️", show_alert=True)


@Client.on_callback_query(filters.regex("set_mute"))
@check_blacklist()
async def cbmute(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⚠️ Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await query.answer("The assistant is already muted❗", show_alert=True)
                return
            await calls.mute_stream(chat_id)
            await music_off(chat_id)
            await query.answer("The assistant has been muted❗", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"× 404 !! Error ×", reply_markup=close_mark)
    else:
        await query.answer("Nothing is streaming in the vc❗️", show_alert=True)


@Client.on_callback_query(filters.regex("set_unmute"))
@check_blacklist()
async def cbunmute(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⚠️ Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await query.answer("The assistant is already unmuted❗", show_alert=True)
                return
            await calls.unmute_stream(chat_id)
            await music_on(chat_id)
            await query.answer("The assistant has unmuted❗", show_alert=True)
        except Exception as e:
            traceback.print_exc()
            await query.edit_message_text(f"× 404 !! Error ×", reply_markup=close_mark)
    else:
        await query.answer("Nothing is streaming in the vc❗️", show_alert=True)


@Client.on_callback_query(filters.regex("set_skip"))
@check_blacklist()
async def cbskip(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⚠️ Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    queue = await skip_current_song(chat_id)
    if queue == 0:
        await query.answer("Nothing is streaming in the vc❗️", show_alert=True)
    elif queue == 1:
        await query.answer("There is no more music in queue to Skip❗", show_alert=True)
    elif queue == 2:
        await query.answer("Clearing the queues❗", show_alert=True)
    else:
        await query.answer("goes to the next track, proccessing...")
        await query.message.delete()
        buttons = stream_markup(user_id)
        requester = f"[{query.from_user.first_name}](tg://user?id={query.from_user.id})"
        thumbnail = f"{IMG_5}"
        title = f"{queue[0]}"
        userid = query.from_user.id
        gcname = query.message.chat.title
        ctitle = await CHAT_TITLE(gcname)
        image = await thumb(thumbnail, title, userid, ctitle)
        await _.send_photo(
            chat_id,
            photo=image,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=f"[Song Information ⚠️]({queue[1]})\n\n**Group Id :** `{chat_id}`\n**Bot User :** {requester}",
        )
        remove_if_exists(image)
