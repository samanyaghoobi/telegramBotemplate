from telebot.types import Message
from app.core.decorators import handler_guard

# هر فایل یک تابع register(bot) داشته باشد

def register(bot):
    @bot.message_handler(commands=["start"])
    @handler_guard
    def start_cmd(m: Message):
        bot.reply_to(m, "سلام! ربات روشنه ✅")