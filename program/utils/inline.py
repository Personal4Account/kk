""" inline section button """


from pyrogram.types import (
  InlineKeyboardButton,
  InlineKeyboardMarkup,
)


def stream_markup(user_id):
  buttons = [
    [
      InlineKeyboardButton(text="ð· á´á´É´á´", callback_data=f'stream_menu_panel | {user_id}'),
      InlineKeyboardButton(text="ðº á´á´á´á´á´á´s", https://t.me/{UPDATES_CHANNEL}),
    ],
  ]
  return buttons


def menu_markup(user_id):
  buttons = [
    [
      InlineKeyboardButton(text="â¢", callback_data=f'set_stop | {user_id}'),
      InlineKeyboardButton(text="â·", callback_data=f'set_pause | {user_id}'),
      InlineKeyboardButton(text="II", callback_data=f'set_resume | {user_id}'),
      InlineKeyboardButton(text="â£â£", callback_data=f'set_skip | {user_id}'),
    ],
    [
      InlineKeyboardButton(text="ð", callback_data=f'set_mute | {user_id}'),
      InlineKeyboardButton(text="ð", callback_data=f'set_unmute | {user_id}'),
    ],
    [
      InlineKeyboardButton(text="ð Go Back", callback_data='stream_home_panel'),
    ]
  ]
  return buttons


close_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "Closeâï¸", callback_data="set_close"
      )
    ]
  ]
)


back_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "ð Go Back", callback_data="stream_menu_panel"
      )
    ]
  ]
)
