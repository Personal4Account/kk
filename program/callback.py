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


from driver.core import me_bot, me_user
from driver.queues import QUEUE
from driver.decorators import check_blacklist
from program.utils.inline import menu_markup, stream_markup

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_USERNAME,
    UPDATES_CHANNEL,
    SUDO_USERS,
    OWNER_ID,
)


@Client.on_callback_query(filters.regex("home_start"))
@check_blacklist()
async def start_set(_, query: CallbackQuery):
    await query.answer("home start")
    await query.edit_message_text(
        f"""ʜᴇʟʟᴏ [👋](START_IMG) ɪ ᴀᴍ ᴠᴇɴᴏᴍ sᴜᴘᴇʀ-ғᴀsᴛ ᴠᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ 🤖 ᴛᴏ ᴘʟᴀʏ ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ 🎸 ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘs ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.

┏━━━━━━━━━━━━━━━━━┓
┣★ ᴄʀᴇᴀᴛᴏʀ › : ʀᴏᴍᴇᴏ xᴅ
┣★ ᴜᴘᴅᴀᴛᴇs › : sᴛʀᴀʏ ᴄᴏᴅᴇʀ
┣★ sᴜᴘᴘᴏʀᴛ › : sᴛʀᴀʏ ᴄʜᴀᴛ 
┣★ ᴏғғɪᴄɪᴀʟ  › : ɴᴇᴛᴡᴏʀᴋ 
┣★ ʙʀᴏᴛʜᴇʀ › : ᴄғᴄ ᴘʜᴏᴇɴɪx
┗━━━━━━━━━━━━━━━━━┛

ᴜsᴇ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ !!
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔎 How to use ? Commands", callback_data="command_list")
                ],[
                    InlineKeyboardButton("📨 Support", url=f"https://t.me/{GROUP_SUPPORT}"),
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


@Client.on_callback_query(filters.regex("quick_use"))
@check_blacklist()
async def quick_set(_, query: CallbackQuery):
    await query.answer("quick bot usage")
    await query.edit_message_text(
        f"""Mostly Faced Error ⚠️

There wiil be the main error about to music assistant. If you are facing any type of error in your group then that time first make sure @MusicMicPlayer is available in your group. If not then add it manually and before that make sure also it is not banned in your chat.


If you are facing any issues regarding me kindly report in my support group so the developers can fix me out for your needs.

Thanks !!""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📨 Support", url=f"https://t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton("🔙 Back", callback_data="user_guide")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("user_guide"))
@check_blacklist()
async def guide_set(_, query: CallbackQuery):
    await query.answer("user guide")
    await query.edit_message_text(
        f"""Read the basic guide carefully if you don't know how to use this amazing bot properly !!

• First of all add this amazing bot in your group.

• Make bot as a administrator of your group with needed powers.

• Now give /refresh Command to the bot and then send /play command to invite the music assistant of the bot in your precious group.

• Now all the Setup of the bot is successfully completed. Play your favourite Songs × Videos in the vc with high quality and lag free Sound.

If you are facing any problem in using this bot then first of all check out command section carefully otherwise kindly report in our support group !!""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("❗About Common Error", callback_data="quick_use")
                ],[
                    InlineKeyboardButton("🔙 Back", callback_data="home_start")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("command_list"))
@check_blacklist()
async def commands_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.answer("commands menu")
    await query.edit_message_text(
        f"""Click on the buttons below for more information. If you're facing any problem in command you can contact my bot owner or ask in support chat.

All commands can be used with: /""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Admin Commands", callback_data="admin_command"),
                    InlineKeyboardButton("Play Commands", callback_data="user_command"),
                ],[
                    InlineKeyboardButton("Extra Commands", callback_data="sudo_command"),
                    InlineKeyboardButton("Owner Commands", callback_data="owner_command"),
                ],[
                    InlineKeyboardButton("🔙 Back", callback_data="home_start")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("user_command"))
@check_blacklist()
async def user_set(_, query: CallbackQuery):
    await query.answer("basic commands")
    await query.edit_message_text(
        f"""⚠️ Voice Chat Commands.

» /play (song name/youtube link) - play the music from youtube
» /vplay (video name/youtube link) - play the video from youtube
» /stream (m3u8/youtube live link) - play youtube/m3u8 live stream music
» /vstream (youtube live link) - play youtube/m3u8 live stream video
» /playlist - view the queue list of songs and current playing song
» /lyric (query) - search for song lyrics based on the name of the song
» /song (query) - download song from YouTube
» /video (query) - download video from YouTube""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("admin_command"))
@check_blacklist()
async def admin_set(_, query: CallbackQuery):
    await query.answer("admin commands")
    await query.edit_message_text(
        f"""⚠️ Only Group admins can use this commands.

» /pause - pause the current track being played
» /resume - play the previously paused track
» /skip - goes to the next track
» /stop - stop playback of the track and clears the queue
» /volume `1-200` - adjust the volume of music (userbot must be admin)
» /refresh - refresh the bot server and refresh the admin data
» /userbotjoin - invite the userbot to join group
» /userbotleave - order userbot to leave from group""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("sudo_command"))
@check_blacklist()
async def sudo_set(_, query: CallbackQuery):
    await query.answer("sudo commands")
    await query.edit_message_text(
        f"""⚠️ Extra Commands List.

» /eval - run an code
» /sh - run an code
» /id - Get id of a [Chat , User , Sticker]
» /sysinfo - show the system information
» /repo - Get The Bot Repo !!
» /alive - show the bot alive info (in Group only)
» /speedtest - run the bot server speedtest
» /search (query) - search for the youtube video link
» /ping - show the bot ping status
» /uptime - show the bot uptime status""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("about_bot"))
@check_blacklist()
async def about_set(_, query: CallbackQuery):
    await query.answer("bot about")
    await query.edit_message_text(
        f"""This bot is designed by a noob for playing a high quality and unbreakable music × video in your groups voice chat. This bot is also helps you to download music and video from the YouTube server.

• Bot Managed By 
- @Its_romeoo
- @xtm_BidiBaaz

• Powered by
- @StrayCoder
- @StrayCoderSupport

Note : Contact developers only that time if you have really need a help or facing any type of issues. Don't try to waste our and your time by asking useless queries !!""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Create Your Personal Bot 🤖", callback_data="own_bot")
                ],[
                    InlineKeyboardButton("🔙 Back", callback_data="home_start")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("own_bot"))
@check_blacklist()
async def own_bot(_, query: CallbackQuery):
    await query.answer("Create Your Personal Bot")
    await query.edit_message_text(
        f"""Tutorial soon at :- @StrayCoder

The Tutorial video about to making your own bot like this will be soon available at @StrayCoderSupport. Also source code and all information about making bot published soon.Stay connected with us at our update channel.

Thanks !!""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="home_start")]]
        ),
    )


@Client.on_callback_query(filters.regex("owner_command"))
@check_blacklist()
async def owner_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in OWNER_ID:
        await query.answer("⚠️ Opps, You are not the owner of this Bot.", show_alert=True)
        return
    await query.answer("owner commands")
    await query.edit_message_text(
        f"""✏️ Command list for bot owner.
» /gban (`username` or `user_id`) - for global banned people, can be used only in group
» /ungban (`username` or `user_id`) - for un-global banned people, can be used only in group
» /update - update your bot to latest version
» /restart - restart your bot server
» /leaveall - order userbot to leave from all group
» /leavebot (`chat id`) - order bot to leave from the group you specify
» /broadcast (`message`) - send a broadcast message to all groups in bot database
» /broadcast_pin (`message`) - send a broadcast message to all groups in bot database with the chat pin""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("stream_menu_panel"))
@check_blacklist()
async def at_set_markup_menu(_, query: CallbackQuery):
    user_id = query.from_user.id
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⚠️ Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.message.from_user.id
    buttons = menu_markup(user_id)
    if chat_id in QUEUE:
        await query.answer("control panel opened")
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await query.answer("Nothing is streaming in the vc❗️", show_alert=True)


@Client.on_callback_query(filters.regex("stream_home_panel"))
@check_blacklist()
async def is_set_home_menu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⚠️ Only admin with manage video chat permission that can tap this button !", show_alert=True)
    await query.answer("control panel closed")
    user_id = query.message.from_user.id
    buttons = stream_markup(user_id)
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex("set_close"))
@check_blacklist()
async def on_close_menu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⚠️ Only admin with manage video chat permission that can tap this button !", show_alert=True)
    await query.message.delete()


@Client.on_callback_query(filters.regex("close_panel"))
@check_blacklist()
async def in_close_panel(_, query: CallbackQuery):
    await query.message.delete()
