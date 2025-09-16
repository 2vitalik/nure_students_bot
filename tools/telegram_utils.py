"""
    This module is copied from `shared_utils.api.telegram.telegram_utils`.
"""
import telegram
from telegram.error import BadRequest


def process_keyboard(keyboard):
    return telegram.ReplyKeyboardMarkup([
        [telegram.KeyboardButton(button) for button in line]
        for line in keyboard
    ], resize_keyboard=True)


def process_buttons(buttons):
    if not buttons:
        return None
    return telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(button, callback_data=callback_data)
         for button, callback_data in line]  # todo: case without tuple
        for line in buttons
    ])


class ChatNotFoundError(BadRequest):
    pass


class MessageNotModifiedError(BadRequest):
    pass


def telegram_send(bot, chat_id, text, keyboard=None, buttons=None, silent=False):
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    if keyboard:
        reply_markup = process_keyboard(keyboard)
    elif buttons:
        reply_markup = process_buttons(buttons)
    else:
        reply_markup = None

    try:
        return bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=telegram.ParseMode.HTML,
            disable_web_page_preview=True,
            disable_notification=silent,
            reply_markup=reply_markup,
        )
    except BadRequest as e:
        if 'Chat not found' in str(e):
            raise ChatNotFoundError(str(e)) from e
        raise


def edit(bot, chat_id, message_id, text, buttons=None):
    reply_markup = None
    if buttons:
        reply_markup = process_buttons(buttons)

    try:
        return bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,
            parse_mode=telegram.ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except BadRequest as e:
        if 'Chat not found' in str(e):
            raise ChatNotFoundError(str(e)) from e
        if 'Message is not modified' in str(e):
            raise MessageNotModifiedError(str(e)) from e
        raise


def delete(bot, chat_id, msg_id):
    bot.delete_message(chat_id, msg_id)


def telegram_callback(query, text, buttons):
    query.edit_message_text(
        text=text,
        reply_markup=process_buttons(buttons),
        parse_mode=telegram.ParseMode.HTML,
        disable_web_page_preview=True,
    )
