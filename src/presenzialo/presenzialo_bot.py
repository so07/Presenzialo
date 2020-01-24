import os
import re
import sys
import configparser
from threading import Thread

from telegram import (
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ChatAction,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)

from .presenzialo_auth import PRauth, config_auth
from .presenzialo_web import PRweb
from .presenzialo_day import PRday
from .presenzialo_address import PRaddress


def get_token(config_file):
    parser = configparser.ConfigParser()
    parser.read(config_file)
    return parser.get("PRbot", "token")


token = get_token(config_auth)

print("found token", token)

bot = Bot(token=token)
updater = Updater(token=token)


def get_prweb():
    return PRweb(PRauth())


def _message_format(msg):
    return re.sub(r"[.\.]+", " ", msg)


def bot_wakeup(bot, update):
    keyboard = [
        [KeyboardButton("/time", True, True), KeyboardButton("/stamp", True, True),],
    ]
    # reply_markup = telegram.ReplyKeyboardMarkup(keyboard)

    keyboard = [
        [
            InlineKeyboardButton("time", callback_data="time"),
            InlineKeyboardButton("stamp", callback_data="stamp"),
        ],
        # [
        #  InlineKeyboardButton("in", callback_data='present'),
        #  InlineKeyboardButton("phone", callback_data='phone'),
        #  InlineKeyboardButton("name", callback_data='name'),
        # ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("inline button commands", reply_markup=reply_markup)
    update.message.reply_text("type /help for more commands")


def bot_print(bot, update, msg):
    # msg = re.sub(r"[.\.]+", "\n", msg)
    bot.sendMessage(
        parse_mode="HTML", chat_id=update.message.chat.id, text="<pre>" + msg + "</pre>"
    )
    # bot.send_message(chat_id=update.message.chat_id, text="`" + msg + "`", parse_mode=telegram.ParseMode.MARKDOWN)


def call_prlo(func):
    def wrapped(bot, update, *args, **kwargs):
        ret = func(bot, update, *args, **kwargs)
        bot_wakeup(bot, update)
        return ret

    return wrapped


@call_prlo
def time(bot, update):
    """bot command for uptime"""
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    pr_day = PRday(get_prweb().timecard())
    day = pr_day.days[0]
    msg = "Today  {}\n".format(day.date().date())
    msg += "Uptime {}\n".format(day.uptime())
    bot_print(bot, update, msg)


@call_prlo
def stamp(bot, update):
    """bot command for time stamps"""
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    pr_day = PRday(get_prweb().timecard())
    day = pr_day.days[0]
    msg = "Today  {}\n".format(day.date().date())
    msg += "Stamps {}\n".format(
        ", ".join([i.time().strftime("%H:%M") for i in day.logs()])
    )
    bot_print(bot, update, msg)


@call_prlo
def present(bot, update, args):
    """bot command for worker's presence"""
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    address = PRaddress(get_prweb())
    workers = address.present(args)
    msg = "Workers' status:\n"
    msg += str(address)
    bot_print(bot, update, msg)


# @call_prlo
# def name(bot, update, args):
#    """bot command for worker's name"""
#    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#    address = PRaddress(get_prweb())
#    workers = address.phone(args)
#    msg = "Worker's name:\n"
#    msg += str(workers)
#    bot_print(bot, update, msg)


@call_prlo
def phone(bot, update, args):
    """bot command for worker's phone"""
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    address = PRaddress(get_prweb())
    workers = address.phone(args)
    msg = "Worker's phone:\n"
    msg += str(workers)
    bot_print(bot, update, msg)


@call_prlo
def help(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    msg = """HRbot help

/bot
   inline button command

/time
   today uptime
/stamp
   today time stamps

/in name [name ...]
   worker status
/phone 12345 [12345 ...]
   phone from phone number

/restart
   restart HRbot

/help
   print this help
    """
    update.message.reply_text(msg)
    # bot_print(bot, update, msg)


def button(bot, update):
    query = update.callback_query
    globals()[query.data](bot, query)


def stop(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text="stop me please")
    updater.stop()


def stop_and_restart():
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


def restart(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text("bot is restarting ...")
    Thread(target=stop_and_restart).start()


def main():

    # echo handler
    updater.dispatcher.add_handler(MessageHandler(Filters.text, bot_wakeup))

    updater.dispatcher.add_handler(CommandHandler("bot", bot_wakeup))

    updater.dispatcher.add_handler(CommandHandler("stamp", stamp))
    updater.dispatcher.add_handler(CommandHandler("time", time))

    updater.dispatcher.add_handler(CommandHandler("in", present, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("phone", phone, pass_args=True))
    # updater.dispatcher.add_handler( CommandHandler('name', name, pass_args=True) )

    updater.dispatcher.add_handler(CommandHandler("help", help))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # stop and restart HRbot
    updater.dispatcher.add_handler(CommandHandler("stop", stop))
    updater.dispatcher.add_handler(CommandHandler("restart", restart))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
