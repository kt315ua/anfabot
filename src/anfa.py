#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import settings
import language
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
from telegram import Update, constants
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ChatMemberHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

token = settings.token


def check_allowed_chats(chat_type, member_chat_id, username):
    is_allowed = False

    if chat_type is constants.ChatType.SUPERGROUP:
        print(f"> SUPERGROUP CHAT CHECK: {member_chat_id}")
        if str(member_chat_id) in settings.allowed_chat_ids():
            is_allowed = True
            print(f">> CHAT is ALLOWED: {member_chat_id}")

    if chat_type is constants.ChatType.PRIVATE:
        print(f"> PRIVATE CHAT CHECK: {member_chat_id}")
        if str(username) == settings.owner_username:
            is_allowed = True
            print(f">> CHAT is ALLOWED: {member_chat_id}")

    if not is_allowed:
        print(f">>> CHAT ID {member_chat_id} is not allowed")
    else:
        print(f">>> CHAT ID {member_chat_id} is allowed")

    return is_allowed


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
    print(f"Show current chat id: {update.message.chat_id}")
    await update.message.reply_text(f"Current chat_id is: {update.message.chat_id}")


async def show_allowed_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Show allowed chats for chat id: {update.effective_chat.id}")
    is_allowed = check_allowed_chats(constants.ChatType.PRIVATE,
                                  update.effective_chat.id,
                                  update.effective_chat.username)
    if is_allowed:
        chat_id = str(settings.allowed_chat_ids())
        await update.message.reply_text(f"Allowed chat ids: {chat_id}")
    else:
        await update.message.reply_text(f"You have no rights to get private data!")


async def check_for_allowed_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Check allowed member chat: {update.my_chat_member.chat.id}")
    is_allowed = check_allowed_chats(update.effective_chat.type,
                                  update.my_chat_member.chat.id,
                                  update.effective_chat.username)
    if not is_allowed:
        await update.effective_chat.send_message(f"Chat id {update.my_chat_member.chat.id} is not allowed!")
        time.sleep(1)
        await update.effective_chat.leave()


async def check_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    user_first_name = update.message.from_user.first_name
    user_last_name = update.message.from_user.last_name
    text = update.message.text if update.message.text else update.message.caption
    need_remove = False

    # Text can be None
    if text:
        if len(text) >= 3:
            if language.is_lang("ru", text):
                need_remove = True

    if need_remove:
        if user_name:
            user = f"@{user_name}"
        elif user_first_name and user_last_name:
            user = f"'{user_first_name} {user_last_name}'"
        elif user_first_name:
            user = f"'{user_first_name}' (id: {user_id})"
        elif user_last_name:
            user = f"'{user_last_name}' (id: {user_id})"
        else:
            user = f"[{user_id}]"

        await update.message.delete()
        await update.effective_chat.send_message(f"Повідомлення користувача {user} видалено!\n"
                                                 f"Використання 'росіянської' заборонено.\n"
                                                 f"Перекладач: https://translate.google.com.ua/")


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
