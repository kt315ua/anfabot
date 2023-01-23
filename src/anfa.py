#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import time
import settings
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ChatMemberHandler

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

token = settings.token
owner_username = settings.owner_username

cyrrilic_ru = settings.cyrrilic_ru
cyrrilic_ua = settings.cyrrilic_ua


# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_msg = f"Hi {update.effective_user.username if update.effective_user.username else update.effective_user.id}!"
    tutorial_msg = "Supported commends:\n" \
                    "/start - print this message\n" \
                    "/help - print this messahe\n" \
                    "/chatid - show current chat id\n" \
                    "/allowed_chats - show allowed chat ids in config"
    await update.effective_chat.send_message(f"{welcome_msg}\n{tutorial_msg}")


async def show_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = str(update.message.chat_id)
    await update.message.reply_text(f"Current chat_id is: {chat_id}")


async def show_allowed_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(settings.allowed_chat_ids())
    chat_id = str(settings.allowed_chat_ids())
    await update.message.reply_text(f"Allowed chat ids: {chat_id}")


async def check_for_allowed_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    is_allowed = False
    if str(update.my_chat_member.chat.id) in settings.allowed_chat_ids():
        is_allowed = True
        print("CHAT is ALLOWED")

    if str(update.effective_chat.username) == owner_username:
        is_allowed = True
        print("CHAT with OWNER")

    if not is_allowed:
        await update.effective_chat.send_message(f"Chat id {update.my_chat_member.chat.id} is not allowed!")
        time.sleep(1)
        await update.effective_chat.leave()
    else:
        print(f"CHAT ID {update.my_chat_member.chat.id} is allowed")


async def check_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    text = update.message.text if update.message.text else update.message.caption
    need_remove = False
    chat_id = None
    message_id = None
    user_id = None
    user_name = None
    if text:
        for c in cyrrilic_ru:
            result = text.find(str(c))
            if result != -1:
                need_remove = True
                chat_id = update.message.chat_id
                message_id = update.message.message_id
                user_id = update.message.from_user.id
                user_name = update.message.from_user.username
                break

    if need_remove:
        user = user_name if user_name else user_id

        await update.message.delete()
        await update.effective_chat.send_message(f"Повідомлення користувача {user} з російськомовними символами видалено!")


def main() -> None:
    """Start the bot."""
    # Prepare env
    settings.prepare_env()

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("chatid", show_chat_id))
    application.add_handler(CommandHandler("allowed_chats", show_allowed_chats))
    application.add_handler(ChatMemberHandler(check_for_allowed_chats, ChatMemberHandler.MY_CHAT_MEMBER))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND | filters.PHOTO & ~filters.COMMAND | filters.FORWARDED & ~filters.COMMAND,
        check_text
    ))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
