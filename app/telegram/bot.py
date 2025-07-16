import os
import signal
import traceback
from telebot import TeleBot
from telebot import apihelper
from app.config import settings
from app.core.logger import logger
from app.core.utils import get_last_rotated_log
from app.telegram.loader import load_handlers
from app.core.filters import IsAdminFilter

_bot: TeleBot | None = None

# تابع ساده برای اطلاع‌رسانی به ادمین اصلی

def notify_admin(text: str):
    global _bot
    if _bot is None:
        return
    try:
        _bot.send_message(settings.MAIN_ADMIN_ID, text, parse_mode="Markdown")
    except Exception:
        logger.error("Failed to send admin notification: %s", text)


def send_startup_report():
    last_log = get_last_rotated_log()
    msg = "🚀 Bot started (polling)."
    if last_log and last_log.exists():
        # ارسال آخرین لاگ دوره قبل
        try:
            notify_admin(msg + "\nSending previous log file...")
            with open(last_log, "rb") as f:
                _bot.send_document(settings.MAIN_ADMIN_ID, f, caption=f"Previous log: {last_log.name}")
        except Exception:
            logger.error("Could not send previous log file")
    else:
        notify_admin(msg)


def graceful_shutdown(*_args):
    # روی سیگنال‌ها
    try:
        notify_admin("⏹️ Bot is shutting down (signal received).")
    except Exception:
        pass
    os._exit(0)


def run_bot():
    global _bot

    _bot = TeleBot(settings.BOT_TOKEN, parse_mode="Markdown")

    # فیلتر ادمین را ثبت کن
    _bot.add_custom_filter(IsAdminFilter())

    # پراکسی/Timeout دلخواه (اختیاری)
    apihelper.SESSION_TIME_TO_LIVE = 5
    apihelper.READ_TIMEOUT = 15
    apihelper.CONNECT_TIMEOUT = 10

    # لود هندلرها
    load_handlers(_bot)

    # گزارش استارتاپ برای ادمین
    send_startup_report()

    # هندل سیگنال‌ها
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    logger.info("Bot is starting polling...")
    _bot.infinity_polling(skip_pending=True, allowed_updates=None, timeout=20, long_polling_timeout=25)