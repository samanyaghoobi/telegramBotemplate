from telebot.types import Message
from app.core.decorators import handler_guard

# آخرین هندلر برای پیام‌های غیر قابل‌تشخیص

def register(bot):
    @bot.message_handler(func=lambda m: True, content_types=["text", "photo", "document", "audio", "video", "voice"])
    @handler_guard
    def fallback(m: Message):
        bot.reply_to(m, "متوجه نشدم، از /start کمک بگیر.")